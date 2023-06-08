<script>
    import RapidReportTransmisor, { rapid_report_messages } from '../../../libs/transmisors';
    import { products_server } from '../../../libs/HttpRequests'; 
    import { GetRapidReport } from '../../../libs/HttpRequests';
    import bonhart_storage from '../../../libs/bonhart-storage';
    import { onMount } from 'svelte';

    let transmisor = new RapidReportTransmisor();
    let rapid_report_human_message = 'El proceso no se ha iniciado';
    let progress_bar = undefined;
    let report_length = 0;
    let report_progress = 0;

    const handleTransmisorMessages = message_data => {
        if(message_data.human_message !== undefined) {
            rapid_report_human_message = message_data.human_message;
        }
        
        switch (message_data.type) {
            case rapid_report_messages.PROGRESS_MADE:
                report_length = message_data.length;
                report_progress = message_data.progress;
                const absolute_progress = (report_progress / report_length);
                setProgress(absolute_progress);
                break;
            case rapid_report_messages.STAGE_CHANGED:
                if ('length' in message_data) {
                    report_length = message_data.length;
                    report_progress = message_data.progress;
                }
                break;
            case rapid_report_messages.REPORT_FINISHED:
                const { report_id } = message_data;
                transmisor.Close();
                transmisor = new RapidReportTransmisor();
                downloadReport(report_id);
                break;
        }
    }

    const downloadReport = report_id => {
        const get_rapid_report = new GetRapidReport(bonhart_storage.Token);
        get_rapid_report.report_id = report_id;

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

        get_rapid_report.do(on_success, on_error);
    }

    const requestRapidReport = () => {

        transmisor.message_callback = handleTransmisorMessages
        transmisor.connect();
    }

    const setProgress = progress => {
        const computed_style = getComputedStyle(progress_bar);
        const svg_container_width = document.querySelector('#rapid-reports-panel svg').clientWidth;
        const stroke_width = parseFloat(computed_style.strokeWidth);
        const loader_percentage = (parseFloat(computed_style.r)*2)/100; // this is allways a percentage of the svg container width
        let loader_size = svg_container_width * loader_percentage;
        loader_size -= stroke_width*5;
        const loader_radius = (loader_size/2) - stroke_width;
        let circumference = 2 * Math.PI * loader_radius;
        circumference = circumference.toFixed(2);
        let offset = circumference - (progress * circumference);
        // offset = offset + (offset * 0.15);
        console.log(`progress: ${progress} is ${offset} from ${circumference}`);
        progress_bar.style.setProperty('--stroke-dasharray', `${circumference}px`);
        progress_bar.style.setProperty('--stroke-dashoffset', `${offset}px`);
    }
</script>

<div id="rapid-reports-panel">
    <div id="rapid-reports-panel-header">
        <h2>
            Solicitar reporte rápido
        </h2>
    </div>
    <div id="rrp-progress-bar-wrapper">
        <div id="rrp-progress-bar-stage">
            <h3>
                {rapid_report_human_message}
            </h3>
        </div>
        <svg>
            <circle class="bg" cx="50%" cy="50%" r="22%"/>
            <circle bind:this={progress_bar} class="progress-meter" cx="50%" cy="50%" r="22%" />
            <text class="progress-text" x="50%" y="54%">({report_progress}/{report_length})</text>
        </svg>
    </div>
    <div id="rrp-request-btn-wrapper">
        <button on:click={requestRapidReport} id="rrp-request-btn" class="material-symbols-outlined full-two-btn">bolt</button>
    </div>
</div>

<style>
    /* #rapid-reports-panel * {
        border: 1px solid red;
    } */

    #rapid-reports-panel {
        display: grid;
        width: 52%;
        box-sizing: content-box;
        min-height: calc(var(--spacing-4) * 2.8);
        padding: var(--spacing-3);
        grid-template-columns: repeat(4, 1fr);
        background: var(--primary-gradient);
        border-radius: var(--boxes-roundness);
        box-shadow: var(--boxes-shadow);
        grid-template-areas:
            "hea hea hea hea"
            'pbw pbw pbt pbt'
        ;
    }

    #rapid-reports-panel-header {
        grid-area: hea;
        display: grid;
        place-items: center;
        color: var(--clear-color);
    }


    #rrp-progress-bar-wrapper {
        grid-area: pbw;
    }

    #rrp-progress-bar-stage {
        color: var(--clear-color);
    }

    #rrp-progress-bar-stage h3 {
        font-weight: 500;
        margin: 0;
        font-size: var(--font-size-small);
        text-align: center;
    }

    /* Loading bar */

    #rrp-progress-bar-wrapper svg {
        --circle-radius: 22%; /* This must allways be in percentage */
        --circle-stroke-width: calc(var(--spacing-1) * 1.1); 
        width: 100%;
        min-height: 80%;
    }

    #rrp-progress-bar-wrapper svg circle.bg {
        fill: none;
        stroke: var(--grey-color);
        stroke-width: var(--spacing-1);
    }

    #rrp-progress-bar-wrapper svg circle.progress-meter {
        --stroke-dasharray: 200%;
        --stroke-dashoffset: 200%;

        opacity: 1;
        fill: none;
        stroke: var(--ready);
        stroke-width: var(--circle-stroke-width);
        stroke-linecap: square;
        stroke-dasharray: var(--stroke-dasharray);
        stroke-dashoffset: var(--stroke-dashoffset);
        transform: rotate(90deg);
        transform-origin: 50% 50%;
        transition: stroke-dashoffset .2s ease-in-out;
    }
    
    .progress-text {
        fill: var(--clear-color);
        font-family: var(--primary-font);
        font-size: var(--font-size-1);
        font-weight: 500;
        text-anchor: middle;
    }

    #rrp-request-btn-wrapper {
        grid-area: pbt;
        display: grid;
        place-items: center;
    }
</style>