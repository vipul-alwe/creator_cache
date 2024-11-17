<template>
    <div class="welcome-container">
      <h1>Welcome, {{ userEmail }}!</h1>
      <p>You have successfully logged in.</p>
      <router-link to="/login">Logout</router-link>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from "vue";
  import { useRouter } from "vue-router";
  
  export default defineComponent({
    name: "WelcomePage",
    setup() {
      const router = useRouter();
      const userEmail = ref("");
  
      onMounted(() => {
        // Check if token is available in localStorage
        const token = localStorage.getItem("token");
        if (!token) {
          // Redirect to login page if not logged in
          router.push("/login");
        } else {
          // If logged in, set the user email (example)
          userEmail.value = "user@example.com"; // Use actual user data from backend if needed
        }
      });
  
      return {
        userEmail,
      };
    },
  });
  </script>
  
  <style scoped>
  .welcome-container {
    text-align: center;
    margin-top: 2rem;
  }
  
  h1 {
    font-size: 2rem;
    color: #333;
  }
  
  router-link {
    text-decoration: none;
    color: #007bff;
    font-size: 1rem;
  }
  </style>
  