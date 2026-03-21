/** @type {import('next').NextConfig} */
const nextConfig = {
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
