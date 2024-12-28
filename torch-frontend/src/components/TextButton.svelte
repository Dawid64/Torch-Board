<script lang="ts">
    let texts: string[] = ['cat', 'dog', 'horse'];
    let currentIdx: number = 0;
  
    function changeText(): void {
      currentIdx = (currentIdx + 1) % texts.length;
    }
  
    $: currentText = texts[currentIdx];
  </script>
  
  <style>
    button {
      padding: 12px 16px;
      font-size: 1rem;
      margin-left: 16px;
      cursor: pointer;
      background-color: #ccc;
      border: 1px solid #888;
      border-radius: 4px;
    }
  </style>
  
  <button on:click={changeText}>
    {currentText}
  </button>
  