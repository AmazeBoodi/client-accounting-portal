"use client";

import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";

type Client = { id:number; name:string };
type Cat = { id:number; name:string; is_active:boolean };

export default function AdminPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [expCats, setExpCats] = useState<Cat[]>([]);
  const [incCats, setIncCats] = useState<Cat[]>([]);
  const [clientName, setClientName] = useState("");
  const [userForm, setUserForm] = useState({ email:"", name:"", password:"", client_id:"" });
  const [catForm, setCatForm] = useState({ type:"expense", name:"" });
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    const [c, ec, ic] = await Promise.all([
      apiGet("/admin/clients"),
      apiGet("/admin/expense-categories"),
      apiGet("/admin/income-categories"),
    ]);
    setClients(c); setExpCats(ec); setIncCats(ic);
  }

  useEffect(() => { load().catch(e=>setErr(e.message)); }, []);

  async function createClient() {
    setErr(null);
    await apiPost("/admin/clients", { name: clientName });
    setClientName("");
    await load();
  }

  async function createUser() {
    setErr(null);
    await apiPost("/admin/client-users", {
      email: userForm.email,
      name: userForm.name,
      password: userForm.password,
      client_id: Number(userForm.client_id),
    });
    setUserForm({ email:"", name:"", password:"", client_id:"" });
    alert("Client user created.");
  }

  async function createCategory() {
    setErr(null);
    const path = catForm.type === "expense" ? "/admin/expense-categories" : "/admin/income-categories";
    await apiPost(path, { name: catForm.name, is_active: true });
    setCatForm({ ...catForm, name:"" });
    await load();
  }

  return (
    <div className="card">
      <h2>Admin</h2>
      {err && <p className="small" style={{color:"#b91c1c"}}>{err}</p>}

      <div className="row">
        <div className="card">
          <h3 style={{marginTop:0}}>Create Client</h3>
          <input value={clientName} onChange={e=>setClientName(e.target.value)} placeholder="Client company name" />
          <button className="primary" style={{marginTop:10}} onClick={createClient} disabled={!clientName}>Create</button>
          <hr/>
          <div className="small">Clients:</div>
          <ul>
            {clients.map(c => <li key={c.id}>{c.name} (ID: {c.id})</li>)}
          </ul>
        </div>

        <div className="card">
          <h3 style={{marginTop:0}}>Create Client Login</h3>
          <div className="row">
            <div><label className="small">Client</label>
              <select value={userForm.client_id} onChange={e=>setUserForm({...userForm, client_id:e.target.value})}>
                <option value="">Select</option>
                {clients.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div><label className="small">Name</label><input value={userForm.name} onChange={e=>setUserForm({...userForm, name:e.target.value})} /></div>
          </div>
          <div className="row" style={{marginTop:8}}>
            <div><label className="small">Email</label><input value={userForm.email} onChange={e=>setUserForm({...userForm, email:e.target.value})} /></div>
            <div><label className="small">Password</label><input type="password" value={userForm.password} onChange={e=>setUserForm({...userForm, password:e.target.value})} /></div>
          </div>
          <button className="primary" style={{marginTop:10}} onClick={createUser} disabled={!userForm.client_id || !userForm.email || !userForm.password || !userForm.name}>Create login</button>
        </div>
      </div>

      <hr />
      <div className="row">
        <div className="card">
          <h3 style={{marginTop:0}}>Categories</h3>
          <div className="row">
            <div>
              <label className="small">Type</label>
              <select value={catForm.type} onChange={e=>setCatForm({...catForm, type:e.target.value})}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            <div>
              <label className="small">Name</label>
              <input value={catForm.name} onChange={e=>setCatForm({...catForm, name:e.target.value})} placeholder="Category name" />
            </div>
          </div>
          <button className="primary" style={{marginTop:10}} onClick={createCategory} disabled={!catForm.name}>Add</button>
          <hr />
          <div className="small">Expense categories</div>
          <ul>{expCats.map(c => <li key={c.id}>{c.name}</li>)}</ul>
          <div className="small">Income categories</div>
          <ul>{incCats.map(c => <li key={c.id}>{c.name}</li>)}</ul>
        </div>
      </div>
    </div>
  );
}
