import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
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
