<script>
    import { link } from 'svelte-spa-router';
    export let drop_down_name = undefined;
    export let drop_down_options = [
        {
            name: "test",
            link: "/"
        }
    ];

    const isNameShorterThenChild = () => {
        if (drop_down_name === undefined) {
            return false;
        }

        let longest_child_name = 0;
        drop_down_options.forEach((option) => {
            if (option.name.length > longest_child_name) {
                longest_child_name = option.name.length;
            }
        });
        window.pendejadas = window.pendejadas === undefined ? [] : window.pendejadas;
        window.pendejadas.push(`longest_child_name: ${longest_child_name} > drop_down_name: ${drop_down_name.length} == ${longest_child_name > drop_down_name.length}`)
        return drop_down_name.length < longest_child_name;
    };

</script>

<div class="drop-down-container {!isNameShorterThenChild() ? "" : "round-corner-drop-down"}">
    {#each drop_down_options as option}
        <div class="ddc-option">
            <a href="{option.link}" use:link>{option.name}</a>
        </div>
    {/each}
</div>

<style>
    .drop-down-container {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        min-width: max-content;
        background: var(--clear-color);
        border-radius: 0 0 var(--boxes-roundness) var(--boxes-roundness);
        box-shadow: var(--boxes-shadow);
        z-index: var(--z-index-10);
    }

    .drop-down-container.round-corner-drop-down {
        border-radius: 0 var(--boxes-roundness) var(--boxes-roundness) var(--boxes-roundness);
    }

    :global(.drop-down-parent:hover .drop-down-container) {
        display: block;
    }

    .ddc-option {
        cursor: pointer;
        padding: var(--spacing-2);
        color: var(--primary-color);
    }

    .ddc-option:last-child {
        border-radius: inherit;
    }

    .ddc-option:hover {
        background: var(--tertiary-color-light);
        color: var(--clear-color);
        transition: all 0.2s ease-in-out;
    }

    .ddc-option a {
        text-decoration: none;
        color: inherit;
    }

    .drop-down-container.round-corner-drop-down > .ddc-option:first-child {
        border-radius: 0 var(--boxes-roundness) 0 0;
    }
</style>