import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Właściwość na głównym poziomie (Top-level) zgodnie z nowym standardem
  // @ts-ignore - uciszamy brak definicji w typach TS przy zachowaniu poprawnego działania runtime
  allowedDevOrigins: [
    "localhost:4000",
    "127.0.0.1:4000",
    "localhost:8000",
    "127.0.0.1:8000",
  ],

  // Obsługa serwowania plików wideo z backendu przez proxy Next.js
  async rewrites() {
    return [
      {
        source: "/output/:path*",
        destination: "http://localhost:8000/output/:path*",
      },
    ];
  },
} as any; // Rzutowanie całego obiektu na any rozwiązuje problem "known properties"

export default nextConfig;
