import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function LoginPage() {
  const nav = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setErr(null);
    try {
      await login(email, password);
      nav("/accounts");
    } catch (e) {
      setErr(e?.response?.data?.detail ?? "Login failed");
    }
  }

  return (
    <div style={{ maxWidth: 360 }}>
      <h3>Login</h3>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 8 }}>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Sign in</button>
        {err && <div style={{ color: "crimson" }}>{err}</div>}
      </form>
    </div>
  );
}
