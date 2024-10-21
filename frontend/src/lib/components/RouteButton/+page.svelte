<script lang="ts">
  import { goto } from '$app/navigation';

  export let route: string;
  export let label: string;
</script>

<button on:click={() => goto(route)}>
  {label}
</button>

<style>
  button {
    background-color: #e0e0e0;
    border: none;
    padding: 0.5rem 1rem;
    cursor: pointer;
    margin: 0 0.5rem;
  }
</style>

