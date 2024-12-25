<script>
    import "../css/app.css";
    import Sidebar from "./Sidebar.svelte";
</script>

<div class="w-full h-screen flex">
    <Sidebar />
    <slot />
</div>