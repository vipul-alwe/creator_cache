<template>
  <div class="signup-container">
    <h1>Signup</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="fullName">Full Name</label>
        <input
          id="fullName"
          v-model="form.full_name"
          type="text"
          placeholder="Enter your full name"
          required
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          placeholder="Enter your email"
          @blur="validateEmail"
          required
        />
        <p v-if="emailError" class="error-text">{{ emailError }}</p>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          placeholder="Enter your password"
          required
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm your password"
          @blur="checkPasswordsMatch"
          required
        />
        <p v-if="passwordError" class="error-text">{{ passwordError }}</p>
      </div>

      <div class="form-group">
        <label for="teamName">Team Name</label>
        <select id="teamName" v-model="form.team_name" required>
          <option value="" disabled>Select your team</option>
          <option value="Management">Management</option>
          <option value="Client Servicing">Client Servicing</option>
          <option value="Media and Analytics">Media and Analytics</option>
        </select>
      </div>

      <button type="submit" :disabled="!isFormValid">Signup</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, computed } from "vue";

export default defineComponent({
  name: "SignupForm",
  setup() {
    const form = reactive({
      full_name: "",  // Updated to match backend field
      email: "",
      password: "",
      team_name: "",  // Updated to match backend field
      ts: "", // Timestamp field
    });

    const confirmPassword = ref("");
    const emailError = ref("");
    const passwordError = ref("");

    const validateEmail = () => {
      const emailPattern =
        /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      if (!emailPattern.test(form.email)) {
        emailError.value = "Please enter a valid email address.";
      } else {
        emailError.value = "";
      }
    };

    const checkPasswordsMatch = () => {
      if (form.password !== confirmPassword.value) {
        passwordError.value = "Passwords do not match.";
      } else {
        passwordError.value = "";
      }
    };

    const isFormValid = computed(() => {
      return (
        form.full_name &&  // Updated to match backend field
        form.email &&
        form.password &&
        confirmPassword.value &&
        !emailError.value &&
        !passwordError.value &&
        form.team_name  // Updated to match backend field
      );
    });

    const handleSubmit = () => {
      // Add the current timestamp to the form
      form.ts = new Date().toISOString();

      // Send form data to the Flask backend using fetch
      fetch("http://localhost:5000/signup", { // Flask backend URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      })
        .then(response => response.json())
        .then(data => {
          console.log("Server response:", data);
          // Handle success (e.g., show a success message or redirect)
        })
        .catch(error => {
          console.error("Error:", error);
          // Handle error (e.g., show an error message)
        });
    };

    return {
      form,
      confirmPassword,
      emailError,
      passwordError,
      validateEmail,
      checkPasswordsMatch,
      isFormValid,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input,
select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error-text {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.3rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
