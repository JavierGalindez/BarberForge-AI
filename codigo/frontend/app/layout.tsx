import type { Metadata } from "next";

import Navbar from "@/components/Navbar";

import "./globals.css";

export const metadata: Metadata = {
  title: "BarberForge",
  description: "Agenda tu cita en la barbería",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Navbar />
        <main className="contenedor">{children}</main>
      </body>
    </html>
  );
}
