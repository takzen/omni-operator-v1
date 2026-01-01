"use client";

import React, { useState } from "react";
import MissionControl from "@/components/MissionControl";
import {
  Terminal,
  ShieldCheck,
  Video,
  Copy,
  Check,
  Zap,
  Share2,
  Cpu,
  Layers,
  MonitorCheck,
} from "lucide-react";

export default function Home() {
  const [missionResult, setMissionResult] = useState<any>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [tacticalId, setTacticalId] = useState<string>("");

  React.useEffect(() => {
    setTacticalId(Math.random().toString(36).substring(7).toUpperCase());
  }, []);

  return (
    <div className="min-h-screen bg-[#020202] text-zinc-100 font-sans selection:bg-red-700/50 overflow-hidden relative">
      {/* TACTICAL OVERLAYS */}
      <div className="scanline" />
      <div className="crt-overlay" />

      {/* AMBIENT GLOWS */}
      <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-red-900/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-red-900/10 rounded-full blur-[120px] pointer-events-none" />

      <main className="max-w-[1600px] mx-auto px-6 py-12 md:py-16 relative z-10">
        {/* HEADER: TACTICAL HUD STYLE */}
        <header className="mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 glass-panel p-8 rounded-2xl border-l-4 border-l-red-700 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-2 opacity-5 scale-150 rotate-12 group-hover:rotate-0 transition-all duration-700">
            <Cpu size={120} />
          </div>
          <div className="space-y-2 relative z-10">
            <div className="flex items-center gap-4">
              <div className="bg-red-700 p-3 rounded-lg red-glow">
                <Terminal size={28} className="text-white" />
              </div>
              <div>
                <h1 className="text-4xl md:text-5xl font-black tracking-tighter uppercase italic text-white glow-text">
                  OMNI-OPERATOR <span className="text-red-700">V1.0.0</span>
                </h1>
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    {[1, 2, 3].map((i) => (
                      <div
                        key={i}
                        className="w-1 h-3 bg-red-700 animate-pulse"
                        style={{ animationDelay: `${i * 0.2}s` }}
                      />
                    ))}
                  </div>
                  <p className="text-[10px] text-zinc-400 tracking-[0.6em] uppercase font-black">
                    Autonomous Content Intelligence Branch
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="bg-zinc-950/80 border border-zinc-800 px-6 py-3 rounded-xl flex items-center gap-4 backdrop-blur-md">
              <div className="relative">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-ping absolute inset-0" />
                <div className="w-2 h-2 bg-green-500 rounded-full relative" />
              </div>
              <div className="flex flex-col">
                <span className="text-[9px] font-black uppercase tracking-widest text-zinc-500">
                  Core Engine
                </span>
                <span className="text-xs font-bold text-green-500">
                  GEMINI_3_FLASH_PREVIEW
                </span>
              </div>
            </div>
            <div className="bg-zinc-950/80 border border-zinc-800 px-6 py-3 rounded-xl flex items-center gap-3 backdrop-blur-md">
              <ShieldCheck className="text-red-600" size={18} />
              <div className="flex flex-col">
                <span className="text-[9px] font-black uppercase tracking-widest text-zinc-500">
                  Node Secure
                </span>
                <span className="text-xs font-bold text-zinc-200 uppercase">
                  Active
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* MAIN LAYOUT */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* LEFT: MISSION CONTROL */}
          <div className="lg:col-span-5 space-y-8 animate-in slide-in-from-left-10 duration-700">
            <div className="flex items-center justify-between px-2">
              <h2 className="text-red-700 font-black uppercase text-xs tracking-[0.3em] flex items-center gap-3">
                <MonitorCheck size={16} /> [ COMMAND_CENTER_STATION ]
              </h2>
              <span className="text-[9px] text-zinc-600 font-mono">
                ID: {tacticalId || "PENDING"}
              </span>
            </div>

            <div className="relative group">
              <div className="corner-top-left" />
              <div className="corner-bottom-right" />
              <div className="glass-panel p-8 rounded-3xl border border-white/5 group-hover:border-red-900/20 transition-all">
                <MissionControl onComplete={(data) => setMissionResult(data)} />
              </div>
            </div>

            {/* TACTICAL READOUT (Aesthetic only) */}
            <div className="glass-panel p-5 rounded-2xl border border-white/5 font-mono text-[9px] text-zinc-600 space-y-2 uppercase leading-none overflow-hidden h-32 opacity-50 relative">
              <div className="absolute top-0 right-0 p-3 flex gap-1">
                <div className="w-2 h-2 bg-red-900/20" />
                <div className="w-2 h-2 bg-red-900/40" />
                <div className="w-2 h-2 bg-red-900/60" />
              </div>
              <p className="">System.Internal.State: IDLE</p>
              <p className="">Network.Latency: 14ms</p>
              <p className="">Processor.Load: 4.2%</p>
              <p className="">Buffer.Status: NULL_POINTER_SAFE</p>
              <p className="">&gt;&gt; Ready for sequence initiation...</p>
              <p className="text-red-900">
                &gt;&gt; Authenticating biometric handshake...
              </p>
              <p className="">Encryption.Standard: AES-256-GCM</p>
              <p className="animate-pulse">_ TERMINAL HEARTBEAT [OK]</p>
            </div>
          </div>

          {/* RIGHT: OUTPUT HANGAR */}
          <div className="lg:col-span-7 space-y-8 animate-in fade-in duration-1000">
            <div className="flex items-center justify-between px-2">
              <h2 className="text-zinc-500 font-black uppercase text-xs tracking-[0.3em] flex items-center gap-3">
                <Layers size={16} /> [ ASSET_HANGAR_DEPLOYMENT ]
              </h2>
              {missionResult && (
                <span className="text-[9px] text-red-600 font-black uppercase animate-pulse">
                  Transmission Received
                </span>
              )}
            </div>

            {missionResult ? (
              <div className="space-y-10 animate-in fade-in slide-in-from-right-10 duration-1000">
                {/* STRATEGY SUMMARY */}
                <div className="glass-panel p-8 rounded-3xl relative overflow-hidden group">
                  <div className="absolute top-0 left-0 w-2 h-full bg-red-700 shadow-[0_0_15px_rgba(194,29,29,0.5)]" />
                  <div className="flex items-center gap-4 mb-4">
                    <div className="p-2 bg-red-700/10 rounded-lg">
                      <Zap className="text-red-600" size={20} />
                    </div>
                    <h3 className="text-white font-black uppercase text-[10px] tracking-[0.2em] glow-text">
                      Strategic Objective Report
                    </h3>
                  </div>
                  <p className="text-zinc-300 text-xs leading-relaxed font-medium italic opacity-90 first-letter:text-2xl first-letter:font-black first-letter:text-red-700 first-letter:mr-1">
                    {missionResult.campaign?.overall_strategy}
                  </p>
                </div>

                {/* PRODUCED CLIPS */}
                <div className="grid grid-cols-1 gap-12">
                  {missionResult.videos?.map((video: any, i: number) => (
                    <div
                      key={i}
                      className="glass-panel rounded-[2.5rem] overflow-hidden transition-all hover:scale-[1.01] duration-500 group relative border border-white/5"
                    >
                      <div className="absolute -inset-px bg-gradient-to-r from-red-600/0 via-red-600/10 to-red-600/0 opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />

                      <div className="grid grid-cols-1 md:grid-cols-2 relative z-10">
                        {/* VIDEO PLAYER */}
                        <div className="bg-black/90 aspect-[9/16] relative flex items-center justify-center border-r border-white/5">
                          <video
                            src={`http://localhost:8000${video.url}`}
                            controls
                            className="w-full h-full object-contain"
                          />
                          <div className="absolute top-6 left-6 bg-red-700/90 backdrop-blur-lg text-white text-[9px] font-black px-5 py-2 rounded-lg uppercase shadow-2xl tracking-widest border border-white/10">
                            UNIT_SHORT_IDX_{i + 1}
                          </div>

                          {/* Corner deco on player */}
                          <div className="absolute bottom-6 right-6 flex gap-2">
                            <div className="w-1 h-8 bg-white/10" />
                            <div className="w-1 h-8 bg-white/5" />
                          </div>
                        </div>

                        {/* POST CONTENT */}
                        <div className="p-10 space-y-8 bg-zinc-950/20 backdrop-blur-sm self-center">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3 text-zinc-500">
                              <Share2 size={16} className="text-red-700" />
                              <span className="text-[10px] font-black uppercase tracking-[0.3em]">
                                Multi-Platform Dissemination
                              </span>
                            </div>
                            {/* VIRAL SCORE GAUGE */}
                            <div className="flex items-center gap-4 bg-red-950/10 px-4 py-2 rounded-xl border border-red-900/10">
                              <div className="flex flex-col items-end">
                                <span className="text-[7px] font-black text-zinc-500 uppercase tracking-widest">
                                  Viral_Potential
                                </span>
                                <span className="text-sm font-black text-red-600 glow-text">
                                  {missionResult.analysis?.clips?.[i]?.score ||
                                    "8.2"}
                                  /10
                                </span>
                              </div>
                              <Zap
                                size={14}
                                className="text-red-700 animate-pulse"
                              />
                            </div>
                          </div>

                          <div className="space-y-6">
                            {missionResult.campaign?.clip_strategies
                              ?.find((strat: any) => strat.clip_index === i + 1)
                              ?.posts?.map((post: any, pi: number) => (
                                <div
                                  key={pi}
                                  className="bg-black/40 border border-white/5 p-6 rounded-2xl space-y-4 relative group/post hover:bg-black/60 transition-all duration-300"
                                >
                                  <div className="flex justify-between items-center px-1">
                                    <span className="text-red-500 font-black text-[9px] uppercase tracking-widest">
                                      // {post.platform}
                                    </span>
                                    <button
                                      onClick={() => {
                                        navigator.clipboard.writeText(
                                          post.content
                                        );
                                        setCopiedId(`p-${i}-${pi}`);
                                        setTimeout(
                                          () => setCopiedId(null),
                                          2000
                                        );
                                      }}
                                      className="text-zinc-700 hover:text-red-600 transition-all p-1"
                                    >
                                      {copiedId === `p-${i}-${pi}` ? (
                                        <Check
                                          size={18}
                                          className="text-green-500"
                                        />
                                      ) : (
                                        <Copy size={18} />
                                      )}
                                    </button>
                                  </div>
                                  <p className="text-[11px] text-zinc-400 font-medium leading-relaxed tracking-tight lg:tracking-normal selection:bg-red-900/30">
                                    {post.content}
                                  </p>
                                  {post.hashtags &&
                                    post.hashtags.length > 0 && (
                                      <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-white/5">
                                        {post.hashtags.map(
                                          (tag: string, ti: number) => (
                                            <span
                                              key={ti}
                                              className="text-[8px] text-zinc-600 font-bold uppercase tracking-widest px-2 py-0.5 bg-white/5 rounded"
                                            >
                                              #{tag}
                                            </span>
                                          )
                                        )}
                                      </div>
                                    )}
                                </div>
                              ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              /* EMPTY STATE: TACTICAL HUD STYLE */
              <div className="glass-panel border-2 border-dashed border-zinc-800 bg-zinc-950/20 rounded-[4rem] h-[650px] flex flex-col items-center justify-center p-12 text-center group relative overflow-hidden">
                <div className="absolute inset-0 bg-red-900/5 animate-pulse" />
                <div className="relative z-10 transition-all duration-700 group-hover:scale-110">
                  <div className="relative mb-10">
                    <Video size={84} className="text-zinc-800" />
                    <div className="absolute inset-0 bg-red-700 blur-[40px] opacity-10 group-hover:opacity-30 transition-opacity" />
                  </div>
                  <h3 className="text-zinc-400 font-black text-xs uppercase tracking-[0.5em] mb-4">
                    Neural Analytics Offline
                  </h3>
                  <p className="text-zinc-600 font-mono text-[10px] uppercase tracking-widest max-w-[280px] leading-loose">
                    Upload source material to initiate{" "}
                    <span className="text-red-800 font-black">
                      AI Orchestration Sequence
                    </span>
                  </p>
                </div>

                {/* HUD Deco elements in corners */}
                <div className="absolute top-10 left-10 w-20 h-20 border-l border-t border-zinc-900" />
                <div className="absolute bottom-10 right-10 w-20 h-20 border-r border-b border-zinc-900" />
              </div>
            )}
          </div>
        </div>

        <footer className="mt-40 mb-10 flex flex-col items-center gap-6 opacity-30">
          <div className="flex gap-1">
            {[...Array(12)].map((_, i) => (
              <div
                key={i}
                className={`w-0.5 h-4 ${i % 3 === 0 ? "bg-red-700" : "bg-zinc-800"
                  }`}
              />
            ))}
          </div>
          <p className="text-[10px] font-black uppercase tracking-[2em] text-zinc-400">
            Kuźnia Operatorów // Sovereign Content Stack
          </p>
        </footer>
      </main>
    </div>
  );
}
