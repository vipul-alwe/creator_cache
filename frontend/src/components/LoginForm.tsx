import React, { useState } from "react";

interface LoginFormProps {
  setIsSignup: (isSignup: boolean) => void;
  onLoginSuccess: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ setIsSignup, onLoginSuccess }) => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Login form submitted");

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!response.ok) {
        console.error("Failed to log in:", response.statusText);
        alert(`Login failed: ${response.statusText}`);
        return;
      }

      const data = await response.json();
      console.log("Response data:", data);

      if (data.success) {
        console.log("Login successful!");
        onLoginSuccess();  // Trigger the success callback
      } else {
        alert(data.message || "Login failed.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("Error connecting to the server. Please try again later.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <div>
        <label>Email ID:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Login</button>
      <p>
        New user?{" "}
        <a href="#" onClick={() => setIsSignup(true)}>
          Sign Up
        </a>
      </p>
    </form>
  );
};

export default LoginForm;
