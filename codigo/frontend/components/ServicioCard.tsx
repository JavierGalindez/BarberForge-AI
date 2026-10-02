import type { Servicio } from "@/lib/api";
import { formatearPrecio } from "@/lib/formato";

export default function ServicioCard({ servicio }: { servicio: Servicio }) {
  return (
    <article className="tarjeta">
      <h3>{servicio.nombre}</h3>
      {servicio.descripcion && <p className="tenue">{servicio.descripcion}</p>}
      <p className="detalle">
        <strong>{formatearPrecio(servicio.precio)}</strong>
        <span>{servicio.duracion_minutos} min</span>
      </p>
    </article>
  );
}
