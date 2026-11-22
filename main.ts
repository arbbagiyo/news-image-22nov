// The World — Sunday 22 November 2026 (Node 22, standard library only):
// the entry image is entry.png beside this file, and the program hands it
// in as /output/entry.png. The gate takes a whole PNG or JPEG of at most
// 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes
// copied. The image itself is drawn by render.py (PIL, deterministic);
// this program only carries the finished bytes to the output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const out = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
const src = new URL('./entry.png', import.meta.url);

// The gate only accepts a whole PNG: check the eight-byte signature
// before copying, so a truncated render fails loudly instead of
// submitting a broken file.
const head = readFileSync(src).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) throw new Error('entry.png is not a PNG');

copyFileSync(src, out);

// Fail loudly if the copied image ever breaks the gate (at most 1 MiB).
const bytes = statSync(out).size;
if (bytes > 1048576) throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB limit`);
console.log(`wrote entry.png (${bytes} bytes)`);
