<script lang="ts">
    import SimpleLineChart from "./SimpleLineChart.svelte";
    import SimpleBarChart from "./SimpleBarChart.svelte";
    import AdvancedLineChart from "./AdvancedLineChart.svelte";
    import AdvancedBarChart from "./AdvancedBarChart.svelte";
    import NeuralNetwork from "./NeuralNetwork.svelte";
    import ChartComponent from "./ChartComponent.svelte";

    export let variables: { [key: string]: number[] } = {};

    let charts: [{ [key:string]: string[]}] = [];
</script>