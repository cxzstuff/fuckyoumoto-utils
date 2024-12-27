use std::{env};
use std::process::Stdio;
use tauri::Emitter;
use sysinfo::{Pid, System};

use std::sync::Arc;
use tokio::process::Command;
use tokio::sync::Mutex;
use lazy_static::lazy_static;
use tauri::Window;
use tauri::async_runtime::spawn;

lazy_static! {
    pub static ref PROCESS_PID: Arc<Mutex<Option<u32>>> = Arc::new(Mutex::new(None));
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
    let process_pid_lock = PROCESS_PID.clone();
    let mut pid = process_pid_lock.lock().await;

    // Kill the previous process if it is in an infinite loop or hangs
    if pid.is_some() {
        let pid: u32 = *pid.as_ref().ok_or("Failed to get process pid")?;
        kill_process(pid)?;
    };

    let mut child = Command::new("sh")
        .arg("-c")
        .arg(&command)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to start command: {}", e))?;

    *pid = Some(child.id().unwrap_or_default() as u32);

    let stdout = child.stdout.take().ok_or("Failed to capture stdout")?;
    let stderr = child.stderr.take().ok_or("Failed to capture stderr")?;
    let stdout_reader = tokio::io::BufReader::new(stdout);
    let stderr_reader = tokio::io::BufReader::new(stderr);

    let stdout_window = window.clone();
    let stderr_window = window.clone();

    let stdout_task = spawn(async move {
        let mut lines = tokio::io::AsyncBufReadExt::lines(stdout_reader);
        while let Ok(Some(line)) = lines.next_line().await {
            stdout_window.emit("log", line).ok();
        }
    });

    let stderr_task = spawn(async move {
        let mut lines = tokio::io::AsyncBufReadExt::lines(stderr_reader);
        while let Ok(Some(line)) = lines.next_line().await {
            stderr_window.emit("log", line).ok();
        }
    });

    let status = child.wait().await.map_err(|e| format!("Failed to wait on child: {}", e))?;
    let _ = tokio::try_join!(stdout_task, stderr_task);

    if status.success() {
        window.emit("log", "Command completed successfully")
            .map_err(|e| format!("Failed to emit success status: {}", e))?;
    } else {
        window.emit("log", format!("Command failed with status: {:?}", status))
            .map_err(|e| format!("Failed to emit failure status: {}", e))?;
    }

    // Successfully, deleting the last pid
    *pid = None;

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
