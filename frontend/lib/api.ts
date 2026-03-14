"use client";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
const TOKEN_KEY = "portal_token";

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path: string, opts: RequestInit = {}) {
  const token = getToken();
  const headers: Record<string, string> = { ...(opts.headers as any) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!headers["Content-Type"] && !(opts.body instanceof FormData)) headers["Content-Type"] = "application/json";

  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `Request failed ${res.status}`);
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return res.json();
  return res;
}

export async function apiGet(path: string) { return request(path); }
export async function apiPost(path: string, body: any) {
  return request(path, { method: "POST", body: JSON.stringify(body) });
}
export async function apiUpload(path: string, file: File) {
  const form = new FormData();
  form.append("file", file);
  return request(path, { method: "POST", body: form });
}
