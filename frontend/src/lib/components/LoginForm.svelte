<script>
    import { createEventDispatcher } from 'svelte';
    import { goto } from '$app/navigation';
  
    const dispatch = createEventDispatcher();
  
    function handleLogin() {
      // 여기에 실제 로그인 로직을 추가합니다.
      localStorage.setItem('authenticated', 'true');
      dispatch('login');
      goto('/home');
    }
  </script>
  
  <div>
    <h2>로그인</h2>
    <button on:click={handleLogin}>Start with Google</button>
  </div>
  
  <style>
    div {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  
    button {
      padding: 1rem 2rem;
      font-size: 1.5rem;
      background-color: #4285f4;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  </style>
  