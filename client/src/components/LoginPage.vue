<template>
    <div class="login-form">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>
  
        <div class="form-group">
          <input
            type="checkbox"
            id="remember"
            v-model="remember"
          />
          <label for="remember">Remember Me</label>
        </div>
  
        <button type="submit">Login</button>
  
        <div class="signup-link">
          <p>New here? <router-link to="/signup">Create an account</router-link></p>
        </div>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  export default {
    name: "LoginPage",
    setup() {
      const router = useRouter();
  
      // Form data binding
      const email = ref("");
      const password = ref("");
      const remember = ref(false);
  
      // Handle form submission
      const handleLogin = async () => {
        const loginData = { email: email.value, password: password.value };
        
        try {
          const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(loginData),  // Send the correct JSON
          });
  
          if (response.ok) {
            const data = await response.json();
            if (data.success) {
              // Handle successful login (e.g., navigate to the welcome page)
              router.push("/welcome");
            } else {
              alert(data.message || "Invalid email or password.");
            }
          } else {
            alert("Error logging in.");
          }
        } catch (error) {
          console.error("Error:", error);
          alert("Error logging in.");
        }
      };
  
      return {
        email,
        password,
        remember,
        handleLogin,
      };
    },
  };
  </script>
  
  <style scoped>
  .login-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  input[type="checkbox"] {
    margin-right: 10px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .signup-link {
    text-align: center;
    margin-top: 20px;
  }
  
  .signup-link a {
    color: #4CAF50;
  }
  </style>
  