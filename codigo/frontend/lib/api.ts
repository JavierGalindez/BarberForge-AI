import { borrarToken, conAuth } from "./auth";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ---- Tipos de la API ----

export type Rol = "cliente" | "barbero" | "admin";
export type EstadoCita = "agendada" | "cancelada";

export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  rol: Rol;
}

export interface Servicio {
  id: number;
  nombre: string;
  descripcion: string | null;
  precio: string;
  duracion_minutos: number;
  activo: boolean;
}

export interface Barbero {
  id: number;
  nombre: string;
  hora_inicio: string;
  hora_fin: string;
  activo: boolean;
}

export interface Disponibilidad {
  barbero_id: number;
  servicio_id: number;
  fecha: string;
  horarios: string[];
}

export interface Cita {
  id: number;
  cliente_id: number;
  inicio: string;
  fin: string;
  estado: EstadoCita;
  barbero: Barbero;
  servicio: Servicio;
}

// ---- Cliente HTTP ----

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

function mensajeDeError(cuerpo: unknown, status: number): string {
  const detalle = (cuerpo as { detail?: unknown } | null)?.detail;
  if (typeof detalle === "string") return detalle;
  if (Array.isArray(detalle)) return detalle.map((d) => d?.msg ?? String(d)).join(". ");
  return `Error ${status}`;
}

async function request<T>(ruta: string, init: RequestInit = {}): Promise<T> {
  const respuesta = await fetch(`${API_URL}${ruta}`, { ...init, headers: conAuth(init.headers) });
  const cuerpo = respuesta.status === 204 ? null : await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    if (respuesta.status === 401) borrarToken();
    throw new ApiError(respuesta.status, mensajeDeError(cuerpo, respuesta.status));
  }
  return cuerpo as T;
}

function json(metodo: string, datos: unknown): RequestInit {
  return { method: metodo, headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) };
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: new URLSearchParams({ username: email, password }),
    }),
  registro: (datos: { email: string; nombre: string; password: string }) =>
    request<Usuario>("/auth/register", json("POST", datos)),
  yo: () => request<Usuario>("/auth/me"),

  servicios: () => request<Servicio[]>("/servicios"),
  barberos: () => request<Barbero[]>("/barberos"),
  disponibilidad: (barberoId: number, servicioId: number, fecha: string) =>
    request<Disponibilidad>(
      `/barberos/${barberoId}/disponibilidad?${new URLSearchParams({ servicio_id: String(servicioId), fecha })}`,
    ),

  citas: () => request<Cita[]>("/citas"),
  crearCita: (datos: { barbero_id: number; servicio_id: number; inicio: string }) =>
    request<Cita>("/citas", json("POST", datos)),
  cancelarCita: (id: number) => request<Cita>(`/citas/${id}/cancelar`, { method: "POST" }),
};
