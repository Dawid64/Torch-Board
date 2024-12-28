<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let count: number = 0;
  let intervalId: number | undefined;

  // Funkcja inicjalizująca interwał
  function startCounter(): void {
    stopCounter(); // Na wszelki wypadek zatrzymujemy stary interwał
    intervalId = setInterval(() => {
      count += 1; // Reaktywnie zmieniamy wartość
    }, 1000);
  }

  // Funkcja zatrzymująca interwał
  function stopCounter(): void {
    if (intervalId !== undefined) {
      clearInterval(intervalId);
      intervalId = undefined;
    }
  }

  onMount(() => {
    startCounter(); // Uruchamiamy licznik po zamontowaniu

    // Zatrzymujemy licznik podczas odmontowywania komponentu
    return stopCounter;
  });

  // Możliwość zatrzymania licznika manualnie
  onDestroy(stopCounter);
</script>

<style>
  .counter {
    font-size: 1.2rem;
    padding: 8px;
    background-color: #f0f0f0;
    display: inline-block;
    border-radius: 4px;
    margin-top: 10px;
  }
  .controls {
    margin-top: 10px;
  }
  button {
    padding: 6px 12px;
    margin-right: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
</style>

<div class="counter">
  Current count: {count}
</div>

<div class="controls">
  <button on:click={startCounter}>Start</button>
  <button on:click={stopCounter}>Stop</button>
</div>
