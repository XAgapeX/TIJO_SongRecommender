<template>
  <nav v-if="$route.path !== '/login' && $route.path !== '/register'" class="top-nav">
    <RouterLink to="/" class="brand">Song Recommender</RouterLink>
    <div class="nav-actions">
      <template v-if="auth.user">
        <RouterLink to="/favorites" class="nav-link">Ulubione</RouterLink>
        <span class="username">{{ auth.user.username }}</span>
        <button @click="handleLogout">Wyloguj</button>
      </template>
      <template v-else>
        <RouterLink to="/login" class="nav-link">Zaloguj się</RouterLink>
        <RouterLink to="/register" class="nav-link register">Rejestracja</RouterLink>
      </template>
    </div>
  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from "vue-router"
import { auth, logout } from "./services/Auth"

const router = useRouter()

async function handleLogout() {
  await logout()
  router.push("/")
}
</script>

<style scoped>
.top-nav { position:absolute; z-index:100; top:0; left:0; right:0; height:56px; box-sizing:border-box; display:flex; align-items:center; justify-content:space-between; padding:0 24px; color:white; background:rgba(20,20,20,.72); backdrop-filter:blur(10px); border-bottom:1px solid rgba(255,255,255,.08); }
.brand { color:white; text-decoration:none; font-weight:bold; }
.nav-actions { display:flex; align-items:center; gap:12px; }
.nav-link { color:#ddd; text-decoration:none; }
.nav-link.register { background:#1DB954; color:white; padding:8px 14px; border-radius:18px; }
.username { color:#aaa; font-size:14px; }
button { border:1px solid #555; border-radius:18px; background:transparent; color:white; padding:8px 14px; cursor:pointer; }
</style>
