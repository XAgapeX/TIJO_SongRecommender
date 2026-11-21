<template>
  <div class="container">
    <div class="app-icon">
      <img src="/sound.png" width="512" height="512" alt="SongRecommender" />
    </div>
    <button class="back-btn" @click="router.push('/')">← Back</button>
    <h1 class="title">Song Recommender</h1>

    <div class="results-grid" v-if="recommendedSongs.length > 0">
      <div v-for="song in recommendedSongs" :key="song.track_id" class="song-item">
        <div class="cover">
          <SongTrial :song="song" />
          <button
            v-if="auth.user"
            class="favorite-btn"
            :class="{ active: favoriteIds.includes(song.track_id) }"
            :title="favoriteIds.includes(song.track_id) ? 'Usuń z ulubionych' : 'Dodaj do ulubionych'"
            @click="toggleFavorite(song.track_id)"
          >♥</button>
        </div>
        <div class="song-info">
          <p class="song-title">{{ song.track_name }}</p>
          <p class="song-artist">{{ song.artists }}</p>
        </div>
      </div>
    </div>

    <div v-else class="loading-state">
      <p>Finding the best songs for you...</p>
    </div>

    <p class="description">
      These are the songs chosen for you.<br />
      Enjoy listening!
    </p>

    <div class="footer">
      <img src="/src/assets/spotify_logo.png" alt="Spotify" />
      <span>Powered by Spotify</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import SongTrial from "../components/SongTrial.vue"
import { BASE_URL } from "../utils/Config"
import { auth, authHeaders } from "../services/Auth"

const router = useRouter()
const recommendedSongs = ref([])
const favoriteIds = ref([])

async function toggleFavorite(trackId) {
  if (!auth.token) return
  const isFavorite = favoriteIds.value.includes(trackId)
  const response = await fetch(
    `${BASE_URL}/auth/favorites${isFavorite ? `/${encodeURIComponent(trackId)}` : ""}`,
    {
      method: isFavorite ? "DELETE" : "POST",
      headers: {
        ...authHeaders(),
        "Content-Type": "application/json"
      },
      body: isFavorite ? undefined : JSON.stringify({ track_id: trackId })
    }
  )
  if (response.ok) {
    favoriteIds.value = isFavorite
      ? favoriteIds.value.filter(id => id !== trackId)
      : [...favoriteIds.value, trackId]
  }
}

async function loadFavorites() {
  if (!auth.token) {
    favoriteIds.value = []
    return
  }
  const response = await fetch(`${BASE_URL}/auth/favorites`, { headers: authHeaders() })
  if (response.ok) {
    const songs = await response.json()
    favoriteIds.value = songs.map(song => song.track_id)
  }
}

onMounted(() => {
  if (history.state && history.state.recommendations) {
    recommendedSongs.value = history.state.recommendations
  } else {
    router.push('/')
  }
  loadFavorites()
})
</script>

<style scoped>
.container {
  position: relative;
  min-height: 100vh;
  background: radial-gradient(circle, #3a3a3a, #1f1f1f);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  gap: 25px;
  color: white;
  text-align: center;
  box-sizing: border-box;
}

.app-icon {
  height: 80px;
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-icon img {
  width: 150%;
  height: 150%;
  object-fit: contain;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.title {
  font-size: 36px;
  margin: 0;
}

.results-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
  max-width: 1200px;
  margin: 20px 0;
}

.song-item {
  width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cover {
  position: relative;
  width: 100%;
}

.favorite-btn {
  position: absolute;
  right: -10px;
  bottom: -10px;
  width: 40px;
  height: 40px;
  border: 2px solid #222;
  border-radius: 50%;
  background: #555;
  color: #ddd;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,.5);
}

.favorite-btn.active {
  background: #1DB954;
  color: white;
}

.song-info {
  margin-top: 12px;
  width: 100%;
}

.song-title {
  font-size: 15px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.song-artist {
  font-size: 13px;
  color: #aaa;
  margin: 4px 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.description {
  font-size: 18px;
  color: #ccc;
}

.loading-state {
  min-height: 200px;
  display: flex;
  align-items: center;
}

.footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.5;
}

.footer img {
  width: 24px;
}
</style>
