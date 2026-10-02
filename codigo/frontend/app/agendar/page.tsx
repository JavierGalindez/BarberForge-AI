"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import Aviso from "@/components/Aviso";
import { api, type Barbero, type Servicio } from "@/lib/api";
import { leerToken } from "@/lib/auth";
import { formatearPrecio, hora, hoy } from "@/lib/formato";

export default function Agendar() {
  const router = useRouter();
  const [autenticado, setAutenticado] = useState<boolean | null>(null);
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [barberos, setBarberos] = useState<Barbero[]>([]);
  const [servicioId, setServicioId] = useState("");
  const [barberoId, setBarberoId] = useState("");
  const [fecha, setFecha] = useState(hoy());
  const [horarios, setHorarios] = useState<string[] | null>(null);
  const [inicio, setInicio] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    setAutenticado(Boolean(leerToken()));
    Promise.all([api.servicios(), api.barberos()])
      .then(([s, b]) => {
        setServicios(s);
        setBarberos(b);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    setInicio("");
    setHorarios(null);
    if (!servicioId || !barberoId || !fecha) return;
    api
      .disponibilidad(Number(barberoId), Number(servicioId), fecha)
      .then((d) => setHorarios(d.horarios))
      .catch((e: Error) => setError(e.message));
  }, [servicioId, barberoId, fecha]);

  const agendar = async () => {
    setError("");
    setEnviando(true);
    try {
      await api.crearCita({ barbero_id: Number(barberoId), servicio_id: Number(servicioId), inicio });
      router.push("/citas");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setEnviando(false);
    }
  };

  if (autenticado === false) {
    return (
      <>
        <h1>Agendar cita</h1>
        <p className="tenue">
          Para agendar necesitas <Link href="/login">ingresar</Link> o <Link href="/registro">crear una cuenta</Link>.
        </p>
      </>
    );
  }

  return (
    <>
      <h1>Agendar cita</h1>
      <div className="formulario">
        <label>
          Servicio
          <select value={servicioId} onChange={(e) => setServicioId(e.target.value)}>
            <option value="">Selecciona un servicio</option>
            {servicios.map((s) => (
              <option key={s.id} value={s.id}>
                {s.nombre} · {formatearPrecio(s.precio)} · {s.duracion_minutos} min
              </option>
            ))}
          </select>
        </label>
        <label>
          Barbero
          <select value={barberoId} onChange={(e) => setBarberoId(e.target.value)}>
            <option value="">Selecciona un barbero</option>
            {barberos.map((b) => (
              <option key={b.id} value={b.id}>
                {b.nombre} ({b.hora_inicio.slice(0, 5)}–{b.hora_fin.slice(0, 5)})
              </option>
            ))}
          </select>
        </label>
        <label>
          Fecha
          <input type="date" min={hoy()} value={fecha} onChange={(e) => setFecha(e.target.value)} />
        </label>

        {horarios !== null && (
          <fieldset style={{ border: "none", padding: 0, margin: 0 }}>
            <legend style={{ fontWeight: 500, marginBottom: "0.35rem" }}>Horario</legend>
            {horarios.length === 0 ? (
              <p className="tenue">No hay horarios libres ese día.</p>
            ) : (
              <div className="horarios">
                {horarios.map((h) => (
                  <button key={h} type="button" aria-pressed={inicio === h} onClick={() => setInicio(h)}>
                    {hora(h)}
                  </button>
                ))}
              </div>
            )}
          </fieldset>
        )}

        <button onClick={agendar} disabled={!inicio || enviando}>
          {enviando ? "Agendando…" : "Confirmar cita"}
        </button>
        <Aviso>{error}</Aviso>
      </div>
    </>
  );
}
