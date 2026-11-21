<template>
  <main class="legal-page">
    <section class="legal-card">
      <button class="back-btn" @click="router.back()">← Wstecz</button>
      <h1>Regulamin</h1>
      <p>Korzystając z aplikacji Song Recommender, zobowiązujesz się do korzystania z serwisu zgodnie z prawem i zasadami użytkowania.</p>
      <p>Nie możesz wykorzystywać konta do działania na szkodę innych użytkowników ani celów niezgodnych z przeznaczeniem serwisu.</p>
    </section>
  </main>
</template>
<script setup>
import { useRouter } from "vue-router"
const router = useRouter()
</script>
<style scoped>
.legal-page { min-height:100vh; display:flex; align-items:center; justify-content:center; background:radial-gradient(circle,#3a3a3a,#1f1f1f); color:white; }
.legal-card { position:relative; width:min(620px,calc(100vw - 40px)); box-sizing:border-box; background:#262626; border:1px solid #444; border-radius:18px; padding:32px; }
.back-btn { position:absolute; top:-50px; left:0; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:white; padding:8px 16px; border-radius:20px; cursor:pointer; }
</style>
