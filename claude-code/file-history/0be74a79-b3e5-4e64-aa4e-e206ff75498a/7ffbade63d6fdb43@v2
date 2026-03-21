import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: true, // TODO: enable once lint errors are resolved
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-XSS-Protection", value: "1; mode=block" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data: blob: https:",
              "connect-src 'self' https:",
              "font-src 'self' data:",
              "frame-ancestors 'none'",
            ].join("; "),
          },
        ],
      },
    ];
  },
  transpilePackages: ["@compass/ui", "@compass/types", "@compass/db"],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*.clerk.com",
      },
    ],
  },
  experimental: {
    optimizePackageImports: ["@compass/ui"],
    outputFileTracingRoot: path.join(__dirname, "../../"),
  },
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Custom loader for Prisma's WASM query engine.
      // Next.js 14's bundled wasm-parser can't handle this file, so we
      // bypass it by treating the .wasm as JS (inlined base64 buffer →
      // synchronous WebAssembly.Module compilation).
      config.module.rules.push({
        test: /query_engine_bg\.wasm$/,
        loader: path.resolve(__dirname, "prisma-wasm-loader.js"),
        type: "javascript/auto",
      });
    }
    return config;
  },
};

export default nextConfig;
