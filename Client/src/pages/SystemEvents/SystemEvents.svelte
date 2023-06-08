<script>

    import EventsContainer from "./page-components/EventsContainer.svelte";

</script>

<main id="bonhart-system-events">
    <h2 class="page-title">Eventos del sistema</h2>
    <div id="events-container-component-wrapper">
        <EventsContainer />
    </div>
</main>

<style>
    #bonhart-system-events .page-title {
        margin: var(--spacing-4) var(--spacing-2);
    }

    #events-container-component-wrapper {
        padding: var(--spacing-3) var(--spacing-4);
    }
</style>