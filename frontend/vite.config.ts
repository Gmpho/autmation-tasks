import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      "/health": "http://localhost:8000",
      "/ai": "http://localhost:8000",
      "/analytics": "http://localhost:8000",
      "/instagram": "http://localhost:8000",
      "/mcp": "http://localhost:8000",
    },
  },
});
