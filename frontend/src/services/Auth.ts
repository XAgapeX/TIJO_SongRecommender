import { reactive } from "vue"
import { BASE_URL } from "../utils/Config"

export interface AuthUser {
  id: number
  username: string | null
  email: string
}

const saved = localStorage.getItem("song_recommender_auth")
const initial = saved ? JSON.parse(saved) : null

export const auth = reactive({
  token: initial?.token as string | null,
  user: initial?.user as AuthUser | null
})

function save() {
  localStorage.setItem("song_recommender_auth", JSON.stringify({
    token: auth.token,
    user: auth.user
  }))
}

async function authRequest(path: string, username: string, password: string) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: username, password })
  })

  const data = await response.json()
  if (!response.ok) throw new Error(data.detail || "Operacja nie powiodła się")

  auth.token = data.token
  auth.user = data.user
  save()
  return data
}

export function login(email: string, password: string) {
  return authRequest("/auth/login", email, password)
}

export async function register(payload: {
  email: string
  username?: string
  password: string
  passwordConfirm: string
  termsAccepted: boolean
  marketingConsent: boolean
}) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: payload.email,
      username: payload.username || null,
      password: payload.password,
      password_confirm: payload.passwordConfirm,
      terms_accepted: payload.termsAccepted,
      marketing_consent: payload.marketingConsent,
      website: ""
    })
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.detail || "Nie udało się utworzyć konta")
  return data as { message: string; verification_url: string | null }
}

export async function logout() {
  if (auth.token) {
    await fetch(`${BASE_URL}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${auth.token}` }
    }).catch(() => {})
  }
  auth.token = null
  auth.user = null
  localStorage.removeItem("song_recommender_auth")
}

export function authHeaders() {
  return auth.token ? { Authorization: `Bearer ${auth.token}` } : {}
}
