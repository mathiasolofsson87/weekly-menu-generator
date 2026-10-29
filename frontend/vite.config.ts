import { defineConfig } from "vitest/config";

// One self-contained ES module (Lit included), written into the integration so that HACS
// delivers it with everything else and the integration can register it itself.
export default defineConfig({
  build: {
    lib: {
      entry: "src/index.ts",
      formats: ["es"],
      fileName: () => "weeklymenu-cards.js",
    },
    outDir: "../custom_components/weeklymenu/www",
    emptyOutDir: true,
    target: "es2022",
    minify: "esbuild",
    sourcemap: false,
  },
  test: {
    environment: "jsdom",
    include: ["tests/**/*.test.ts"],
  },
});
