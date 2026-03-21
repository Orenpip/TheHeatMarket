/**
 * Custom webpack loader for Prisma's query_engine_bg.wasm.
 *
 * Next.js 14's bundled @webassemblyjs/wasm-parser cannot parse the Prisma
 * query engine WASM binary ("parseVec could not cast the value"). This loader
 * bypasses the parser entirely by converting the WASM binary into a JS module
 * that synchronously compiles the WASM from an inlined base64 buffer.
 */
module.exports = function (source) {
  const base64 = source.toString("base64");
  return `
    const wasmBuffer = Buffer.from("${base64}", "base64");
    const wasmModule = new WebAssembly.Module(wasmBuffer);
    module.exports = wasmModule;
    module.exports.__esModule = true;
    module.exports.default = wasmModule;
  `;
};
module.exports.raw = true;
