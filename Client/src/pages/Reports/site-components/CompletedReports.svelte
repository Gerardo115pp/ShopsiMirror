<script>
    import CompletedReportRow from "./CompletedReportRow.svelte";


    export let reports = [
        {
            completed: 0,
            records: 0,
            last_updated: "2022-08-22 18:17:40",
            serial: 1
        }
    ];
</script>

<div id="completed-reports-wrapper">
    <h3 class="page-title">Reportes completados</h3>
    <div id="crw-reports-container">
        {#each reports as report}
            <CompletedReportRow report_data={report} />
        {/each}
    </div>
</div>

<style>
    #completed-reports-wrapper {
        width: 100%;
        padding: var(--spacing-2) var(--spacing-h4);
    }

    #crw-reports-container {
        width: 60%;
        overflow: hidden;
        border-radius: var(--boxes-roundness);
        margin-top: var(--spacing-3);
    }
</style>