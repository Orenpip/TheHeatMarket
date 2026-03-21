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
};

export default nextConfig;

