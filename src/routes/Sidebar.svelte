<script lang="ts">
    import {goto} from "$app/navigation";

    const items = [
        {
            title: "Home",
            link: "/"
        },
        {
            title: "MTKCLIENT",
            link: "/mtkclient"
        },
        {
            title: "Documentation",
            link: "/documentation"
        }
    ];
</script>

<div class="w-min h-full bg-primary-800 flex flex-col gap-4 p-4">
    <h1 class="font-bold text-lg">FUCKYOUMOTO</h1>
    {#each items as item}
        <button type="button"
                class="text-white bg-primary-700 hover:bg-accent-500 font-medium rounded-lg text-sm px-5 py-2.5"
                on:click={() => goto(item.link)}>{ item.title }</button>
    {/each}
</div>