"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import Aviso from "@/components/Aviso";
import { api } from "@/lib/api";
import { guardarToken } from "@/lib/auth";

export default function Registro() {
  const router = useRouter();
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  const enviar = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setEnviando(true);
    try {
      await api.registro({ nombre, email, password });
      const { access_token } = await api.login(email, password);
      guardarToken(access_token);
      router.push("/agendar");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <>
      <h1>Crear cuenta</h1>
      <p className="tenue">
        ¿Ya tienes cuenta? <Link href="/login">Ingresa</Link>
      </p>
      <form className="formulario" onSubmit={enviar}>
        <label>
          Nombre
          <input required maxLength={120} value={nombre} onChange={(e) => setNombre(e.target.value)} />
        </label>
        <label>
          Email
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Contraseña (mínimo 8 caracteres)
          <input
            type="password"
            required
            minLength={8}
            maxLength={72}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit" disabled={enviando}>
          {enviando ? "Creando…" : "Crear cuenta"}
        </button>
        <Aviso>{error}</Aviso>
      </form>
    </>
  );
}
