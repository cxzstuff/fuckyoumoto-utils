use std::{fs, env};
use chrono::Local;
use std::process::{Child, Command, Stdio};
use std::io::{BufReader, BufRead};
use std::ops::Deref;
use std::sync::{Arc, Mutex};
use lazy_static::lazy_static;
use tauri::Window;
use tauri::Emitter;
use sysinfo::{Pid, System};

lazy_static! {
    pub static ref process_pid: Arc<Mutex<Option<u32>>> = Arc::new(Mutex::new(None));
}

fn kill_process(pid: u32) -> Result<(), String> {
    let processes = System::new_all();

    if let Some(process) = processes.process(Pid::from_u32(pid)) {
        process.kill();
        Ok(())
    } else {
        Err(format!("Failed to get process pid: {}", pid))
    }
}

#[tauri::command]
async fn run_command(command: String, window: Window) -> Result<(), String> {
    let mut process_pid_lock = process_pid.lock().unwrap();

    if process_pid_lock.is_some() {
        let pid: u32 = *process_pid_lock.as_ref().ok_or("Failed to get process pid")?;
        kill_process(pid)?;
    };

    let mut child = Command::new("sh")
        .arg("-c")
        .arg(command)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to start command: {}", e))?;

    *process_pid_lock = Some(child.id());

    let stdout = child.stdout.take().ok_or("Failed to capture stdout")?;
    let reader = BufReader::new(stdout);

    for line in reader.lines() {
        if let Ok(line) = line {
            // Emit the log line to the frontend
            window.emit("log", line).map_err(|e| format!("Failed to emit log: {}", e))?;
        }
    }

    child.wait().map_err(|e| format!("Failed to wait on child: {}", e))?;
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            run_command
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
