<template>
  <main class="favorites-page">
    <button class="back-btn" @click="router.push('/')">← Wstecz</button>
    <h1>Ulubione piosenki</h1>
    <p v-if="loading">Ładowanie...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <div v-else-if="songs.length" class="grid">
      <article v-for="song in songs" :key="song.track_id" class="song-item">
        <div class="cover">
          <SongTrial :song="song" />
          <button class="favorite active" title="Usuń z ulubionych" @click="removeFavorite(song.track_id)">♥</button>
        </div>
        <p class="title">{{ song.track_name }}</p>
        <p class="artist">{{ song.artists }}</p>
      </article>
    </div>
    <p v-else class="empty">Nie masz jeszcze ulubionych piosenek.</p>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import SongTrial from "../components/SongTrial.vue"
import { BASE_URL } from "../utils/Config"
import { authHeaders } from "../services/Auth"

const router = useRouter()
const songs = ref([])
const loading = ref(true)
const error = ref("")

async function load() {
  loading.value = true
  error.value = ""
  try {
    const response = await fetch(`${BASE_URL}/auth/favorites`, { headers: authHeaders() })
    if (!response.ok) throw new Error("Nie udało się pobrać ulubionych")
    const data = await response.json()
    songs.value = data.map(song => ({ ...song, img: `https://picsum.photos/seed/${song.track_id}/300` }))
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Wystąpił błąd"
  } finally {
    loading.value = false
  }
}

async function removeFavorite(trackId) {
  await fetch(`${BASE_URL}/auth/favorites/${encodeURIComponent(trackId)}`, {
    method: "DELETE",
    headers: authHeaders()
  })
  await load()
}

onMounted(load)
</script>

<style scoped>
.favorites-page { min-height:100vh; box-sizing:border-box; padding:70px 20px 40px; text-align:center; color:white; background:radial-gradient(circle,#3a3a3a,#1f1f1f); }
.back-btn { position:absolute; top:20px; left:20px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:white; padding:8px 16px; border-radius:20px; cursor:pointer; }
h1 { margin:20px 0 35px; }
.grid { display:flex; flex-wrap:wrap; justify-content:center; gap:30px; max-width:1100px; margin:auto; }
.song-item { width:160px; }
.cover { position:relative; }
.favorite { position:absolute; right:-10px; bottom:-10px; width:40px; height:40px; border-radius:50%; border:2px solid #222; background:#1DB954; color:white; font-size:20px; cursor:pointer; }
.title,.artist { width:100%; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.title { margin-top:12px; font-weight:bold; }
.artist { color:#aaa; font-size:13px; margin-top:4px; }
.empty,.error { color:#aaa; }
</style>
