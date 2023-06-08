<script>
    import { Datepicker } from 'svelte-calendar';
    import { emitTimeRangeChanged } from '../events';

    export let performance_recorded_between ;
    let selected_start_date = performance_recorded_between?.first;
    let selected_end_date = performance_recorded_between?.last;


    let first_calendar_store;
    let last_calendar_store;
    let calendar_theme = {
        "calendar": {
            "width": "20vw",
            "maxWidth": "100vw",
            "legend": {
                "height": "45px"
            },
            "shadow": "var(--boxes-shadow)",
            "colors": {
                "text": {
                    "primary": "#333",
                    "highlight": "#fff"
            },
            "background": {
                "primary": "var(--clear-color)",
                "highlight": "var(--primary-color)",
                "hover": "var(--dark-tranparent-background)"
            },
            "border": "#eee"
            },
            "font": {
                "regular": "var(--font-size-small)",
                "large": "var(--font-size-small)",
            },
            "grid": {
                "disabledOpacity": ".35",
                "outsiderOpacity": ".6"
            }
        }
    }

    $: handleTimeRangeChange(), selected_end_date, selected_start_date;

    let spanish_date_formatter = new Intl.DateTimeFormat('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    function handleTimeRangeChange() {
        emitTimeRangeChanged({
            first: selected_start_date,
            last: selected_end_date
        });
    }

</script>

<div id="mlp-tf-date-filter">
    <span class="mlp-tf-df-label">Rango de fechas</span>
    <div class="datepicker-wrapper"  id="mlp-tf-df-first-date">
        <Datepicker bind:selected={selected_start_date} theme={calendar_theme} start={performance_recorded_between.first} end={performance_recorded_between.last}  bind:store={first_calendar_store} let:key let:send let:receive>
            <button class="full-btn" in:receive|local={{ key }} out:send|local={{ key }}>
                {#if $first_calendar_store?.hasChosen}
                    Desde {spanish_date_formatter.format($first_calendar_store?.selected).toLowerCase()}
                {:else}
                    Desde {spanish_date_formatter.format(performance_recorded_between.first).toLowerCase()}
                {/if}
            </button>
        </Datepicker>
    </div>
    <div class="datepicker-wrapper" id="mlp-tf-df-last-date">
        <Datepicker  bind:selected={selected_end_date} start={performance_recorded_between.first} end={performance_recorded_between.last} theme={calendar_theme} bind:store={last_calendar_store} let:key let:send let:receive>
            <button class="full-btn" in:receive|local={{ key }} out:send|local={{ key }}>
                {#if $last_calendar_store?.hasChosen}
                    Hasta {spanish_date_formatter.format($last_calendar_store?.selected).toLowerCase()}
                {:else}
                    Hasta {spanish_date_formatter.format(performance_recorded_between.last).toLowerCase()}
                {/if}
            </button>
        </Datepicker>
    </div>
</div>

<style>
    #mlp-tf-date-filter {
        display: flex;
        align-items: center;
        column-gap: var(--spacing-1);
    }

    .mlp-tf-df-label {
        margin: 0 var(--spacing-1) 0 0;
    }

    .datepicker-wrapper button.full-btn {
        text-transform: lowercase;
    }
</style>