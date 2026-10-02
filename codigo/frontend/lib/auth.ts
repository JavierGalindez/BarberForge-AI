const TOKEN_KEY = "barberforge_token";
const EVENTO = "barberforge-auth";

export function guardarToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
  window.dispatchEvent(new Event(EVENTO));
}

export function leerToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function borrarToken(): void {
  localStorage.removeItem(TOKEN_KEY);
  window.dispatchEvent(new Event(EVENTO));
}

/** Agrega el header Authorization: Bearer si hay un token guardado. */
export function conAuth(headers: HeadersInit = {}): Headers {
  const resultado = new Headers(headers);
  const token = leerToken();
  if (token) resultado.set("Authorization", `Bearer ${token}`);
  return resultado;
}

/** Permite a los componentes reaccionar cuando se inicia o cierra sesión. */
export function suscribirseAuth(callback: () => void): () => void {
  window.addEventListener(EVENTO, callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener(EVENTO, callback);
    window.removeEventListener("storage", callback);
  };
}
