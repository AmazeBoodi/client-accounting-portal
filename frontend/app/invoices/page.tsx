"use client";

import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";

type Invoice = {
  id:number; invoice_number:string; customer_name:string; due_date:string; total_amount:number;
  paid_amount:number; balance:number; status:string; is_overdue:boolean;
};

export default function InvoicesPage() {
  const [items, setItems] = useState<Invoice[]>([]);
  const [form, setForm] = useState({ invoice_number:"", customer_name:"", due_date:"", total_amount:"" });
  const [pay, setPay] = useState<{[k:number]: { payment_date:string; amount:string; payment_method:string }}>({});
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    const inv = await apiGet("/invoices");
    setItems(inv);
  }
  useEffect(() => { load().catch(e=>setErr(e.message)); }, []);

  async function createInvoice() {
    setErr(null);
    await apiPost("/invoices", {
      invoice_number: form.invoice_number,
      customer_name: form.customer_name,
      due_date: form.due_date,
      total_amount: Number(form.total_amount),
      issue_date: null,
      notes: null
    });
    setForm({ invoice_number:"", customer_name:"", due_date:"", total_amount:"" });
    await load();
  }

  async function addPayment(id: number) {
    setErr(null);
    const p = pay[id] || { payment_date:"", amount:"", payment_method:"Bank" };
    await apiPost(`/invoices/${id}/payments`, {
      payment_date: p.payment_date,
      amount: Number(p.amount),
      payment_method: p.payment_method,
      notes: null
    });
    await load();
  }

  return (
    <div className="card">
      <h2>Invoices</h2>
      {err && <p className="small" style={{color:"#b91c1c"}}>{err}</p>}

      <div className="card" style={{marginTop:12}}>
        <h3 style={{marginTop:0}}>Create invoice</h3>
        <div className="row">
          <div><label className="small">Invoice #</label><input value={form.invoice_number} onChange={e=>setForm({...form, invoice_number:e.target.value})} /></div>
          <div><label className="small">Customer</label><input value={form.customer_name} onChange={e=>setForm({...form, customer_name:e.target.value})} /></div>
          <div><label className="small">Due date</label><input type="date" value={form.due_date} onChange={e=>setForm({...form, due_date:e.target.value})} /></div>
          <div><label className="small">Amount</label><input value={form.total_amount} onChange={e=>setForm({...form, total_amount:e.target.value})} /></div>
        </div>
        <button className="primary" style={{marginTop:10}} onClick={createInvoice} disabled={!form.invoice_number || !form.customer_name || !form.due_date || !form.total_amount}>Save</button>
      </div>

      <hr />
      <table>
        <thead>
          <tr><th>Invoice</th><th>Customer</th><th>Due</th><th>Total</th><th>Paid</th><th>Balance</th><th>Status</th><th>Add payment</th></tr>
        </thead>
        <tbody>
          {items.map(inv => (
            <tr key={inv.id}>
              <td>{inv.invoice_number}</td>
              <td>{inv.customer_name}</td>
              <td>
                {inv.due_date}{" "}
                {inv.is_overdue && inv.balance > 0 ? <span className="badge red">Overdue</span> : null}
              </td>
              <td>{inv.total_amount}</td>
              <td>{inv.paid_amount}</td>
              <td>{inv.balance}</td>
              <td>
                <span className={"badge " + (inv.status==="Paid" ? "green" : "")}>{inv.status}</span>
              </td>
              <td>
                <div className="row" style={{gap:8}}>
                  <input type="date" value={(pay[inv.id]?.payment_date)||""} onChange={e=>setPay(prev=>({...prev, [inv.id]: {...(prev[inv.id]||{payment_method:"Bank"}), payment_date:e.target.value}}))} />
                  <input placeholder="Amount" value={(pay[inv.id]?.amount)||""} onChange={e=>setPay(prev=>({...prev, [inv.id]: {...(prev[inv.id]||{payment_method:"Bank"}), amount:e.target.value}}))} />
                  <select value={(pay[inv.id]?.payment_method)||"Bank"} onChange={e=>setPay(prev=>({...prev, [inv.id]: {...(prev[inv.id]||{}), payment_method:e.target.value}}))}>
                    <option>Cash</option><option>Bank</option><option>Card</option><option>Other</option>
                  </select>
                </div>
                <button onClick={()=>addPayment(inv.id)} disabled={!pay[inv.id]?.payment_date || !pay[inv.id]?.amount}>Add</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <p className="small" style={{marginTop:12}}>
        Export: <a href={(process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000") + "/exports/invoices.csv"} target="_blank">invoices.csv</a> ·{" "}
        <a href={(process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000") + "/exports/invoice_payments.csv"} target="_blank">invoice_payments.csv</a>
      </p>
    </div>
  );
}
