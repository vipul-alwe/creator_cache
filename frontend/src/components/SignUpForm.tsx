import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SignUpForm.css";

const teamOptions = ["Management", "Client Servicing", "Media & Analytics"];

interface SignupFormProps {
  setIsSignup: (isSignup: boolean) => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ setIsSignup }) => {
  const [fullName, setFullName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [teamName, setTeamName] = useState<string>("");

  const [errors, setErrors] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    teamName: "",
  });

  const navigate = useNavigate(); // hook for navigating to a new page

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    let isValid = true;
    const newErrors = { ...errors };

    // Full Name validation
    newErrors.fullName = fullName ? "" : "Full Name is required";
    if (!fullName) isValid = false;

    // Email validation
    newErrors.email = email
      ? validateEmail(email)
        ? ""
        : "Invalid email format"
      : "Email is required";
    if (!email || !validateEmail(email)) isValid = false;

    // Password validation
    newErrors.password = password ? "" : "Password is required";
    if (!password) isValid = false;

    // Confirm Password validation
    newErrors.confirmPassword = confirmPassword
      ? confirmPassword === password
        ? ""
        : "Passwords do not match"
      : "Confirm Password is required";
    if (!confirmPassword || confirmPassword !== password) isValid = false;

    // Team Name validation
    newErrors.teamName = teamName ? "" : "Please select a team";
    if (!teamName) isValid = false;

    setErrors(newErrors);

    if (isValid) {
      try {
        const timestamp = new Date().toISOString(); // Generate timestamp

        const response = await fetch("http://localhost:8000/signup/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            full_name: fullName, // Changed 'fullName' to 'full_name' to match backend
            email,
            password,
            team_name: teamName, // Changed 'teamName' to 'team_name' to match backend
            ts: timestamp, // Added timestamp field 'ts'
          }),
        });

        if (!response.ok) {
          console.error("Failed to sign up:", response.statusText);
          alert(`Signup failed: ${response.statusText}`);
          return;
        }

        const data = await response.json();
        console.log("Response data:", data);

        if (data.success) {
          alert("Signup successful!");
          setIsSignup(false); // If successful, switch to login screen
          navigate("/welcome"); // Navigate to the welcome page
        } else {
          alert(data.message || "Signup failed.");
        }
      } catch (error) {
        console.error("Error during signup:", error);
        alert("Error connecting to the server. Please try again later.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign Up</h2>
      <div>
        <label>Full Name:</label>
        <input
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
        {errors.fullName && <p className="error">{errors.fullName}</p>}
      </div>
      <div>
        <label>Email ID:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {errors.email && <p className="error">{errors.email}</p>}
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {errors.password && <p className="error">{errors.password}</p>}
      </div>
      <div>
        <label>Confirm Password:</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        {errors.confirmPassword && (
          <p className="error">{errors.confirmPassword}</p>
        )}
      </div>
      <div>
        <label>Team Name:</label>
        <select
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          required
        >
          <option value="">Select Team</option>
          {teamOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        {errors.teamName && <p className="error">{errors.teamName}</p>}
      </div>
      <button type="submit">Sign Up</button>
      <p>
        Already a user?{" "}
        <a href="#" onClick={() => setIsSignup(false)}>
          Login
        </a>
      </p>
    </form>
  );
};

export default SignupForm;
