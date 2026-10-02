"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { api, type Usuario } from "@/lib/api";
import { borrarToken, leerToken, suscribirseAuth } from "@/lib/auth";

export default function Navbar() {
  const router = useRouter();
  const [usuario, setUsuario] = useState<Usuario | null>(null);

  useEffect(() => {
    const cargar = () => {
      if (!leerToken()) return setUsuario(null);
      api.yo().then(setUsuario).catch(() => setUsuario(null));
    };
    cargar();
    return suscribirseAuth(cargar);
  }, []);

  const salir = () => {
    borrarToken();
    router.push("/");
  };

  return (
    <header className="navbar">
      <Link href="/" className="marca">
        BarberForge
      </Link>
      <nav>
        <Link href="/">Servicios</Link>
        {usuario ? (
          <>
            {usuario.rol !== "barbero" && <Link href="/agendar">Agendar</Link>}
            <Link href="/citas">{usuario.rol === "cliente" ? "Mis citas" : "Agenda"}</Link>
            <span className="usuario">{usuario.nombre}</span>
            <button className="enlace" onClick={salir}>
              Salir
            </button>
          </>
        ) : (
          <>
            <Link href="/login">Ingresar</Link>
            <Link href="/registro" className="boton">
              Crear cuenta
            </Link>
          </>
        )}
      </nav>
    </header>
  );
}
