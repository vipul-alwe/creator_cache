// utils/auth.ts

// Function to get the token from localStorage or cookies
export const getToken = (): string | null => {
    return localStorage.getItem("authToken"); // Or use a cookie here
  };
  
  // Function to set the token
  export const setToken = (token: string): void => {
    localStorage.setItem("authToken", token); // Store token in localStorage
  };
  
  // Function to remove the token
  export const removeToken = (): void => {
    localStorage.removeItem("authToken"); // Remove token from localStorage
  };
  