export default function Aviso({ tipo = "error", children }: { tipo?: "error" | "exito"; children: React.ReactNode }) {
  if (!children) return null;
  return (
    <p className={`aviso aviso-${tipo}`} role={tipo === "error" ? "alert" : "status"}>
      {children}
    </p>
  );
}
