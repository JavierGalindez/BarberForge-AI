"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import Aviso from "@/components/Aviso";
import ServicioCard from "@/components/ServicioCard";
import { api, type Servicio } from "@/lib/api";

export default function Inicio() {
  const [servicios, setServicios] = useState<Servicio[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .servicios()
      .then(setServicios)
      .catch((e: Error) => setError(`No se pudieron cargar los servicios: ${e.message}`));
  }, []);

  return (
    <>
      <h1>Nuestros servicios</h1>
      <p className="tenue">
        Elige un servicio y <Link href="/agendar">agenda tu cita</Link>.
      </p>
      <Aviso>{error}</Aviso>
      {servicios === null && !error && <p className="tenue">Cargando…</p>}
      {servicios?.length === 0 && <p className="tenue">Aún no hay servicios en el catálogo.</p>}
      <section className="rejilla">
        {servicios?.map((s) => <ServicioCard key={s.id} servicio={s} />)}
      </section>
    </>
  );
}
