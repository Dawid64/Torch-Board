<script lang="ts">
    import { onDestroy } from "svelte";
    import ChartComponent from "./components/charts/ChartComponent.svelte";
    import OptimizerVariablesEditor from "./components/OptimizerVariablesEditor.svelte";

    import { ServerState } from "./common/ServerCommunication";

    import { chartOptions, colorPalette } from "./chartConfig/chartConfig";

    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    let serverState = new ServerState(BACKEND_URL);

    async function doAction(actionType: string) {
        serverState.triggerAction(actionType, null);
    }
    //Subscribe to server state values
    let chartVars = serverState.chartValues.value;
    const unsubscribeChartVars = serverState.chartValues.subscribe((value) => {
        chartVars = value;
    });

    let boardVars = serverState.boardValues.value;
    const unsubscribeBoardVars = serverState.boardValues.subscribe((value) => {
        boardVars = value;
    });

    let optimizerVars = serverState.optimizerVariables.value;
    const unsubscribeOptimizerVars = serverState.optimizerVariables.subscribe((value) => {
        optimizerVars = value;
    });

    onDestroy(() => {
        unsubscribeChartVars();
        unsubscribeBoardVars();
        unsubscribeOptimizerVars();
    });

    function makeDatasets(chartVars: Map<string, number[]>) {
        let datasets: any[] = [];

        let usedColors = new Set<string>(); // Zestaw użytych kolorów
        chartVars.forEach((value, key) => {
            if (key !== "loss") {
                const color = colorPalette[Array.from(usedColors).length % colorPalette.length];
                usedColors.add(color);
                datasets.push({
                    label: key,
                    data: value,
                    borderColor: colorPalette.find((color) => !usedColors.has(color)) || "gray",
                    backgroundColor: "rgba(0, 0, 255, 0.1)", // Stała wartość
                    fill: false, // Stała wartość
                });
            }
        });
        return datasets;
    }

    $: datasets = makeDatasets(chartVars);
    $: labels_length = datasets.map((dataset) => dataset.data.length).reduce((a, b) => Math.max(a, b), 0);
</script>

<header>
    <h1 style="color:orange">Torch-Board</h1>
    <div>
        {#if boardVars.get("connected")}
            <p style="color:green">Connected</p>
        {:else}
            <p style="color:red">Waiting for server connection...</p>
        {/if}
        {#if boardVars.get("training")}
            <p style="color:green">Training in progress</p>
        {:else}
            <p style="color:yellow">Training paused...</p>
        {/if}
    </div>
    <section class="action-section">
        <h2 style="color:orange">Actions</h2>
        {#each ["save_model", "toggle_training"] as action}
            <button on:click={() => doAction(action)}>{action.replace("_", " ")}</button>
        {/each}
    </section>
</header>
<main>
    <div class="horizontal-split flex-space-filling">
        <section class="chart-section">
            <!-- Pierwszy wykres -->
            <h2 style="color:orange">Chart</h2>
            <ChartComponent
                chartData={{
                    labels: new Array(labels_length).fill(null).map((_, i) => i),
                    datasets: datasets,
                }}
                {chartOptions}
                chartType="line"
            />
        </section>
        <div class="list-vertical flex-space-filling">
            <section class="form-section list-vertical">
                <OptimizerVariablesEditor {optimizerVars} onSubmitChange={(k, v) => serverState.updateOptimizerValue(k, v)} />
            </section>
        </div>
    </div>
</main>

<style>
    header {
        max-height: 100px;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        gap: 20px;

        border-bottom: 2px solid orange;
    }
    main {
        flex-grow: 1;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;

        gap: 20px;
        padding: 20px;

        width: 100%;
        max-height: calc(100vh - 100px);

        overflow-y: scroll;
    }

    /* Styl dla przycisków */
    button {
        padding: 12px 18px;
        font-size: 16px;
        font-weight: 500;
        background-color: #99c8ff;
        color: white;
        border: 1px solid #365575;
        border-radius: 4px;
        cursor: pointer;
        transition:
            background-color 0.3s ease,
            transform 0.2s ease;
    }

    button:hover {
        background-color: #99c8ff;
        transform: translateY(-2px);
    }

    button:active {
        background-color: #6197d6;
        transform: translateY(0);
    }
    .flex-space-filling {
        flex-grow: 1;
    }
    .horizontal-split {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-start;
        gap: 20px;

        max-width: 100%;
        width: 100%;
    }

    .list-vertical {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 20px;

        height: inherit;
        max-height: 100%;
    }
    .chart-section {
        min-height: 100%;
        min-width: 70%;
        flex-grow: 1;
        margin: 0;
    }
    /* .chart-section {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #fff;
  }

  .form-section {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #fff;
  } */

    .action-section {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: center;
        flex-grow: 1;
        gap: 20px;
    }
    .action-section button {
        text-transform: capitalize;
    }
</style>
