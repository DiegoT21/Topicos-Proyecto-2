// Utilidades compartidas. Regla RNF-02 / CA-10: nunca se inserta HTML armado con datos;
// todo texto que venga de la API se pone con textContent (ver la función el()).
"use strict";

const store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* sin almacenamiento */ } },
  del(key) { try { localStorage.removeItem(key); } catch { /* sin almacenamiento */ } },
};

async function api(path, { method = "GET", body, headers = {} } = {}) {
  const opts = { method, headers: { ...headers } };
  if (body !== undefined) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  const data = res.status === 204 ? null : await res.json().catch(() => null);
  if (!res.ok) throw new Error(errorText(res.status, data));
  return data;
}

function errorText(status, data) {
  const d = data && data.detail;
  if (d && typeof d === "object" && !Array.isArray(d) && d.message) return d.message;
  if (Array.isArray(d) && d.length) {
    const first = d[0];
    const names = { email: "correo", name: "nombre", start_at: "inicio", end_at: "fin" };
    const raw = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : "";
    return `Revisa el campo ${names[raw] || raw}: ${String(first.msg).replace(/^Value error, /, "")}`;
  }
  return `La solicitud falló (código ${status}).`;
}

// Crea un elemento con texto seguro. el("td", "Ana") o el("button", "Cancelar", { class: "danger" })
function el(tag, text, attrs = {}) {
  const node = document.createElement(tag);
  if (text !== undefined && text !== null) node.textContent = String(text);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  return node;
}

function show(target, text, kind = "ok") {
  target.className = `msg ${kind}`;
  target.textContent = text;
}

// Las fechas de la API vienen sin zona ("2099-01-05T10:00:00") en hora de Panamá: se leen como texto
// para no desplazarlas con la zona del navegador (lección del Proyecto 1).
const hourOf = (iso) => iso.slice(11, 16);
const dateOf = (iso) => iso.slice(0, 10);
function prettyDate(isoDate) {
  const [y, m, d] = isoDate.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString("es-PA", { weekday: "long", day: "numeric", month: "long" });
}
function todayLocal() {
  const n = new Date();
  const pad = (x) => String(x).padStart(2, "0");
  return `${n.getFullYear()}-${pad(n.getMonth() + 1)}-${pad(n.getDate())}`;
}
