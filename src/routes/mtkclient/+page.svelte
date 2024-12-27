<script lang="ts">
    import { invoke } from "@tauri-apps/api/core";
    import { onMount } from "svelte";
    import { listen } from "@tauri-apps/api/event";
    import { tick } from "svelte";

    let logs: any[] = [];
    let logContainer: HTMLElement;

    // Слушаем события логов и обновляем состояние
    onMount(() => {
        const unlisten = listen("log", (event) => {
            logs = [...logs, event.payload]; // Добавляем новый лог
        });

        return () => {
            unlisten.then((fn) => fn()); // Отписка от событий при уничтожении компонента
        };
    });

    // Функция для выполнения команды и очистки логов
    async function runCommand(command: string): Promise<void> {
        logs = []; // Очищаем логи перед запуском новой команды
        await invoke("run_command", { command });
    }

    // Функция для прокрутки контейнера
    async function scrollToBottom() {
        // Ждем, пока Svelte завершит рендеринг
        await tick();
        if (logContainer) {
            logContainer.scrollTop = logContainer.scrollHeight; // Прокручиваем контейнер до самого низа
        }
    }

    // Следим за изменением логов и прокручиваем контейнер
    $: logs, scrollToBottom();
</script>

<div class="w-full h-full flex flex-col">
    <div class="w-full flex flex-shrink-0 flex-col gap-4 overflow-x-auto">
        <div class="w-full flex items-center gap-4 p-4 pb-0">
            <h4>Partitions:</h4>
            <button type="button"
                    class="text-white bg-primary-700 hover:bg-accent-500 font-medium rounded-lg text-sm px-5 py-2.5 h-10 whitespace-nowrap"
                    on:click={() => runCommand("python ./scripts/backup.py")}>Backup critical partitions</button>
        </div>
        <div class="w-full flex items-center gap-4 p-4 pt-0">
            <h4>Logs:</h4>
            <button type="button"
                    class="text-white bg-primary-700 hover:bg-accent-500 font-medium rounded-lg text-sm px-5 py-2.5 h-10 whitespace-nowrap"
                    on:click={() => runCommand("python ./scripts/get_logs.py")}>Get expdb logs</button>
        </div>
    </div>
    <div class="flex flex-col h-[100%] overflow-y-auto bg-gray-800 rounded-lg p-4 shadow-inner" bind:this={logContainer}>
        {#if logs.length > 0}
            {#each logs as log, index}
                <p class="text-sm font-mono text-gray-300 mb-1">[{index + 1}] {log}</p>
            {/each}
        {:else}
            <p class="text-gray-500 text-center italic">No logs available yet.</p>
        {/if}
    </div>
</div>