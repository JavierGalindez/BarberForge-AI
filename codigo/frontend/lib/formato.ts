export function formatearPrecio(precio: string | number): string {
  return new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 }).format(
    Number(precio),
  );
}

/** "2030-01-15T09:00:00" → "09:00". La API usa la hora local de la barbería, sin zona horaria. */
export function hora(fechaHora: string): string {
  return fechaHora.slice(11, 16);
}

/** "2030-01-15T09:00:00" → "mar, 15 ene 2030" */
export function fecha(fechaHora: string): string {
  const [a, m, d] = fechaHora.slice(0, 10).split("-").map(Number);
  return new Date(a, m - 1, d).toLocaleDateString("es-CO", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

/** Fecha local de hoy en formato YYYY-MM-DD. */
export function hoy(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
