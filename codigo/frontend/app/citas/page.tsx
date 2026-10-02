"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import Aviso from "@/components/Aviso";
import { api, type Cita } from "@/lib/api";
import { leerToken } from "@/lib/auth";
import { fecha, formatearPrecio, hora } from "@/lib/formato";

export default function Citas() {
  const [autenticado, setAutenticado] = useState<boolean | null>(null);
  const [citas, setCitas] = useState<Cita[] | null>(null);
  const [error, setError] = useState("");

  const cargar = useCallback(() => {
    api
      .citas()
      .then(setCitas)
      .catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    const hayToken = Boolean(leerToken());
    setAutenticado(hayToken);
    if (hayToken) cargar();
  }, [cargar]);

  const cancelar = async (id: number) => {
    if (!confirm("¿Cancelar esta cita?")) return;
    setError("");
    try {
      await api.cancelarCita(id);
      cargar();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  if (autenticado === false) {
    return (
      <>
        <h1>Citas</h1>
        <p className="tenue">
          <Link href="/login">Ingresa</Link> para ver tus citas.
        </p>
      </>
    );
  }

  return (
    <>
      <h1>Citas</h1>
      <p className="tenue">
        <Link href="/agendar">Agendar una nueva cita</Link>
      </p>
      <Aviso>{error}</Aviso>
      {citas?.length === 0 && <p className="tenue">No hay citas.</p>}
      <ul className="lista-citas">
        {citas?.map((c) => (
          <li key={c.id} className={`tarjeta estado-${c.estado}`}>
            <div>
              <strong>{c.servicio.nombre}</strong> con {c.barbero.nombre}
              <p className="tenue">
                {fecha(c.inicio)} · {hora(c.inicio)}–{hora(c.fin)} · {formatearPrecio(c.servicio.precio)}
              </p>
            </div>
            {c.estado === "agendada" ? (
              <button className="secundario" onClick={() => cancelar(c.id)}>
                Cancelar
              </button>
            ) : (
              <span className="tenue">Cancelada</span>
            )}
          </li>
        ))}
      </ul>
    </>
  );
}
