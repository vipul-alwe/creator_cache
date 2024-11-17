import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../components/LoginPage.vue";
import WelcomePage from "../components/WelcomePage.vue";
import SignupPage from "../components/SignUpForm.vue"; // Assuming it's in the same folder

const routes = [
  { path: "/login", component: LoginPage },
  { path: "/welcome", component: WelcomePage },
  { path: "/signup", component: SignupPage },
  { path: "/", redirect: "/login" }, // Redirect to login by default
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
