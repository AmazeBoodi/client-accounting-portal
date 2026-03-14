"use client";

import { useState } from "react";
import { apiPost, setToken } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      const data = await apiPost("/auth/login", { email, password });
      setToken(data.access_token);
      location.href = "/dashboard";
    } catch (e: any) {
      setErr(e.message);
    }
  }

  return (
    <div className="card" style={{maxWidth:520}}>
      <h2>Login</h2>
      <p className="small">Use the admin created credentials.</p>
      <form onSubmit={onSubmit}>
        <div className="row">
          <div>
            <label className="small">Email</label>
            <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email@domain.com" />
          </div>
          <div>
            <label className="small">Password</label>
            <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="••••••••" />
          </div>
        </div>
        {err && <p className="small" style={{color:"#b91c1c"}}>{err}</p>}
        <button className="primary" type="submit">Login</button>
      </form>
    </div>
  );
}
