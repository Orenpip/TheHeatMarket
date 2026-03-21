import type { Config } from "tailwindcss";
import baseConfig from "@compass/config/tailwind";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "../../packages/ui/src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      ...(baseConfig.theme?.extend ?? {}),
    },
  },
  plugins: [],
};

export default config;
