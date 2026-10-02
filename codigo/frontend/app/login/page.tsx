"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import Aviso from "@/components/Aviso";
import { api } from "@/lib/api";
import { guardarToken } from "@/lib/auth";

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  const enviar = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setEnviando(true);
    try {
      const { access_token } = await api.login(email, password);
      guardarToken(access_token);
      router.push("/citas");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <>
      <h1>Ingresar</h1>
      <p className="tenue">
        ¿No tienes cuenta? <Link href="/registro">Regístrate</Link>
      </p>
      <form className="formulario" onSubmit={enviar}>
        <label>
          Email
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Contraseña
          <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit" disabled={enviando}>
          {enviando ? "Ingresando…" : "Ingresar"}
        </button>
        <Aviso>{error}</Aviso>
      </form>
    </>
  );
}
