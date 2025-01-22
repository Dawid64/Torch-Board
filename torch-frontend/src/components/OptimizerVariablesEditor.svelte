<script lang="ts">
    export let optimizerVars: Map<string, any>;
    export let onSubmitChange = (name: string, value: any) => {
        console.log("Submitted Values:", value);
        console.log("Submitted name:", name);
    };

    let selectedOption: string | null = null; // Domyślnie pierwszy element

    $: selectedOptValue = selectedOption ? optimizerVars.get(selectedOption) : null;

    let dynamicValues: any = null;

    function handleSelectionChange() {
        if (selectedOption) {
            if (typeof optimizerVars.get(selectedOption) === "object") {
                dynamicValues = [...optimizerVars.get(selectedOption)]; // Copy array
            } else {
                dynamicValues = optimizerVars.get(selectedOption);
            }
        }
    }

    function handleSubmit() {
        if (!selectedOption) {
            return;
        }

        //No submit for empty values
        if (dynamicValues === null || dynamicValues === "") {
            return;
        }

        if (typeof dynamicValues != "object"){
            //No submit for same values
            if (dynamicValues === optimizerVars.get(selectedOption)) {
                return;
            }
        } else {
            //No submit for same values
            const oldValues = optimizerVars.get(selectedOption);
            if (typeof oldValues != "object") {
                return;
            }  
            //compare arrays
            if (oldValues.length === dynamicValues.length && oldValues.every((value:number, index:number) => value === dynamicValues[index])) {
                console.log("No changes detected", oldValues, dynamicValues);
                return;
            }
        }

        onSubmitChange(selectedOption, dynamicValues);
    }
</script>

<div class="optimizer-variables-editor">
    <h2 style="color:orange">Change Hyperparameters</h2>

    <!-- Select lista -->
    <label for="select">Select an element:</label>
    <select id="select" bind:value={selectedOption} on:change={handleSelectionChange}>
        <option value={null} disabled selected>Select an option</option>
        {#each optimizerVars.keys() as key}
            <option value={key}>{key}</option>
        {/each}
    </select>

    <!-- Generowanie komponentów dynamicznych -->
    {#if selectedOptValue != null}
        {#if typeof selectedOptValue === "number"}
            <div>
                <label for="slider-float">{selectedOption}:</label>
                <input id="slider-float" type="range" min="0" max="1" step="0.01" bind:value={dynamicValues} />
                <input type="number" min="0" max="1" step="0.01" bind:value={dynamicValues} />
            </div>
        {:else if typeof selectedOptValue === "string"}
            <input type="text" bind:value={dynamicValues} placeholder="Enter a string" />
        {:else if typeof selectedOptValue === "boolean"}
            <label>
                <input type="checkbox" bind:checked={dynamicValues} />
                {selectedOption}
            </label>
        {:else if typeof selectedOptValue === "object"}
            {#each dynamicValues as value, index}
                <div>
                    <label for={`slider-list-float-${index}`}>{selectedOption} {index + 1}:</label>
                    <input id={`slider-list-float-${index}`} type="range" min="0" max="1" step="0.01" bind:value={dynamicValues[index]} />
                    <input type="number" min="0" max="1" step="0.01" bind:value={dynamicValues[index]} />
                </div>
            {/each}
        {/if}
        <button on:click={handleSubmit}>Submit</button>
    {/if}
</div>

<style>
    select {
        margin-top: 10px;
        padding: 5px;
        font-size: 16px;
    }
    input[type="range"] {
        margin-top: 10px;
        width: 100%;
    }

    input[type="number"] {
        padding: 8px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        width: 100%;
        transition:
            border-color 0.3s ease,
            box-shadow 0.3s ease;
        background-color: #282323;
    }

    input[type="number"]:focus {
        outline: none;
        border-color: #99c8ff;
        box-shadow: 0 0 4px rgba(85, 114, 181, 0.6);
    }

    .optimizer-variables-editor {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>
