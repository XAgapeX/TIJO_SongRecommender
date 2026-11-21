<template>
  <main class="auth-page">
    <button class="back-btn" @click="router.push('/')">← Wstecz</button>
    <form class="auth-card" @submit.prevent="submit">
      <img src="/sound.png" alt="SongRecommender" />
      <h1>{{ isRegister ? "Rejestracja" : "Logowanie" }}</h1>

      <label>
        Adres e-mail
        <input v-model.trim="email" type="email" maxlength="254" required autocomplete="email" @blur="validateEmail" />
        <span v-if="emailError" class="field-error">{{ emailError }}</span>
      </label>
      <label v-if="isRegister">
        Nazwa użytkownika <span class="optional">(opcjonalnie)</span>
        <input v-model.trim="username" type="text" maxlength="50" autocomplete="nickname" />
      </label>
      <label>
        Hasło
        <div class="password-field">
          <input v-model="password" :type="showPassword ? 'text' : 'password'" minlength="8" maxlength="128" required :autocomplete="isRegister ? 'new-password' : 'current-password'" />
          <button type="button" @click="showPassword = !showPassword">{{ showPassword ? "Ukryj" : "Pokaż" }}</button>
        </div>
      </label>
      <div v-if="isRegister" class="requirements">
        <span :class="{ met: password.length >= 8 }">Co najmniej 8 znaków</span>
        <span :class="{ met: /[a-z]/.test(password) && /[A-Z]/.test(password) }">Mała i wielka litera</span>
        <span :class="{ met: /\d/.test(password) }">Co najmniej jedna cyfra</span>
      </div>
      <label v-if="isRegister">
        Powtórz hasło
        <div class="password-field">
          <input v-model="passwordConfirm" :type="showConfirm ? 'text' : 'password'" minlength="8" maxlength="128" required autocomplete="new-password" />
          <button type="button" @click="showConfirm = !showConfirm">{{ showConfirm ? "Ukryj" : "Pokaż" }}</button>
        </div>
        <span v-if="passwordConfirm && passwordConfirm !== password" class="field-error">Hasła muszą być identyczne</span>
      </label>
      <label v-if="isRegister" class="checkbox">
        <input v-model="termsAccepted" type="checkbox" required />
        <span>Akceptuję <RouterLink to="/terms">regulamin</RouterLink> i <RouterLink to="/privacy">politykę prywatności</RouterLink>.</span>
      </label>
      <label v-if="isRegister" class="checkbox">
        <input v-model="marketingConsent" type="checkbox" />
        <span>Chcę otrzymywać informacje marketingowe (opcjonalnie).</span>
      </label>
      <div v-if="registrationComplete" class="success">
        <p>{{ registrationMessage }}</p>
        <a v-if="verificationUrl" :href="verificationUrl" class="verify-link">Potwierdź adres e-mail</a>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <button class="primary" type="submit" :disabled="busy">
        {{ busy ? "Proszę czekać..." : (isRegister ? "Załóż konto" : "Zaloguj się") }}
      </button>
      <button class="switch" type="button" @click="router.push(isRegister ? '/login' : '/register')">
        {{ isRegister ? "Masz już konto? Zaloguj się" : "Nie masz konta? Zarejestruj się" }}
      </button>
    </form>
  </main>
</template>

<script setup>
import { computed, ref, watch } from "vue"
import { RouterLink, useRoute, useRouter } from "vue-router"
import { login, register } from "../services/Auth"

const route = useRoute()
const router = useRouter()
const username = ref("")
const email = ref("")
const emailError = ref("")
const password = ref("")
const passwordConfirm = ref("")
const showPassword = ref(false)
const showConfirm = ref(false)
const termsAccepted = ref(false)
const marketingConsent = ref(false)
const registrationComplete = ref(false)
const registrationMessage = ref("")
const verificationUrl = ref(null)
const error = ref("")
const busy = ref(false)
const isRegister = computed(() => route.path === "/register")

watch(() => route.path, () => {
  error.value = ""
  password.value = ""
  passwordConfirm.value = ""
  registrationComplete.value = false
})

const validateEmail = () => {
  emailError.value = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
    ? ""
    : "Niepoprawny adres e-mail"
}

const submit = async () => {
  busy.value = true
  error.value = ""
  validateEmail()
  if (emailError.value) {
    busy.value = false
    return
  }
  try {
    if (isRegister.value) {
      if (password.value !== passwordConfirm.value) {
        error.value = "Hasła muszą być identyczne"
        return
      }
      if (!termsAccepted.value) {
        error.value = "Musisz zaakceptować regulamin i politykę prywatności"
        return
      }
      const result = await register({
        email: email.value,
        username: username.value,
        password: password.value,
        passwordConfirm: passwordConfirm.value,
        termsAccepted: termsAccepted.value,
        marketingConsent: marketingConsent.value
      })
      registrationComplete.value = true
      registrationMessage.value = result.message
      verificationUrl.value = result.verification_url
    } else {
      await login(email.value, password.value)
      router.push(typeof route.query.redirect === "string" ? route.query.redirect : "/")
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Wystąpił błąd"
  } finally {
    busy.value = false
  }
}
</script>

<style scoped>
.auth-page { min-height:100vh; display:flex; align-items:center; justify-content:center; background:radial-gradient(circle,#3a3a3a,#1f1f1f); color:white; }
.auth-card { width:min(420px,calc(100vw - 40px)); box-sizing:border-box; background:#262626; border:1px solid #444; border-radius:18px; padding:32px; display:flex; flex-direction:column; gap:16px; box-shadow:0 20px 50px rgba(0,0,0,.35); }
.auth-card img { width:72px; height:72px; margin:auto; object-fit:contain; }
h1 { margin:0 0 8px; text-align:center; }
label { display:flex; flex-direction:column; gap:8px; text-align:left; color:#ddd; }
input { box-sizing:border-box; width:100%; border:1px solid #555; border-radius:10px; background:#333; color:white; padding:12px 14px; outline:none; }
input:focus { border-color:#1DB954; }
.primary { border:none; border-radius:24px; background:#1DB954; color:white; padding:13px; font-size:16px; font-weight:bold; cursor:pointer; }
.primary:disabled { opacity:.6; cursor:not-allowed; }
.switch { border:none; background:none; color:#bbb; cursor:pointer; }
.error { margin:0; color:#ff7777; }
.field-error { color:#ff7777; font-size:13px; }
.optional { color:#999; font-size:13px; }
.password-field { display:flex; gap:8px; }
.password-field input { flex:1; }
.password-field button { border:1px solid #555; border-radius:10px; background:#333; color:#ddd; cursor:pointer; }
.requirements { display:flex; flex-wrap:wrap; gap:6px; }
.requirements span { font-size:12px; color:#999; border:1px solid #555; border-radius:12px; padding:4px 8px; }
.requirements span.met { color:#b6f5c9; border-color:#1DB954; }
.checkbox { flex-direction:row; align-items:flex-start; gap:10px; font-size:14px; }
.checkbox input { width:auto; margin-top:3px; }
.checkbox a { color:#1ed760; }
.success { border:1px solid #1DB954; border-radius:10px; background:rgba(29,185,84,.12); padding:12px; }
.verify-link { color:#1ed760; font-weight:bold; }
.back-btn { position:absolute; top:20px; left:20px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2); color:white; padding:8px 16px; border-radius:20px; cursor:pointer; }
</style>
