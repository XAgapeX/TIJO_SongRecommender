<template>
  <main class="legal-page">
    <button class="back-btn" @click="router.push('/login')">← Do logowania</button>
    <section class="legal-card">
      <h1>Potwierdzanie adresu e-mail</h1>
      <p v-if="status">{{ status }}</p>
      <p v-else>Potwierdzanie...</p>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { BASE_URL } from "../utils/Config"

const route = useRoute()
const router = useRouter()
const status = ref("")

onMounted(async () => {
  const token = route.query.token
  if (typeof token !== "string") {
    status.value = "Brakuje tokenu potwierdzającego."
    return
  }
  try {
    const response = await fetch(`${BASE_URL}/auth/verify-email?token=${encodeURIComponent(token)}`, { method: "POST" })
    const data = await response.json()
    status.value = response.ok ? data.message : (data.detail || "Nie udało się potwierdzić adresu.")
  } catch {
    status.value = "Nie udało się połączyć z serwerem."
  }
})
</script>

<style scoped>
.legal-page { min-height:100vh; display:flex; align-items:center; justify-content:center; background:radial-gradient(circle,#3a3a3a,#1f1f1f); color:white; }
.legal-card { width:min(620px,calc(100vw - 40px)); box-sizing:border-box; background:#262626; border:1px solid #444; border-radius:18px; padding:32px; text-align:center; }
.back-btn { position:absolute; top:20px; left:20px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:white; padding:8px 16px; border-radius:20px; cursor:pointer; }
</style>
