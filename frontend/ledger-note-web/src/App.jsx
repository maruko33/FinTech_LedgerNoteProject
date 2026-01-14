import { Link, Route, Routes } from "react-router-dom";
import RequireAuth from "./auth/RequireAuth";

import LoginPage from "./pages/LoginPage.jsx";
import AccountsPage from "./pages/AccountsPage.jsx";
import EntriesPage from "./pages/EntriesPage.jsx";
import TrialBalancePage from "./pages/TrialBalancePage.jsx";
import { useAuth } from "./auth/AuthContext.jsx";

export default function App() {
  const { token, logout } = useAuth();

  return (
    <div style={{ maxWidth: 960, margin: "0 auto", padding: 16 }}>
      <header style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <h2 style={{ marginRight: "auto" }}>LedgerNote</h2>

        <nav style={{ display: "flex", gap: 10 }}>
          <Link to="/login">Login</Link>
          <Link to="/accounts">Accounts</Link>
          <Link to="/entries">Entries</Link>
          <Link to="/reports/trial-balance">Trial Balance</Link>
        </nav>

        {token ? <button onClick={logout}>Logout</button> : <span>Guest</span>}
      </header>

      <hr style={{ margin: "16px 0" }} />

      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/accounts"
          element={
            <RequireAuth>
              <AccountsPage />
            </RequireAuth>
          }
        />

        <Route
          path="/entries"
          element={
            <RequireAuth>
              <EntriesPage />
            </RequireAuth>
          }
        />

        <Route
          path="/reports/trial-balance"
          element={
            <RequireAuth>
              <TrialBalancePage />
            </RequireAuth>
          }
        />

        <Route path="*" element={<div>Not Found</div>} />
      </Routes>
    </div>
  );
}
