<script lang="ts">
  import { goto } from '$app/navigation';
</script>

<button class="logo" on:click={() => goto('/home')}>
  로고
</button>

<style>
  .logo {
    font-size: 1.5rem;
    font-weight: bold;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
    color: inherit;
  }
</style>
