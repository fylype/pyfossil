#!/usr/bin/env python3
"""
@file plot.py
@brief Post-processing and comparison script for FOSSIL solutions against
fine-grid reference solutions and upscaling methods of the SPE 10 Model 2 benchmark (Christie & Blunt, 2001).
@details Uses the FossilPlotter class (plotter.py) to generate high-resolution figures:
  [Fine-Grid Solutions]:
  - Fig. 7: Field Oil Production Rate [STB/D]
  - Fig. 8: Producer 1 Oil Rate [STB/D]
  - Fig. 9: Producer 1 Water Cut [-]
  - Fig. 10: Field Average Pressure [psia]
  [Upscaling Methods (Christie & Blunt, 2001)]:
  - Fig. 13: Comparison of all upscaling participants for field oil rate
  - Fig. 14: Pseudo-Kr upscaling comparison for Producer 1
  - Fig. 16: Non-pseudo upscaling comparison for Producer 1
  - Fig. 19: Non-pseudo Producer 1 Water Cut
"""

import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from plotter import FossilPlotter

def main():
    print("=" * 76)
    print("  FOSSIL: SPE 10 MODEL 2 BENCHMARK & UPSCALING COMPARISON (CHRISTIE, 2001)")
    print("=" * 76)

    output_dir = script_dir / "output_spe10_3d"
    if not output_dir.exists():
        output_dir = script_dir / "output_spe10_unstructured_3d"
    benchmark_dir = script_dir / "Benchmark"
    save_dir = script_dir / "benchmark_comparison"

    if not output_dir.exists():
        print(f"\n[ERROR] Simulation output directory not found: {output_dir}")
        print("Run the simulation first (run_spe10_3d.py or run_spe10_unstructured_3d.py).")
        return

    print(f"Simulation Directory : {output_dir}")
    print(f"Benchmark Directory  : {benchmark_dir}")
    print(f"Plot Save Directory  : {save_dir}\n")

    plotter = FossilPlotter(str(output_dir), dim=3, use_tex=False)

    print("Generating comparative plots against SPE 10 benchmark reference curves...")
    saved_files = plotter.plot_spe10_benchmark_comparison(
        benchmark_dir=str(benchmark_dir) if benchmark_dir.exists() else None,
        save_dir=str(save_dir),
        create_4panel=True,
        create_individual=True,
        include_upscaling=True,
        fossil_label="FOSSIL"
    )

    print(f"\n[SUCCESS] Generated {len(saved_files)} publication-ready figures in:")
    print(f"  {save_dir.resolve()}")

if __name__ == "__main__":
    main()
