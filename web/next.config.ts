import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: [
    "localhost:4000",
    "127.0.0.1:4000",
    "localhost:8000",
    "127.0.0.1:8000",
  ],

  async rewrites() {
    return [
      {
        source: "/output/:path*",
        destination: "http://localhost:8000/output/:path*",
      },
    ];
  },
} as any;

export default nextConfig;
