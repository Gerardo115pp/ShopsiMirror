<script>
    import CompletedReports from './site-components/CompletedReports.svelte';
    import RapidReportPanel from './site-components/RapidReportPanel.svelte';
    import { newNotification } from '../../components/notifications/events';
    import { GetReportsList } from '../../libs/HttpRequests';
    import bonhart_storage from '../../libs/bonhart-storage';
    import { onMount } from 'svelte';

    let completed_reports = []; 

    onMount(() => {
        getReportsList();
    });

    function getReportsList() {
        const reports_list_request = new GetReportsList(bonhart_storage.Token);

        const on_success = reports_list => {
            completed_reports = reports_list;
        }

        const on_error = error => {
            newNotification(`Error al obtener la lista de reportes: ${error}`);
        }

        reports_list_request.do(on_success, on_error);
    }
</script>

<main id="reports-administration">
    <section id="rapid-reports-section">
        <RapidReportPanel />
    </section>
    <section id="completed-reports-section">
        <CompletedReports reports={completed_reports} />
    </section>
</main>

<style>
    #rapid-reports-section {
        display: grid;
        place-items: center;
        padding: var(--spacing-3) 0;
    }

    #completed-reports-section {
        margin-top: var(--spacing-h4);
    }
</style>