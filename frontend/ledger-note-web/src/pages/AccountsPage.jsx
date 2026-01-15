import { useEffect, useState } from "react";
import { listAccounts, createAccount } from "../api/accounts";

export default function AccountsPage() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [name, setName] = useState("");
  const [type, setType] = useState("ASSET");
  const [currency, setCurrency] = useState("CAD");
  const [subtype, setSubtype] = useState("");

  async function refresh() {
    setLoading(true);
    setErr(null);
    try {
      const data = await listAccounts();
      setAccounts(data);
    } catch (e) {
      setErr(e?.response?.data?.detail ?? "Failed to load accounts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onCreate(e) {
    e.preventDefault();
    setErr(null);
    try {
      await createAccount({
        name,
        type,
        subtype: subtype || null,
        currency,
        parent_id: null,
      });
      setName("");
      setSubtype("");
      await refresh();
    } catch (e) {
      setErr(e?.response?.data?.detail ?? "Failed to create account");
    }
  }

  return (
    <div >
      <h3>Accounts</h3>

      <form onSubmit={onCreate} style={{ display: "grid", gap: 8, maxWidth: 420 }}>
        <input
          placeholder="Account name (e.g., Cash)"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="ASSET">ASSET</option>
          <option value="LIABILITY">LIABILITY</option>
          <option value="EQUITY">EQUITY</option>
          <option value="INCOME">INCOME</option>
          <option value="EXPENSE">EXPENSE</option>
        </select>

        <input
          placeholder="Subtype (optional, e.g., BANK)"
          value={subtype}
          onChange={(e) => setSubtype(e.target.value)}
        />

        <input
          placeholder="Currency (e.g., CAD)"
          value={currency}
          onChange={(e) => setCurrency(e.target.value.toUpperCase())}
        />

        <button type="submit" disabled={!name.trim()}>
          Create account
        </button>
      </form>

      {err && <div style={{ color: "crimson", marginTop: 10 }}>{String(err)}</div>}
      {loading && <div style={{ marginTop: 10 }}>Loading...</div>}

      {!loading && (
        <table style={{ width: "100%", marginTop: 16, borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">ID</th>
              <th align="left">Name</th>
              <th align="left">Type</th>
              <th align="left">Currency</th>
              <th align="left">Active</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((a) => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.name}</td>
                <td>{a.type}</td>
                <td>{a.currency}</td>
                <td>{String(a.is_active)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
