"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    apiGet("/dashboard").then(setData).catch(e=>setErr(e.message));
  }, []);

  if (err) return <div className="card"><p style={{color:"#b91c1c"}}>{err}</p></div>;
  if (!data) return <div className="card">Loading...</div>;

  return (
    <div className="row">
      <div className="card">
        <div className="small">Income (this month)</div>
        <h2>{data.month_income}</h2>
      </div>
      <div className="card">
        <div className="small">Expenses (this month)</div>
        <h2>{data.month_expenses}</h2>
      </div>
      <div className="card">
        <div className="small">Outstanding invoices</div>
        <h2>{data.outstanding_invoices}</h2>
      </div>
      <div className="card">
        <div className="small">Overdue</div>
        <h2>{data.overdue_invoices_amount}</h2>
        <div className="small">{data.overdue_invoices_count} invoice(s)</div>
      </div>
    </div>
  );
}
