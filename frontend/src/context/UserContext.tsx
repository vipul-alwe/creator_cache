import React, { createContext, useState, useContext, ReactNode } from "react";

interface UserContextType {
  loggedIn: boolean;
  setLoggedIn: (loggedIn: boolean) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <UserContext.Provider value={{ loggedIn, setLoggedIn }}>
      {children}
    </UserContext.Provider>
  );
};

// Custom hook to use the UserContext
export const useUserContext = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUserContext must be used within a UserProvider");
  }
  return context;
};
