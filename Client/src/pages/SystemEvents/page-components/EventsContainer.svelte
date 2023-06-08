<script>
    import { critical_events, important_events, info_events } from '../event_types'
    import { newNotification } from '../../../components/notifications/events';
    import { GetSystemEventsRequest } from '../../../libs/HttpRequests';
    import bonhart_storage from '../../../libs/bonhart-storage';
    import { onMount } from 'svelte';

    let events = [];

    onMount(() => {
        const events_request = new GetSystemEventsRequest(bonhart_storage.Token);

        const on_success = data => {
            events = data.reverse(); // reverse to show the most recent events first
        };

        const on_error = error_code => {
            newNotification(`Error getting the system events, please report ${error_code}`);
        }

        events_request.do(on_success, on_error);
    });

    const getEventClass = event_type => {
        let event_class = "event-type-info";
        
        if (!info_events.has(event_type)) {
            event_class = critical_events.has(event_type) ? "event-type-critical" : "event-type-important";
        }

        return event_class
    }

</script>

<div id="bonhart-events-container">
    <ol id="bec-bonhart-events">
        {#each events as event}
            <li class="bonhart-event">
                <div class="main-event-data">
                    <div class="event-type-wrapper">
                        <div class={`event-type ${getEventClass(event.type)}`}>{event.type.replace('_', ' ')}</div>
                    </div>
                    <div class="event-description">{event.description}</div>
                </div>
                <div class="event-metadata-row">
                    <div class="event-actor-wrapper">{event.actor}</div>
                    <div class="event-ocurrence-date">{event.ocurred_at}</div>
                </div>
            </li>
        {/each}
    </ol>
</div>

<style>
    #bonhart-events-container {
        width: 100%;
    }
    
    #bec-bonhart-events {
        list-style: none;
        display: flex;
        flex-direction: column;
        row-gap: var(--spacing-3);
        padding: 0;
        margin: 0;
    }
    
    .bonhart-event {
        width: 100%;
        height: max(10vh, 150px);
        color: white;
        background-color: var(--primary-color);
        border-radius: var(--boxes-roundness);
        padding: calc(var(--spacing-3) * .6) var(--spacing-3);
    }

    .main-event-data {
        --event-type-info-color: #00E0FF;
        --event-type-important-color: #FFE600;
        --event-type-critical-color: #FE5353;
        
        width: 100%;
        height: 80%;
        display: flex;
        column-gap: var(--spacing-3);
    }

    .event-type-wrapper {
        min-width: 10%;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .event-type {
        background: transparent;
        border-radius: var(--boxes-roundness);
        border: 1px solid var(--primary-color);
        padding: var(--spacing-2) var(--spacing-3);
        text-transform: capitalize;
    }

    .event-type.event-type-info {
        color: var(--event-type-info-color);
        border-color: var(--event-type-info-color);
    }

    .event-type.event-type-important {
        color: var(--event-type-important-color);
        border-color: var(--event-type-important-color);
    }

    .event-type.event-type-critical {
        color: var(--event-type-critical-color);
        border-color: var(--event-type-critical-color);
    }

    .event-description {
        max-width: 80%;
        min-width: 50%;
    }

    .event-metadata-row {
        display: flex;
        justify-content: space-between;
        padding-left: calc(var(--spacing-3) * 2);
    }

    .event-actor-wrapper {
        font-size: var(--font-size-small);
    }
    
    .event-ocurrence-date {
        font-size: var(--font-size-small);
    }
</style>