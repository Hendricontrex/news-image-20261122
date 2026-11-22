import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for news-image-20261122: copy the composed front page
// (entry.png, drawn by compose.py) into the grader's output directory.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst}`);
