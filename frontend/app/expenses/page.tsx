"use client";

import { useEffect, useState } from "react";
import { apiGet, apiPost, apiUpload } from "@/lib/api";

type Cat = { id:number; name:string };
type Expense = { id:number; date:string; amount:number; payment_method:string; category_id:number; notes?:string; attachment_path?:string };

export default function ExpensesPage() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [items, setItems] = useState<Expense[]>([]);
  const [form, setForm] = useState({ date:"", amount:"", payment_method:"Cash", category_id:"", notes:"" });
  const [fileById, setFileById] = useState<Record<number, File | null>>({});
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    const [c, e] = await Promise.all([apiGet("/categories/expense"), apiGet("/expenses")]);
    setCats(c);
    setItems(e);
  }

  useEffect(() => {
    load().catch(e=>setErr(e.message));
  }, []);

  async function create() {
    setErr(null);
    const payload = {
      date: form.date,
      amount: Number(form.amount),
      payment_method: form.payment_method,
      category_id: Number(form.category_id),
      notes: form.notes || null
    };
    await apiPost("/expenses", payload);
    setForm({ date:"", amount:"", payment_method:"Cash", category_id:"", notes:"" });
    await load();
  }

  async function upload(expenseId: number) {
    const f = fileById[expenseId];
    if (!f) return;
    await apiUpload(`/expenses/${expenseId}/attachment`, f);
    setFileById(prev => ({...prev, [expenseId]: null}));
    await load();
  }

  return (
    <div className="card">
      <h2>Expenses</h2>
      {err && <p className="small" style={{color:"#b91c1c"}}>{err}</p>}
      <div className="card" style={{marginTop:12}}>
        <h3 style={{marginTop:0}}>Add expense</h3>
        <div className="row">
          <div><label className="small">Date</label><input type="date" value={form.date} onChange={e=>setForm({...form, date:e.target.value})} /></div>
          <div><label className="small">Amount</label><input value={form.amount} onChange={e=>setForm({...form, amount:e.target.value})} /></div>
          <div><label className="small">Payment method</label>
            <select value={form.payment_method} onChange={e=>setForm({...form, payment_method:e.target.value})}>
              <option>Cash</option><option>Bank</option><option>Card</option><option>Other</option>
            </select>
          </div>
          <div><label className="small">Category</label>
            <select value={form.category_id} onChange={e=>setForm({...form, category_id:e.target.value})}>
              <option value="">Select</option>
              {cats.map(c=> <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
        </div>
        <div style={{marginTop:10}}>
          <label className="small">Notes</label>
          <textarea value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})} />
        </div>
        <button className="primary" style={{marginTop:10}} onClick={create} disabled={!form.date || !form.amount || !form.category_id}>Save</button>
      </div>

      <hr />
      <table>
        <thead>
          <tr><th>Date</th><th>Amount</th><th>Method</th><th>Category</th><th>Notes</th><th>Attachment</th></tr>
        </thead>
        <tbody>
          {items.map(it => (
            <tr key={it.id}>
              <td>{it.date}</td>
              <td>{it.amount}</td>
              <td>{it.payment_method}</td>
              <td>{cats.find(c=>c.id===it.category_id)?.name || it.category_id}</td>
              <td>{it.notes || ""}</td>
              <td>
                <input type="file" onChange={e=>setFileById(prev=>({...prev,[it.id]: e.target.files?.[0] || null}))} />
                <button onClick={()=>upload(it.id)}>Upload</button>
                {it.attachment_path ? <span className="badge green">Uploaded</span> : <span className="badge">None</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <p className="small" style={{marginTop:12}}>
        Export: <a href={(process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000") + "/exports/expenses.csv"} target="_blank">expenses.csv</a>
      </p>
    </div>
  );
}
