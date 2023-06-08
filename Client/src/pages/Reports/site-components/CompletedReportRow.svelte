<script>
    import { RequestProductPerformanceReportFile } from '../../../libs/HttpRequests';
    import { newNotification } from '../../../components/notifications/events'
    import bonhart_storage from '../../../libs/bonhart-storage';
    import { logout } from '../../../libs/dandelion-utils';
    import { link } from 'svelte-spa-router';
 
    export let report_data = {
        completed: 0,
        records: 0,
        last_update: "2022-08-22 18:17:40",
        serial: 1
    }

    const date_formatter = new Intl.DateTimeFormat('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    });

    const handleDownloadReport = () => {
        const download_report_request = new RequestProductPerformanceReportFile(bonhart_storage.Token);
        download_report_request.serial = report_data.serial;

        const on_success = (report_blob, filename) => {
            const url = window.URL.createObjectURL(report_blob);
            const download_element = document.createElement('a');
            download_element.href = url;
            download_element.download = filename;
            download_element.click();
        }

        const on_error = error => {
            if (error == 401) {
                newNotification('Sesión expirada, por favor inicia sesión de nuevo');
                logout();
                return;
            }
            newNotification(`Error al descargar el reporte: ${error}`);
        }

        download_report_request.do(on_success, on_error);
    }
</script>

<div class="report-row-wrapper">
    <span class="report-name">reporte {report_data.serial}</span>
    <span class="report-date">creado el <span class="highlighted-text">{date_formatter.format(Date.parse(report_data.last_update))}</span></span>
    <span class="report-actions">
        <span on:click={handleDownloadReport} class="material-symbols-outlined full-two-btn">download</span>
    </span>
</div>

<style>
    .report-row-wrapper {
        display: grid;
        background: var(--primary-color);
        grid-template-columns: repeat(6, 1fr);
        color: var(--clear-color);
        padding: var(--spacing-2) var(--spacing-3);
    }

    .report-row-wrapper:not(:last-child) {
        border-bottom: 1px solid var(--clear-color);
    }

    .report-name {
        grid-column: 1 / 2;
    }

    .report-date {
        grid-column: 2 / 5;
        text-align: right;
    }

    .report-date .highlighted-text {
        color: var(--clear-theme-color);
    }

    .report-date .highlighted-text::before {
        content: "'";
    }

    .report-date .highlighted-text::after {
        content: "'";
    }

    .report-actions {
        grid-column: 6 / 7;
        display: flex;
        justify-content: flex-end;
    }

    .report-actions > span {
        cursor: default;
    }
</style>