import { createRouter, createWebHistory } from "vue-router"
import SearchView from "../views/SearchView.vue"
import ResultsView from "../views/ResultsView.vue"
import AuthView from "../views/AuthView.vue"
import FavoritesView from "../views/FavoritesView.vue"
import VerifyEmailView from "../views/VerifyEmailView.vue"
import TermsView from "../views/TermsView.vue"
import PrivacyView from "../views/PrivacyView.vue"
import { auth } from "../services/Auth"

const routes = [
    { path: "/", component: SearchView },
    { path: "/results", component: ResultsView },
    { path: "/login", component: AuthView },
    { path: "/register", component: AuthView },
    { path: "/verify-email", component: VerifyEmailView },
    { path: "/terms", component: TermsView },
    { path: "/privacy", component: PrivacyView },
    { path: "/favorites", component: FavoritesView, meta: { requiresAuth: true } }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !auth.token) {
    return { path: "/login", query: { redirect: to.fullPath } }
  }
})