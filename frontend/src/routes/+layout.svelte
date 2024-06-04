<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';

  let isAuthenticated = writable(false);

  onMount(() => {
    // 초기 로그인 상태 확인
    isAuthenticated.set(localStorage.getItem('authenticated') === 'true');

    // 페이지 로딩 후 클라이언트에서 네비게이션 처리
    if (window.location.pathname !== '/login' && !localStorage.getItem('authenticated')) {
      goto('/login');
    }
  });

  function handleLogout() {
    localStorage.removeItem('authenticated');
    isAuthenticated.set(false);
    goto('/login');
  }
</script>

<main>
  <nav>
    <button on:click={() => goto('/')}>로고</button>
    <button on:click={() => goto('/menu01')}>메뉴01</button>
    <button on:click={() => goto('/menu02')}>메뉴02</button>
    <button on:click={() => goto('/menu03')}>메뉴03</button>
    {#if $isAuthenticated}
      <button on:click={handleLogout}>로그아웃</button>
    {:else}
      <button on:click={() => goto('/login')}>로그인 / 회원가입</button>
    {/if}
  </nav>
  <slot />
</main>

<style>
  nav {
    display: flex;
    gap: 1rem;
    background-color: #f0f0f0;
    padding: 1rem;
  }

  button {
    background-color: #e0e0e0;
    border: none;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }

  main {
    background-color: lavender;
    min-height: 100vh;
  }
</style>
