<script>
    import "../css/app.css";
    import Sidebar from "./Sidebar.svelte";
</script>

<div class="w-full h-screen flex">
    <Sidebar />
    <div class="w-full h-full overflow-y-auto">
        <slot />
    </div>
</div>