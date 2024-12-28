<script lang="ts">
    let colors: string[] = ['pink', 'red', 'blue'];
    let currentIndex: number = 0;
  
    function changeColor(): void {
      currentIndex = (currentIndex + 1) % colors.length;
    }
  
    $: currentColor = colors[currentIndex];
  </script>
  
  <style>
    button {
      padding: 12px 16px;
      font-size: 1rem;
      border: none;
      cursor: pointer;
      color: white;
      border-radius: 4px;
    }
  </style>
  
  <button on:click={changeColor} style="background-color: {currentColor}">
    Click me
  </button>
  