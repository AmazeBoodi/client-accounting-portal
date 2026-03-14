"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiGet, clearToken, getToken } from "@/lib/api";

type Me = { id:number; email:string; name:string; role:string; client_id:number|null };

export function Navbar() {
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    const t = getToken();
    if (!t) return;
    apiGet("/auth/me").then(setMe).catch(() => setMe(null));
  }, []);

  return (
    <div className="nav">
      <Link href="/" style={{fontWeight:700}}>Portal</Link>
      <span className="small">|</span>
      {!me ? (
        <Link href="/login">Login</Link>
      ) : (
        <>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/expenses">Expenses</Link>
          <Link href="/income">Income</Link>
          <Link href="/invoices">Invoices</Link>
          {me.role === "admin" && <Link href="/admin">Admin</Link>}
          <span style={{marginLeft:"auto"}} className="small">{me.name} ({me.role})</span>
          <button onClick={() => { clearToken(); location.href="/login"; }}>Logout</button>
        </>
      )}
    </div>
  );
}
