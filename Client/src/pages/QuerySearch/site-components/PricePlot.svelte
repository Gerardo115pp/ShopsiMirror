<script>
    import Line from 'svelte-chartjs/src/Line.svelte';

    export let my_item_price = -1;
    export let search_results = [];

    const getPricesSorted = results => {
        const prices = results.map(item => item.price);
        const sorted_prices = prices.sort((a, b) => a - b);
        return sorted_prices;
    }
    
    const getMyPriceData = (my_price, length) => {
        const my_price_data = [];
        for(let i = 0; i < length; i++){
            my_price_data.push(my_price);
        }
        return my_price_data;
    }

    $: sorted_prices = getPricesSorted(search_results);
    $: my_price_line_data = getMyPriceData(my_item_price, sorted_prices.length);

    $: dataLine = {
        labels: sorted_prices,
        datasets: [
            {
                label: "Your price",
                fill: true,
                lineTension: 0.1,
                backgroundColor: "   rgba(209, 132, 132, 0.609)",
                borderColor: " rgb(205, 59, 59)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "  rgb(165, 225, 0)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: my_price_line_data
            },
            {
                label: "Competitor prices",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(160, 149, 255, 0.301)",
                borderColor: "rgb(35, 26, 136)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 26, 136)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: sorted_prices
            }
        ]
    };
</script>

<div id="hpc-prices-chart">
    {#if my_item_price >= 0 && search_results.length > 0}
         <Line data={dataLine}/>
    {/if}
</div>

<style>
    #hpc-prices-chart {
        width: 50%;
        height: 44vh;
        display: flex;
        background-color: white;
        justify-content: center;
        align-items: center;
        border-radius: var(--boxes-roundness);
        box-shadow: 0 4px 10px 1px rgba(26, 0, 51, 0.253);
    }
</style>