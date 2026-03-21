/** @type {import('next').NextConfig} */
// Rebuild with env vars
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
  },
};

export default nextConfig;
