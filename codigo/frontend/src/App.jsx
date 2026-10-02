import React, { useState, useEffect } from 'react';
import { MessageSquare, Scissors, Upload, Sparkles, CheckCircle2, AlertCircle, Calendar } from 'lucide-react';

export default function App() {
  const [backendStatus, setBackendStatus] = useState('conectando');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: '¡Hola! Soy el asistente inteligente de BarberForge AI. ¿En qué te puedo ayudar hoy? (Consultar precios, agenda de citas o recomendación de corte por foto).' }
  ]);
  const [input, setInput] = useState('');

  useEffect(() => {
    // Probar la conexión real con el contenedor del Backend
    fetch('http://localhost:8000/health')
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'ok') setBackendStatus('online');
        else setBackendStatus('error');
      })
      .catch(() => setBackendStatus('offline'));
  }, []);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setMessages((prev) => [...prev, { role: 'user', text: userMsg }]);
    setInput('');

    // Respuesta simulada para demo de la Etapa 1
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: `Recibido: "${userMsg}". El servicio RAG con Ollama se conectará en las próximas etapas.` }
      ]);
    }, 800);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Navbar Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur px-6 py-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="bg-amber-500 p-2 rounded-xl text-slate-950">
            <Scissors className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight tracking-wide">BarberForge <span className="text-amber-500">AI</span></h1>
            <p className="text-xs text-slate-400">Plataforma Inteligente de Barbería</p>
          </div>
        </div>

        {/* Status de conexión con Backend */}
        <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-full text-xs font-medium border border-slate-700">
          {backendStatus === 'online' && (
            <>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-400">API Backend Online</span>
            </>
          )}
          {backendStatus === 'conectando' && (
            <>
              <div className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></div>
              <span className="text-amber-400">Verificando Backend...</span>
            </>
          )}
          {(backendStatus === 'offline' || backendStatus === 'error') && (
            <>
              <AlertCircle className="w-4 h-4 text-rose-400" />
              <span className="text-rose-400">Backend Desconectado</span>
            </>
          )}
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-6xl w-full mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Panel Izquierdo: Funcionalidades del Sistema */}
        <section className="md:col-span-1 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
            <h2 className="font-semibold text-amber-500 mb-3 flex items-center gap-2 text-sm uppercase tracking-wider">
              <Sparkles className="w-4 h-4" /> Módulos en Desarrollo
            </h2>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex items-start gap-2 bg-slate-950/50 p-3 rounded-lg border border-slate-800">
                <Calendar className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <strong className="block text-slate-100">Agendamiento RAG</strong>
                  <span>Consultas en tiempo real sobre disponibilidad y servicios.</span>
                </div>
              </li>
              <li className="flex items-start gap-2 bg-slate-950/50 p-3 rounded-lg border border-slate-800">
                <Upload className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <strong className="block text-slate-100">Corte por Referencia</strong>
                  <span>Análisis multimodal de imágenes con Ollama.</span>
                </div>
              </li>
            </ul>
          </div>

          <div className="bg-gradient-to-br from-amber-500/10 to-transparent border border-amber-500/20 rounded-2xl p-4 text-xs text-slate-400">
            <p className="font-semibold text-slate-200 mb-1">Estado de Infraestructura (Etapa 1)</p>
            <p>Contenedores activos: Frontend (Vite), Backend (FastAPI) y DB (PostgreSQL + pgvector).</p>
          </div>
        </section>

        {/* Panel Derecho: Chat Interactivo & Demostración */}
        <section className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[520px] shadow-lg overflow-hidden">
          {/* Header del Chat */}
          <div className="bg-slate-950/80 px-4 py-3 border-b border-slate-800 flex items-center justify-between text-sm">
            <span className="font-medium flex items-center gap-2 text-slate-200">
              <MessageSquare className="w-4 h-4 text-amber-500" /> Chatbot de Atención
            </span>
            <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Modelo: Ollama Local</span>
          </div>

          {/* Mensajes */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
                    m.role === 'user'
                      ? 'bg-amber-500 text-slate-950 font-medium rounded-br-none'
                      : 'bg-slate-800 text-slate-200 rounded-bl-none border border-slate-700'
                  }`}
                >
                  {m.text}
                </div>
              </div>
            ))}
          </div>

          {/* Input Chat */}
          <form onSubmit={handleSend} className="p-3 bg-slate-950/80 border-t border-slate-800 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu consulta o pide una cita..."
              className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-amber-500 transition-colors"
            />
            <button
              type="submit"
              className="bg-amber-500 hover:bg-amber-600 text-slate-950 font-semibold px-4 py-2 rounded-xl text-sm transition-colors flex items-center gap-1"
            >
              Enviar
            </button>
          </form>
        </section>

      </main>
    </div>
  );
}