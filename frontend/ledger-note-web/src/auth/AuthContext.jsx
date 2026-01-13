import React, { createContext, useContext, useEffect, useState } from "react";
import { api, setAuthToken } from "../api/client";

// Context = “全局共享状态的容器”
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // 初始 token 从 localStorage 里取（刷新页面不丢）
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  // token 变化时：同步到 axios header + localStorage
  useEffect(() => {
    setAuthToken(token);
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  async function login(email, password) {
    // ⚠️这里的 endpoint 可能要按你后端实际路径改
    const res = await api.post("/auth/login", { email, password });

    // 常见返回：{ access_token: "..." }
    const t = res.data.access_token ?? res.data.token;
    setToken(t);
  }

  function logout() {
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
