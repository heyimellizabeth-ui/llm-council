#!/usr/bin/env python3
"""
poem_to_song.py — Expand a poem into a production-ready song via LLM Council.

Requires OPENROUTER_API_KEY in the environment or a .env file.

Usage:
    python poem_to_song.py                    # prints result to stdout
    python poem_to_song.py --output song.md   # also saves to a file
"""

import asyncio
import sys
import os
import argparse

# -- API key guard ----------------------------------------------------------
if not os.getenv("OPENROUTER_API_KEY"):
    sys.exit(
        "Error: OPENROUTER_API_KEY is not set.\n"
        "Add it to a .env file or export it before running:\n"
        "  export OPENROUTER_API_KEY=sk-or-v1-..."
    )

from backend.council import run_full_council  # noqa: E402 (import after key check)

POEM = """\
As rainy drops fell from the skies.
I tried to count as they passed by.
I walked outside and watched the sky
I walked outside and felt alive.\
"""

PROMPT = f"""\
You are a professional songwriter. Expand the following poem into a complete, \
production-ready Indie Rock song.

Original poem ("The Rainy Poem"):
---
{POEM}
---

Produce a full song with this exact structure:
- [Verse 1] — Expand the opening imagery
- [Pre-Chorus] — Build emotional tension
- [Chorus] — The central hook; anchor it on "felt alive"
- [Verse 2] — A new perspective, same world
- [Pre-Chorus]
- [Chorus]
- [Bridge] — Emotional peak or sharp shift in perspective
- [Outro] — Resolution (can reprise the chorus fragment)

After the lyrics, include:
- Suggested key and tempo (BPM)
- Chord progression for each section
- Production notes: instrumentation, dynamics, texture

Style reference: The National, Daughter, Editors — dark, textured, emotionally raw.\
"""


async def main(output_path: str | None) -> None:
    print("Running LLM Council (3 stages) — this may take 30–90 seconds...\n")

    stage1, stage2, stage3, metadata = await run_full_council(PROMPT)

    # -- Stage 1 summary -----------------------------------------------------
    print(f"Stage 1 complete: {len(stage1)} model(s) responded.")
    for r in stage1:
        preview = r["response"][:80].replace("\n", " ")
        print(f"  [{r['model']}] {preview}...")

    # -- Stage 2 summary -----------------------------------------------------
    print(f"\nStage 2 complete: {len(stage2)} peer ranking(s) collected.")
    agg = metadata.get("aggregate_rankings", [])
    if agg:
        print("  Aggregate rankings (avg position, lower = better):")
        for item in agg:
            print(f"    #{item['average_rank']:.2f}  {item['model']}")

    # -- Stage 3 (final song) ------------------------------------------------
    print("\n" + "=" * 72)
    print("FINAL SYNTHESIZED SONG")
    print("=" * 72 + "\n")

    final_song = stage3.get("response", "")
    print(final_song)

    # -- Save to file if requested -------------------------------------------
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Felt Alive — Production-Ready Indie Rock Song\n\n")
            f.write(f"*Synthesized by LLM Council (chairman: {stage3.get('model', 'unknown')})*\n\n")
            f.write("---\n\n")
            f.write(final_song)
        print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poem → production-ready song via LLM Council")
    parser.add_argument("--output", metavar="FILE", help="Save final song to this file")
    args = parser.parse_args()

    asyncio.run(main(args.output))
