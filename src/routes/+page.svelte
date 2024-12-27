<script lang="ts">
    import SvelteMarkdown from "svelte-markdown";
    import source from "$lib/main.md?raw";
    import "../css/markdown.css";
</script>

<div class="markdown w-full px-12">
    <SvelteMarkdown {source} />
</div>