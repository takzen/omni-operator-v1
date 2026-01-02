"use client";

import React, { useState } from "react";
import {
  Upload,
  Activity,
  CheckCircle2,
  AlertCircle,
  Terminal as TerminalIcon,
  Fingerprint,
  Radio,
  Scan,
} from "lucide-react";

type MissionStatus =
  | "idle"
  | "analyzing"
  | "writing"
  | "rendering"
  | "completed"
  | "failed";

export default function MissionControl({
  onComplete,
}: {
  onComplete: (data: any) => void;
}) {
  const [status, setStatus] = useState<MissionStatus>("idle");
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [thought, setThought] = useState<string>("SYSTEM_READY_FOR_DEPLOYMENT");

  const thoughts = [
    "ANALYZING_VISUAL_FREQUENCIES...",
    "EXTRACTING_SEMANTIC_NODES...",
    "IDENTIFYING_VIRAL_PEAKS...",
    "OPTIMIZING_TIKTOK_WEIGHTS...",
    "GENERATING_NARRATIVE_HOOKS...",
    "FFMPEG_BITRATE_STABILIZATION...",
    "RECONSTRUCTING_SCENE_METADATA...",
    "SYNCING_NEURAL_LINK_API...",
    "VALIDATING_PYDANTIC_SCHEMAS...",
  ];

  React.useEffect(() => {
    if (status !== "idle" && status !== "completed" && status !== "failed") {
      const interval = setInterval(() => {
        setThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [status]);

  const startMission = async () => {
    if (!file) return;
    setError(null);
    setStatus("analyzing");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok)
        throw new Error("Neural link rejected source material.");

      const data = await response.json();
      setJobId(data.job_id);
      pollStatus(data.job_id);
    } catch (err: any) {
      setError(err.message);
      setStatus("failed");
    }
  };

  const pollStatus = (id: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/status/${id}`);
        const data = await res.json();

        if (data.status === "ANALYZING") setStatus("analyzing");
        if (data.status === "WRITING") setStatus("writing");
        if (data.status === "RENDERING") setStatus("rendering");

        if (data.status === "COMPLETED") {
          setStatus("completed");
          onComplete(data.result);
          clearInterval(interval);
        }

        if (data.status === "FAILED") {
          setError(data.error);
          setStatus("failed");
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Poll error:", err);
      }
    }, 2000);
  };

  return (
    <div className="flex flex-col gap-8">
      {/* SCANNER AREA */}
      <div
        className={`relative border-2 rounded-[2rem] h-72 flex flex-col items-center justify-center p-10 transition-all duration-500 overflow-hidden group/scanner ${
          file
            ? "border-red-600 bg-red-950/5"
            : "border-white/5 bg-black/40 hover:bg-black/60 hover:border-white/10"
        }`}
      >
        {/* Animated Scanner Bar */}
        {status !== "idle" && status !== "completed" && status !== "failed" && (
          <div className="absolute inset-0 z-0 pointer-events-none">
            <div className="w-full h-1 bg-red-600/40 blur-sm animate-[scanbar_2s_ease-in-out_infinite] absolute top-0" />
          </div>
        )}

        <div className="relative z-10 flex flex-col items-center gap-6">
          <div className="relative group/icon">
            <Scan
              className={`w-14 h-14 transition-all duration-500 ${
                file ? "text-red-600 scale-110 rotate-90" : "text-zinc-800"
              }`}
            />
            {file && (
              <Fingerprint className="absolute inset-0 m-auto text-red-500 animate-pulse w-6 h-6" />
            )}
          </div>

          <div className="text-center space-y-2">
            <p className="text-zinc-200 font-black uppercase text-xl tracking-tighter glow-text">
              {file ? "MATERIAL_LOCK_ACK" : "SOURCE_UPLOAD_PROTO"}
            </p>
            <p className="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em]">
              High Dynamic Range .MP4 Sequence
            </p>
          </div>
        </div>

        <input
          type="file"
          accept="video/mp4"
          className="absolute inset-0 opacity-0 cursor-pointer z-20"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        {file && (
          <div className="mt-6 flex flex-col items-center gap-2">
            <div className="bg-red-700/20 border border-red-700/50 text-red-100 text-[9px] font-black px-4 py-1.5 rounded-full uppercase tracking-widest flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-red-600 rounded-full animate-pulse" />
              {file.name}
            </div>
          </div>
        )}

        <style jsx>{`
          @keyframes scanbar {
            0% {
              top: 0;
              opacity: 0;
            }
            50% {
              opacity: 1;
            }
            100% {
              top: 100%;
              opacity: 0;
            }
          }
        `}</style>
      </div>

      {/* OPERATIONAL TRIGGER */}
      <button
        onClick={startMission}
        disabled={
          !file ||
          (status !== "idle" && status !== "completed" && status !== "failed")
        }
        className={`group relative w-full h-20 rounded-2xl font-black text-2xl uppercase tracking-tighter transition-all overflow-hidden ${
          !file ||
          (status !== "idle" && status !== "completed" && status !== "failed")
            ? "bg-zinc-900/50 text-zinc-700 border border-white/5 cursor-not-allowed"
            : "bg-white text-black hover:bg-red-700 hover:text-white red-glow active:scale-[0.98]"
        }`}
      >
        <span className="relative z-10 flex items-center justify-center gap-4">
          {status === "idle" && (
            <>
              <Radio size={24} className="animate-pulse" />
              Initiate Sequence
            </>
          )}
          {status === "analyzing" && "GEMINI: NEURAL_MAPPING..."}
          {status === "writing" && "AGENT: CONTENT_GENERATION..."}
          {status === "rendering" && "SYSTEM: FFMPEG_SYNTHESIS..."}
          {status === "completed" && "MISSION_COMPLETE"}
          {status === "failed" && "KRYTYCZNY_BŁĄD"}

          {status !== "idle" &&
            status !== "completed" &&
            status !== "failed" && (
              <Activity className="animate-spin w-6 h-6" />
            )}
        </span>
        {file && status === "idle" && (
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-black/5 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
        )}
      </button>

      {/* TERMINAL DATA STREAM */}
      <div className="glass-panel rounded-2xl overflow-hidden border border-white/5">
        <div className="bg-white/5 px-5 py-3 border-b border-white/5 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-red-700 rounded-full animate-pulse" />
            <span className="text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em] flex items-center gap-2">
              INTEL_STREAM_NODE // {jobId || "ID_PENDING"}
            </span>
          </div>
          <div className="flex gap-1">
            <div className="w-8 h-1 bg-zinc-800" />
            <div className="w-3 h-1 bg-red-900" />
          </div>
        </div>
        <div className="p-6 font-mono text-[11px] space-y-4">
          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-zinc-600">
              <span>DOCKER_NODES</span>
              <span className="text-green-500 font-bold">READY</span>
            </div>
            <div className="flex justify-between text-zinc-600">
              <span>GEMINI_LINK</span>
              <span className="text-red-700 font-bold animate-pulse">
                OPTIMIZED
              </span>
            </div>
            <div className="mt-4 pt-4 border-t border-white/5 flex flex-col gap-1">
              <span className="text-[9px] text-zinc-600 font-black uppercase tracking-widest leading-none">
                Thought_Stream:
              </span>
              <span className="text-red-500 font-black text-xs animate-pulse italic">
                {thought}
              </span>
            </div>
          </div>

          {status !== "idle" && (
            <div className="pt-4 border-t border-white/5 space-y-3">
              <div className="flex items-center gap-3">
                {status === "failed" ? (
                  <AlertCircle size={14} className="text-red-500" />
                ) : (
                  <Activity size={14} className="text-red-700 animate-spin" />
                )}
                <span
                  className={`font-black tracking-widest ${
                    status === "failed" ? "text-red-500" : "text-zinc-200"
                  }`}
                >
                  PROTOCOL_STATUS: {status.toUpperCase()}
                </span>
              </div>

              {error && (
                <div className="bg-red-900/10 border border-red-900/40 p-3 rounded-lg text-red-400 text-[10px] leading-relaxed">
                  [!] FATAL_EXCEPTION: {error}
                </div>
              )}

              {status !== "failed" && (
                <div className="w-full h-1 bg-zinc-900 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-red-700 transition-all duration-1000 ${
                      status === "analyzing"
                        ? "w-1/3"
                        : status === "writing"
                        ? "w-2/3"
                        : status === "rendering"
                        ? "w-[90%]"
                        : status === "completed"
                        ? "w-full"
                        : "w-0"
                    }`}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
