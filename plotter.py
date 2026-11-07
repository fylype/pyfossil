"""
@file plotter.py
@ingroup group_pybind
@brief Publication-quality 1D, 2D, and 3D visualization engine for FOSSIL simulation data.
@details Provides the FossilPlotter class for automated ParaView/VTU postprocessing,
time-series history extraction, 1D spatial profile extraction, and PyVista off-screen rendering.
"""

import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pyvista as pv
import pandas as pd
from pathlib import Path


class FossilPlotter:
    """
    @ingroup group_pybind
    @brief Unified postprocessing and visualization manager for FOSSIL simulation results.
    @details Capable of rendering 1D cross-sectional profiles, production history curves,
    and 2D/3D PyVista spatial field distributions directly from output directories.
    """
    def __init__(self, output_dir: str, dim: int = 3, style: str = 'seaborn-v0_8-whitegrid', use_tex: bool = True):
        """
        @brief Initialize the FossilPlotter with directory paths and Matplotlib styling.
        @param output_dir Path to the simulation output directory.
        @param dim Spatial dimension of the simulation (2 or 3).
        @param style Matplotlib stylesheet name.
        @param use_tex Whether to enable LaTeX font rendering if LaTeX is available.
        """
        self.output_dir = Path(output_dir)
        self.dim = dim

        if not self.output_dir.exists():
            raise FileNotFoundError(f"Directory {output_dir} was not found.")

        plt.style.use(style)

        tex_available = use_tex and (shutil.which("latex") is not None)
        plt.rcParams.update({
            "text.usetex": tex_available,
            "font.family": "sans-serif",
            "mathtext.fontset": "cm",
            "axes.edgecolor": "black",
            "axes.linewidth": 0.8,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
        })

        self.default_figsize = (7, 5)
        self.fontsize_labels = 16
        self.fontsize_ticks = 14
        self.fontsize_legend = 13
        self.linewidth = 2.5

        self.colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']
        self.linestyles = [':', '-.', '--', (0, (3, 1, 1, 1)), '-', (0, (5, 1))]
        self.markers = ['o', 's', '^', 'D', 'v', '*']

    def _apply_standard_formatting(self, ax, xlabel, ylabel, scientific_notation=False, xlim=None, ylim=None):
        ax.set_xlabel(xlabel, fontsize=self.fontsize_labels)
        ax.set_ylabel(ylabel, fontsize=self.fontsize_labels)

        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(0.8)

        ax.tick_params(axis='both', which='major', labelsize=self.fontsize_ticks,
                       direction='out', bottom=True, left=True, top=False, right=False)
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.margins(x=0)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        if scientific_notation:
            formatter = ticker.ScalarFormatter(useMathText=True)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-1, 1))
            ax.yaxis.set_major_formatter(formatter)
            ax.xaxis.set_major_formatter(formatter)

    def _apply_top_legend(self, ax, ncol='auto'):
        handles, labels = ax.get_legend_handles_labels()
        n_items = len(labels)
        if n_items == 0:
            return

        if ncol == 'auto' or ncol is None:
            if n_items <= 2:
                ncol = n_items
            elif n_items <= 4:
                ncol = 2
            elif n_items <= 6:
                ncol = 3
            else:
                ncol = 4

        if n_items <= 3:
            fs = self.fontsize_legend
        elif n_items <= 6:
            fs = min(self.fontsize_legend, 11)
        else:
            fs = min(self.fontsize_legend, 9.5)

        ax.legend(
            bbox_to_anchor=(0.5, 1.02),
            loc='lower center',
            ncol=ncol,
            borderaxespad=0.0,
            frameon=True,
            fancybox=True,
            facecolor="white",
            edgecolor="#cccccc",
            framealpha=0.95,
            fontsize=fs,
            handlelength=2.0,
            columnspacing=1.2,
            borderpad=0.4
        )

    def get_vtu_files(self, prefix: str = "volume_vars_"):
        files = list(self.output_dir.glob(f"{prefix}*.vtu"))
        if not files and (self.output_dir / "output").exists():
            files = list((self.output_dir / "output").glob(f"{prefix}*.vtu"))
        if not files:
            print(f"Warning: No files with prefix '{prefix}' found in {self.output_dir}")
            return []
        files.sort(key=lambda f: int(f.stem.split('_')[-1]))
        return files

    # =========================================================================
    # 1. PLOTS TEMPORAIS (CSV / DAT)
    # =========================================================================
    def plot_history(self, filename: str, col_x: str, cols_y: list, xlabel: str, ylabel: str,
                     labels: list = None, save_as: str = None, semilog_y: bool = False,
                     legend_ncol='auto', xlim: tuple = None, ylim: tuple = None):
        file_path = self.output_dir / filename
        df = pd.read_csv(file_path, sep=r'\s+')

        fig, ax = plt.subplots(figsize=self.default_figsize)

        for i, col in enumerate(cols_y):
            if col not in df.columns:
                continue

            ls = self.linestyles[i % len(self.linestyles)]
            color = self.colors[i % len(self.colors)]
            curve_label = labels[i] if (labels is not None and i < len(labels)) else col

            if semilog_y:
                ax.semilogy(df[col_x], df[col], linewidth=self.linewidth, linestyle=ls, color=color, label=curve_label)
            else:
                ax.plot(df[col_x], df[col], linewidth=self.linewidth, linestyle=ls, color=color, label=curve_label)

        self._apply_standard_formatting(ax, xlabel, ylabel, xlim=xlim, ylim=ylim)
        self._apply_top_legend(ax, ncol=legend_ncol)

        if save_as:
            save_path = Path(save_as) if Path(save_as).is_absolute() else (self.output_dir / save_as)
            fig.savefig(save_path, bbox_inches='tight', pad_inches=0.05, dpi=300)
        plt.close(fig)

    # =========================================================================
    # 2. PLOTS ESPACIAIS 1D (Matplotlib Clássico)
    # =========================================================================
    def plot_spatial_1d(self, target_variable: str, time_steps: list, xlabel: str, ylabel: str,
                        labels: list = None, prefix: str = "volume_vars_", save_as: str = None,
                        use_cell_centers: bool = True, show_markers: bool = False,
                        legend_ncol='auto', xlim: tuple = None, ylim: tuple = None):
        vtu_files = self.get_vtu_files(prefix)
        if not vtu_files:
            return

        fig, ax = plt.subplots(figsize=self.default_figsize)

        for i, t_step in enumerate(time_steps):
            if t_step >= len(vtu_files):
                continue

            mesh = pv.read(vtu_files[t_step])
            if target_variable not in mesh.point_data:
                continue

            if use_cell_centers:
                cell_mesh = mesh.point_data_to_cell_data()
                centers = cell_mesh.cell_centers()
                x_coords = centers.points[:, 0]
                field_data = centers.point_data[target_variable]
            else:
                x_coords = mesh.points[:, 0]
                field_data = mesh.point_data.get(target_variable)

            sort_idx = np.argsort(x_coords)
            x_sorted = x_coords[sort_idx]
            field_sorted = field_data[sort_idx]

            ls = self.linestyles[i % len(self.linestyles)]
            color = self.colors[i % len(self.colors)]
            marker = self.markers[i % len(self.markers)] if show_markers else None
            curve_label = labels[i] if (labels is not None and i < len(labels)) else f"Step {t_step}"

            ax.plot(
                x_sorted, field_sorted,
                linewidth=self.linewidth,
                linestyle=ls,
                color=color,
                marker=marker,
                markersize=6 if show_markers else 0,
                markevery=max(1, len(x_sorted) // 20) if show_markers else None,
                label=curve_label
            )

        self._apply_standard_formatting(ax, xlabel, ylabel, xlim=xlim, ylim=ylim)
        self._apply_top_legend(ax, ncol=legend_ncol)

        if save_as:
            save_path = Path(save_as) if Path(save_as).is_absolute() else (self.output_dir / save_as)
            fig.savefig(save_path, bbox_inches='tight', pad_inches=0.05, dpi=300)
        plt.close(fig)

    # =========================================================================
    # 3. MAPA ESPACIAL UNIVERSAL (2D Vetorial sem margens / 3D Otimizado Limpo)
    # =========================================================================
    def plot_spatial_mesh(self, target_variable: str, time_step: int,
                          prefix: str = "volume_vars_", cmap: str = 'jet_r',
                          limits: tuple = None, save_as: str = "spatial_mesh.pdf",
                          z_scale: float = 1.0, show_edges: bool = False, cpos=None):
        """
        Generates clean spatial maps without white margins.
        In 3D, positions the camera to ensure the X-axis flows left-to-right,
        with automated framing.
        """
        vtu_files = self.get_vtu_files(prefix)
        if not vtu_files or time_step >= len(vtu_files):
            print(f"Error: Step {time_step} file not found.")
            return

        save_path = Path(save_as) if Path(save_as).is_absolute() else (self.output_dir / save_as)
        mesh = pv.read(vtu_files[time_step])
        
        if target_variable not in mesh.point_data and target_variable not in mesh.cell_data:
            print(f"Variable '{target_variable}' not found in file.")
            return

        vmin, vmax = limits if limits else (
            mesh.point_data[target_variable].min() if target_variable in mesh.point_data else mesh.cell_data[target_variable].min(),
            mesh.point_data[target_variable].max() if target_variable in mesh.point_data else mesh.cell_data[target_variable].max()
        )

        # ---------------------------------------------------------------------
        # CASO 2D: Renderização Vetorial Limpa (Sem margens laterais)
        # ---------------------------------------------------------------------
        if self.dim == 2:
            surf = mesh.extract_surface(algorithm='dataset_surface').triangulate()
            x = surf.points[:, 0]
            y = surf.points[:, 1]

            if target_variable in surf.point_data:
                field_data = surf.point_data[target_variable]
            elif target_variable in surf.cell_data:
                field_data = surf.cell_data[target_variable]
            else:
                point_mesh = mesh.cell_data_to_point_data()
                field_data = point_mesh.point_data[target_variable]
                x = point_mesh.points[:, 0]
                y = point_mesh.points[:, 1]
                surf = point_mesh.extract_surface(algorithm='dataset_surface').triangulate()

            faces = surf.faces.reshape(-1, 4)[:, 1:4]

            fig = plt.figure(figsize=self.default_figsize, frameon=False)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_axis_off()

            ax.tripcolor(x, y, faces, field_data, cmap=cmap, vmin=vmin, vmax=vmax,
                         shading='flat', edgecolors='gray' if show_edges else 'face',
                         linewidth=0.15 if show_edges else 0)
            
            ax.set_xlim(x.min(), x.max())
            ax.set_ylim(y.min(), y.max())
            ax.set_aspect('equal', adjustable='box')

            fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=300, transparent=True)
            plt.close(fig)
            print(f"Clean 2D vector map saved to: {save_path}")

        # ---------------------------------------------------------------------
        # 3D CASE: True 3D Rendering converted to PDF / PNG
        # ---------------------------------------------------------------------
        elif self.dim == 3:
            if z_scale != 1.0:
                mesh.points[:, 2] *= z_scale

            plotter = pv.Plotter(off_screen=True, window_size=(1600, 1200))
            
            plotter.add_mesh(mesh, scalars=target_variable, cmap=cmap, clim=(vmin, vmax),
                             show_edges=show_edges, edge_color='gray', opacity=1.0,
                             lighting=False, show_scalar_bar=False)
            
            plotter.hide_axes()
            plotter.background_color = "white"

            if cpos is None:
                bounds = mesh.bounds
                x_mid = (bounds[0] + bounds[1]) / 2.0
                y_mid = (bounds[2] + bounds[3]) / 2.0
                z_mid = (bounds[4] + bounds[5]) / 2.0
                
                # Identify largest dimension of reservoir (including z_scale)
                max_dim = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
                
                # Position camera in isometric view
                plotter.camera_position = [
                    (x_mid - max_dim * 1.5, y_mid - max_dim * 1.5, z_mid + max_dim * 1.5), 
                    (x_mid, y_mid, z_mid),                                                 
                    (0, 0, 1)                                                              
                ]
                
                # Framing and subtle zoom
                plotter.reset_camera()
                plotter.camera.zoom(1.1)
            else:
                plotter.camera_position = cpos

            target_ext = save_path.suffix.lower()
            if target_ext == '.pdf':
                temp_png = save_path.with_suffix('.png')
                plotter.screenshot(temp_png, transparent_background=True)
                plotter.close()
                
                fig_pdf, ax_pdf = plt.subplots(figsize=(8, 6), frameon=False)
                ax_pdf.set_axis_off()
                ax_pdf.imshow(plt.imread(temp_png))
                fig_pdf.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=300, transparent=True)
                plt.close(fig_pdf)
                temp_png.unlink()
            else:
                plotter.screenshot(save_path, transparent_background=True)
                plotter.close()

            print(f"Clean 3D map saved to: {save_path}")

    # =========================================================================
    # 4. ISOLATED COLORBAR
    # =========================================================================
    def plot_isolated_colorbar(self, label_name: str, cmap: str = 'jet_r',
                               limits: tuple = (0.0, 1.0), save_as: str = "colorbar.pdf",
                               orientation: str = 'horizontal'):
        """
        Generates an isolated colorbar with top-positioned ticks and labels for horizontal mode.
        """
        fig, ax = plt.subplots(figsize=(6, 0.6) if orientation == 'horizontal' else (1.2, 5))
        
        norm = plt.Normalize(vmin=limits[0], vmax=limits[1])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        cbar = fig.colorbar(sm, cax=ax, orientation=orientation, fraction=1.0, pad=0.0)
        
        if orientation == 'horizontal':
            # Joga os ticks numéricos para a parte superior
            cbar.ax.xaxis.set_ticks_position('top')
            cbar.ax.xaxis.set_label_position('top')
            # Título no topo e ticks apontando para fora
            cbar.set_label(label_name, fontsize=self.fontsize_labels, labelpad=8)
            cbar.ax.tick_params(labelsize=self.fontsize_ticks, direction='out', length=6, width=1.2)
        else:
            cbar.ax.set_title(label_name, fontsize=self.fontsize_labels - 2, pad=12, weight='normal', loc='center')
            cbar.ax.tick_params(labelsize=self.fontsize_ticks, direction='out', length=6, width=1.2)

        save_path = Path(save_as) if Path(save_as).is_absolute() else (self.output_dir / save_as)
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0.02, dpi=300, transparent=True)
        plt.close(fig)
        print(f"Isolated colorbar saved to: {save_path}")

    # =========================================================================
    # 5. SPE 10 BENCHMARK COMPARISONS (CHRISTIE & BLUNT, 2001)
    # =========================================================================
    def plot_spe10_benchmark_comparison(self, benchmark_dir: str = None, save_dir: str = None,
                                        create_4panel: bool = True, create_individual: bool = True,
                                        include_upscaling: bool = True,
                                        fossil_label: str = "FOSSIL"):
        """
        @brief Generates comparative plots of FOSSIL solutions against the SPE 10 fine-grid and upscaling benchmarks.
        @details Reproduces the benchmark comparisons from Christie & Blunt (2001):
          - Fig. 7: Field Oil Production Rate [STB/D]
          - Fig. 8: Producer 1 Oil Production Rate [STB/D]
          - Fig. 9: Producer 1 Water Cut [-]
          - Fig. 10: Field Average Pressure [psia]
          - Fig. 13: All Upscaled Field Oil Production Rate [STB/D]
          - Fig. 14: Pseudo-based Upscaled Producer 1 Oil Rate [STB/D]
          - Fig. 16: Non-pseudo Upscaled Producer 1 Oil Rate [STB/D]
          - Fig. 19: Non-pseudo Upscaled Producer 1 Water Cut [-]
        @param benchmark_dir Directory containing benchmark CSV files.
        @param save_dir Directory to save generated plot images.
        @param create_4panel Whether to generate 4-panel composite figures.
        @param create_individual Whether to generate individual publication-quality figures.
        @param include_upscaling Whether to include upscaling benchmark comparisons.
        @param fossil_label Legend label used to identify the FOSSIL curve.
        @return List of paths to generated image files.
        """
        bench_path = Path(benchmark_dir) if benchmark_dir else (self.output_dir.parent / "Benchmark")
        master_csv = bench_path / "spe10_model2_finegrid_unified_reference.csv"
        if not master_csv.exists():
            raise FileNotFoundError(f"Benchmark master file not found at: {master_csv}")

        df_bench = pd.read_csv(master_csv)

        target_dir = Path(save_dir) if save_dir else (self.output_dir / "benchmark_comparison")
        target_dir.mkdir(parents=True, exist_ok=True)

        BBL_TO_M3 = 0.158987294928
        M3_S_TO_STBD = 1.0 / 1.84013e-6
        PSI_TO_PA = 6894.757

        # ---------------------------------------------------------------------
        # 1. Load FOSSIL production data
        # ---------------------------------------------------------------------
        prod_file = self.output_dir / "production.dat"
        if not prod_file.exists():
            raise FileNotFoundError(f"production.dat not found in {self.output_dir}")

        with open(prod_file, "r") as f:
            cols_prod = f.readline().lstrip("#").strip().split()
        df_prod = pd.read_csv(prod_file, sep=r"\s+", comment="#", names=cols_prod)
        t_days_prod = df_prod["Time_[s]"] / 86400.0

        # In FOSSIL SPE 10 setup, oil is the non-wetting phase (mapped as Gas)
        q_oil_field_stbd = df_prod["Gas_Prod_Flow_Rate_[m3/s]"] * M3_S_TO_STBD

        # ---------------------------------------------------------------------
        # 2. Load FOSSIL well data (BHP and bottomhole rates)
        # ---------------------------------------------------------------------
        bhp_file = self.output_dir / "bhp.dat"
        if not bhp_file.exists():
            raise FileNotFoundError(f"bhp.dat not found in {self.output_dir}")

        with open(bhp_file, "r") as f:
            cols_bhp = f.readline().lstrip("#").strip().split()
        df_bhp = pd.read_csv(bhp_file, sep=r"\s+", comment="#", names=cols_bhp)
        t_days_bhp = df_bhp["Time_[s]"] / 86400.0

        q_oil_p1_stbd = np.abs(df_bhp["P1_Qg_[m3/s]"]) * M3_S_TO_STBD
        q_water_p1 = np.abs(df_bhp["P1_Qw_[m3/s]"])
        q_tot_p1 = q_water_p1 + np.abs(df_bhp["P1_Qg_[m3/s]"])
        p1_wcut = np.where(q_tot_p1 > 1e-15, q_water_p1 / q_tot_p1, 0.0)

        # ---------------------------------------------------------------------
        # 3. Load / Extract FOSSIL average field pressure
        # ---------------------------------------------------------------------
        p_avg_cache = self.output_dir / "pressure_history_extracted.csv"
        p_drop_file = self.output_dir / "pressure_drop.dat"

        # Check if extracted cache is older than simulation files
        cache_is_stale = False
        if p_avg_cache.exists() and prod_file.exists():
            if p_avg_cache.stat().st_mtime < prod_file.stat().st_mtime:
                cache_is_stale = True

        if p_drop_file.exists():
            with open(p_drop_file, "r") as f:
                cols_p = f.readline().lstrip("#").strip().split()
            df_p = pd.read_csv(p_drop_file, sep=r"\s+", comment="#", names=cols_p)
            t_days_press = df_p["Time_[s]"] / 86400.0
            p_avg_psia = df_p["P_avg_[Pa]"] / PSI_TO_PA
        elif p_avg_cache.exists() and not cache_is_stale:
            df_p = pd.read_csv(p_avg_cache)
            t_days_press = df_p["Time_Days"]
            p_avg_psia = df_p["Pressure_psia"]
        else:
            vtu_files = self.get_vtu_files()
            if not vtu_files:
                vtu_dir = self.output_dir / "output"
                vtu_files = sorted(vtu_dir.glob("volume_vars_*.vtu"), key=lambda f: int(f.stem.split("_")[-1]))
            if vtu_files:
                times_p = []
                p_psia_list = []
                for vf in vtu_files:
                    mesh = pv.read(vf)
                    t_sec = mesh.field_data.get("TIME")[0] if "TIME" in mesh.field_data else 0.0
                    times_p.append(t_sec / 86400.0)
                    p_arr = mesh.point_data.get("Pressure")
                    if p_arr is None:
                        p_arr = mesh.point_data.get("Gas_Pressure")
                    p_psia_list.append(float(np.mean(p_arr)) / PSI_TO_PA)
                t_days_press = np.array(times_p)
                p_avg_psia = np.array(p_psia_list)
                pd.DataFrame({"Time_Days": t_days_press, "Pressure_psia": p_avg_psia}).to_csv(p_avg_cache, index=False)
            else:
                t_days_press = np.array([0.0, 2000.0])
                p_avg_psia = np.array([6000.0, 6000.0])

        saved_files = []

        # Benchmark participant line styles
        bench_styles = {
            "Landmark": {"color": "#1f77b4", "ls": "--", "lw": 1.6, "label": "Landmark (Fine Grid)"},
            "GeoQuest": {"color": "#2ca02c", "ls": "-.", "lw": 1.6, "label": "GeoQuest (Streamline)"},
            "Chevron":  {"color": "#d62728", "ls": ":",  "lw": 1.8, "label": "Chevron (Fine Grid)"},
            "StreamSim":{"color": "#9467bd", "ls": (0, (3, 1, 1, 1)), "lw": 1.6, "label": "StreamSim (3DSL)"}
        }
        fossil_style = {"color": "#ff7f0e", "ls": "-", "lw": 2.8, "label": fossil_label}

        # ---------------------------------------------------------------------
        # A. UNIFIED 4-PANEL COMPOSITE (FINE GRID)
        # ---------------------------------------------------------------------
        if create_4panel:
            fig, axs = plt.subplots(2, 2, figsize=(14, 11), dpi=300)

            # --- Panel (a): Fig. 7 - Field Oil Rate ---
            ax = axs[0, 0]
            for name, st in bench_styles.items():
                col = f"Field_Oil_Rate_{name}_STBD"
                ax.plot(df_bench["Time_Days"], df_bench[col], color=st["color"], linestyle=st["ls"],
                        linewidth=st["lw"], label=st["label"])
            ax.plot(t_days_prod, q_oil_field_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                    linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=5)
            self._apply_standard_formatting(ax, "Time (days)", "Field Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 6000))
            ax.set_title("(a) Field Oil Production Rate (Fig. 7)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)

            # --- Panel (b): Fig. 8 - Producer 1 Oil Rate ---
            ax = axs[0, 1]
            for name, st in bench_styles.items():
                col = f"P1_Oil_Rate_{name}_STBD"
                ax.plot(df_bench["Time_Days"], df_bench[col], color=st["color"], linestyle=st["ls"],
                        linewidth=st["lw"], label=st["label"])
            ax.plot(t_days_bhp, q_oil_p1_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                    linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=5)
            self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 1000))
            ax.set_title("(b) Producer 1 Oil Rate (Fig. 8)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)

            # --- Panel (c): Fig. 9 - Producer 1 Water Cut ---
            ax = axs[1, 0]
            for name, st in bench_styles.items():
                col = f"P1_Water_Cut_{name}"
                ax.plot(df_bench["Time_Days"], df_bench[col], color=st["color"], linestyle=st["ls"],
                        linewidth=st["lw"], label=st["label"])
            ax.plot(t_days_bhp, p1_wcut, color=fossil_style["color"], linestyle=fossil_style["ls"],
                    linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=5)
            self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Water Cut (-)", xlim=(0, 2000), ylim=(0, 0.8))
            ax.set_title("(c) Producer 1 Water Cut (Fig. 9)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)

            # --- Panel (d): Fig. 10 - Field Average Pressure ---
            ax = axs[1, 1]
            for name, st in bench_styles.items():
                col = f"Field_Avg_Pressure_{name}_psia"
                ax.plot(df_bench["Time_Days"], df_bench[col], color=st["color"], linestyle=st["ls"],
                        linewidth=st["lw"], label=st["label"])
            ax.plot(t_days_press, p_avg_psia, color=fossil_style["color"], linestyle=fossil_style["ls"],
                    linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=5)
            p_max_plot = max(7500.0, float(np.max(p_avg_psia)) * 1.05)
            self._apply_standard_formatting(ax, "Time (days)", "Field Average Pressure (psia)", xlim=(0, 2000), ylim=(4000, p_max_plot))
            ax.set_title("(d) Field Average Pressure (Fig. 10)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)

            # Unified legend for the entire figure (all 4 panels share the exact same models)
            handles, labels = axs[0, 0].get_legend_handles_labels()
            fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.985),
                       ncol=5, frameon=True, fancybox=True, facecolor="white", edgecolor="#cccccc",
                       framealpha=0.95, fontsize=11.5, handlelength=2.2, columnspacing=1.8, borderpad=0.5)

            fig.subplots_adjust(top=0.91, bottom=0.07, left=0.08, right=0.98, hspace=0.28, wspace=0.22)
            out_4panel = target_dir / "spe10_finegrid_vs_fossil_4panel.png"
            fig.savefig(out_4panel, bbox_inches="tight", dpi=300)
            plt.close(fig)
            saved_files.append(out_4panel)

        # ---------------------------------------------------------------------
        # B. INDIVIDUAL PUBLICATION-QUALITY FIGURES
        # ---------------------------------------------------------------------
        if create_individual:
            individual_configs = [
                {
                    "title": "(Fig. 7) Field Oil Production Rate - SPE 10 Model 2",
                    "ylabel": "Field Oil Rate (STB/D)",
                    "b_col": "Field_Oil_Rate_{}_STBD",
                    "f_t": t_days_prod,
                    "f_v": q_oil_field_stbd,
                    "xlim": (0, 2000),
                    "ylim": (0, 6000),
                    "filename": "fig07_field_oil_rate_comparison.png"
                },
                {
                    "title": "(Fig. 8) Producer 1 Oil Production Rate - SPE 10 Model 2",
                    "ylabel": "Producer 1 Oil Rate (STB/D)",
                    "b_col": "P1_Oil_Rate_{}_STBD",
                    "f_t": t_days_bhp,
                    "f_v": q_oil_p1_stbd,
                    "xlim": (0, 2000),
                    "ylim": (0, 1000),
                    "filename": "fig08_producer1_oil_rate_comparison.png"
                },
                {
                    "title": "(Fig. 9) Producer 1 Water Cut - SPE 10 Model 2",
                    "ylabel": "Producer 1 Water Cut (-)",
                    "b_col": "P1_Water_Cut_{}",
                    "f_t": t_days_bhp,
                    "f_v": p1_wcut,
                    "xlim": (0, 2000),
                    "ylim": (0, 0.8),
                    "filename": "fig09_producer1_water_cut_comparison.png"
                },
                {
                    "title": "(Fig. 10) Field Average Pressure - SPE 10 Model 2",
                    "ylabel": "Field Average Pressure (psia)",
                    "b_col": "Field_Avg_Pressure_{}_psia",
                    "f_t": t_days_press,
                    "f_v": p_avg_psia,
                    "xlim": (0, 2000),
                    "ylim": (4000, max(7500.0, float(np.max(p_avg_psia)) * 1.05)),
                    "filename": "fig10_field_avg_pressure_comparison.png"
                }
            ]

            for cfg in individual_configs:
                fig, ax = plt.subplots(figsize=(8.5, 5.8), dpi=300)
                for name, st in bench_styles.items():
                    col = cfg["b_col"].format(name)
                    ax.plot(df_bench["Time_Days"], df_bench[col], color=st["color"], linestyle=st["ls"],
                            linewidth=st["lw"], label=st["label"])
                ax.plot(cfg["f_t"], cfg["f_v"], color=fossil_style["color"], linestyle=fossil_style["ls"],
                        linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=5)

                self._apply_standard_formatting(ax, "Time (days)", cfg["ylabel"], xlim=cfg["xlim"], ylim=cfg["ylim"])
                fig.suptitle(cfg["title"], fontsize=self.fontsize_labels - 1, fontweight="bold", y=0.985)
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(
                    handles, labels,
                    loc='lower center',
                    bbox_to_anchor=(0.5, 1.01),
                    ncol=3,
                    frameon=True,
                    fancybox=True,
                    facecolor="white",
                    edgecolor="#cccccc",
                    fontsize=11,
                    handlelength=2.0,
                    columnspacing=1.4,
                    borderpad=0.4
                )
                fig.tight_layout(rect=[0, 0, 1, 0.90])

                save_p = target_dir / cfg["filename"]
                fig.savefig(save_p, bbox_inches="tight", dpi=300)
                plt.close(fig)
                saved_files.append(save_p)

        # ---------------------------------------------------------------------
        # C. COMPARISON WITH UPSCALING RESULTS (CHRISTIE & BLUNT, 2001)
        # ---------------------------------------------------------------------
        if include_upscaling:
            fig13_csv = bench_path / "spe10_model2_all_upscaled_field_oil_rate.csv"
            fig14_csv = bench_path / "spe10_model2_producer1_oil_rate_pseudo.csv"
            fig16_csv = bench_path / "spe10_model2_producer1_oil_rate_nonpseudo.csv"
            fig19_csv = bench_path / "spe10_model2_producer1_water_cut_nonpseudo.csv"

            df_fig13 = pd.read_csv(fig13_csv) if fig13_csv.exists() else None
            df_fig14 = pd.read_csv(fig14_csv) if fig14_csv.exists() else None
            df_fig16 = pd.read_csv(fig16_csv) if fig16_csv.exists() else None
            df_fig19 = pd.read_csv(fig19_csv) if fig19_csv.exists() else None

            up_styles = {
                "TotalFinaElf":      {"color": "#17becf", "ls": "--", "lw": 1.4, "label": "TotalFinaElf"},
                "Landmark":          {"color": "#1f77b4", "ls": "-.", "lw": 1.4, "label": "Landmark"},
                "GeoQuest":          {"color": "#2ca02c", "ls": ":",  "lw": 1.6, "label": "GeoQuest"},
                "Phillips":          {"color": "#bcbd22", "ls": "--", "lw": 1.4, "label": "Phillips"},
                "StreamSim":         {"color": "#9467bd", "ls": "-.", "lw": 1.4, "label": "StreamSim"},
                "Roxar":             {"color": "#8c564b", "ls": ":",  "lw": 1.6, "label": "Roxar"},
                "Coats":             {"color": "#7f7f7f", "ls": "--", "lw": 1.4, "label": "Coats"},
                "Chevron":           {"color": "#d62728", "ls": "-.", "lw": 1.6, "label": "Chevron"},
                "BP":                {"color": "#e377c2", "ls": ":",  "lw": 1.6, "label": "BP"},
                "Landmark_Upscaled": {"color": "#1f77b4", "ls": "-.", "lw": 1.4, "label": "Landmark (Upscaled)"},
                "FineGrid_Ref":      {"color": "black",   "ls": "-",  "lw": 1.5, "label": "Fine Grid Ref (Landmark)"}
            }

            # 1. UPSCALING 4-PANEL COMPOSITE (2x2)
            if create_4panel and (df_fig13 is not None or df_fig16 is not None):
                fig_up, axs_up = plt.subplots(2, 2, figsize=(15, 12), dpi=300)

                # --- (a) Fig. 13: All Upscaled Field Oil Rate ---
                ax = axs_up[0, 0]
                if df_fig13 is not None:
                    if "Field_Oil_Rate_Landmark_STBD" in df_bench:
                        ax.plot(df_bench["Time_Days"], df_bench["Field_Oil_Rate_Landmark_STBD"],
                                color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                                linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "Landmark", "GeoQuest", "Phillips", "StreamSim", "Roxar", "Coats", "Chevron"]:
                        col = f"{part}_STB_D"
                        if col in df_fig13:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig13["Time_Days"], df_fig13[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                ax.plot(t_days_prod, q_oil_field_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                        linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                self._apply_standard_formatting(ax, "Time (days)", "Field Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 6000))
                ax.set_title("(a) All Upscaled Field Oil Rate (Fig. 13)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)
                ax.legend(loc='upper right', ncol=2, fontsize=8.5, frameon=True, fancybox=True,
                          facecolor="white", edgecolor="#cccccc", framealpha=0.92,
                          handlelength=1.8, columnspacing=0.8, borderpad=0.3)

                # --- (b) Fig. 16: Non-pseudo Upscaled Producer 1 Oil Rate ---
                ax = axs_up[0, 1]
                if df_fig16 is not None:
                    ax.plot(df_fig16["Time_Days"], df_fig16["FineGrid_Landmark_STB_D"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "GeoQuest", "BP", "Roxar", "Chevron"]:
                        col = f"{part}_STB_D"
                        if col in df_fig16:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig16["Time_Days"], df_fig16[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                ax.plot(t_days_bhp, q_oil_p1_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                        linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 1000))
                ax.set_title("(b) Non-pseudo Upscaled P1 Oil Rate (Fig. 16)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)
                ax.legend(loc='upper right', ncol=2, fontsize=8.5, frameon=True, fancybox=True,
                          facecolor="white", edgecolor="#cccccc", framealpha=0.92,
                          handlelength=1.8, columnspacing=0.8, borderpad=0.3)

                # --- (c) Fig. 14: Pseudo-based Upscaled Producer 1 Oil Rate ---
                ax = axs_up[1, 0]
                if df_fig14 is not None:
                    ax.plot(df_fig14["Time_Days"], df_fig14["FineGrid_Landmark_STB_D"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part, col in [("Landmark_Upscaled", "Landmark_Upscaled_STB_D"), ("Phillips", "Phillips_STB_D"), ("Coats", "Coats_STB_D")]:
                        if col in df_fig14:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig14["Time_Days"], df_fig14[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                ax.plot(t_days_bhp, q_oil_p1_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                        linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 1000))
                ax.set_title("(c) Pseudo-based Upscaled P1 Oil Rate (Fig. 14)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)
                ax.legend(loc='upper right', ncol=1, fontsize=9.0, frameon=True, fancybox=True,
                          facecolor="white", edgecolor="#cccccc", framealpha=0.92,
                          handlelength=1.8, columnspacing=0.8, borderpad=0.3)

                # --- (d) Fig. 19: Non-pseudo Upscaled Producer 1 Water Cut ---
                ax = axs_up[1, 1]
                if df_fig19 is not None:
                    ax.plot(df_fig19["Time_Days"], df_fig19["FineGrid_Landmark"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "GeoQuest", "BP", "Roxar", "Chevron"]:
                        if part in df_fig19:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig19["Time_Days"], df_fig19[part], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                ax.plot(t_days_bhp, p1_wcut, color=fossil_style["color"], linestyle=fossil_style["ls"],
                        linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Water Cut (-)", xlim=(0, 2000), ylim=(0, 0.8))
                ax.set_title("(d) Non-pseudo Upscaled P1 Water Cut (Fig. 19)", fontsize=self.fontsize_labels - 2, fontweight="bold", pad=8)
                ax.legend(loc='upper left', ncol=2, fontsize=8.5, frameon=True, fancybox=True,
                          facecolor="white", edgecolor="#cccccc", framealpha=0.92,
                          handlelength=1.8, columnspacing=0.8, borderpad=0.3)

                fig_up.subplots_adjust(top=0.94, bottom=0.07, left=0.08, right=0.98, hspace=0.28, wspace=0.22)
                out_up_4panel = target_dir / "spe10_upscaled_vs_fossil_4panel.png"
                fig_up.savefig(out_up_4panel, bbox_inches="tight", dpi=300)
                plt.close(fig_up)
                saved_files.append(out_up_4panel)

            # 2. INDIVIDUAL UPSCALING FIGURES
            if create_individual:
                # Fig 13 individual (10 curves)
                if df_fig13 is not None:
                    fig, ax = plt.subplots(figsize=(9.5, 6.2), dpi=300)
                    if "Field_Oil_Rate_Landmark_STBD" in df_bench:
                        ax.plot(df_bench["Time_Days"], df_bench["Field_Oil_Rate_Landmark_STBD"],
                                color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                                linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "Landmark", "GeoQuest", "Phillips", "StreamSim", "Roxar", "Coats", "Chevron"]:
                        col = f"{part}_STB_D"
                        if col in df_fig13:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig13["Time_Days"], df_fig13[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                    ax.plot(t_days_prod, q_oil_field_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                            linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                    self._apply_standard_formatting(ax, "Time (days)", "Field Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 6000))
                    fig.suptitle("(Fig. 13) All Upscaled Field Oil Production Rate - SPE 10 Model 2",
                                 fontsize=self.fontsize_labels - 1, fontweight="bold", y=0.985)
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.01),
                              ncol=5, frameon=True, fancybox=True, facecolor="white", edgecolor="#cccccc",
                              fontsize=9.5, handlelength=1.8, columnspacing=1.0, borderpad=0.4)
                    fig.tight_layout(rect=[0, 0, 1, 0.89])
                    save_p = target_dir / "fig13_all_upscaled_field_oil_rate_comparison.png"
                    fig.savefig(save_p, bbox_inches="tight", dpi=300)
                    plt.close(fig)
                    saved_files.append(save_p)

                # Fig 14 individual (5 curves)
                if df_fig14 is not None:
                    fig, ax = plt.subplots(figsize=(8.5, 5.8), dpi=300)
                    ax.plot(df_fig14["Time_Days"], df_fig14["FineGrid_Landmark_STB_D"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part, col in [("Landmark_Upscaled", "Landmark_Upscaled_STB_D"), ("Phillips", "Phillips_STB_D"), ("Coats", "Coats_STB_D")]:
                        if col in df_fig14:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig14["Time_Days"], df_fig14[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                    ax.plot(t_days_bhp, q_oil_p1_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                            linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                    self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 1000))
                    fig.suptitle("(Fig. 14) Pseudo-based Upscaled Producer 1 Oil Rate - SPE 10 Model 2",
                                 fontsize=self.fontsize_labels - 1, fontweight="bold", y=0.985)
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.01),
                              ncol=3, frameon=True, fancybox=True, facecolor="white", edgecolor="#cccccc",
                              fontsize=10.5, handlelength=2.0, columnspacing=1.2, borderpad=0.4)
                    fig.tight_layout(rect=[0, 0, 1, 0.90])
                    save_p = target_dir / "fig14_pseudo_upscaled_producer1_oil_rate_comparison.png"
                    fig.savefig(save_p, bbox_inches="tight", dpi=300)
                    plt.close(fig)
                    saved_files.append(save_p)

                # Fig 16 individual (7 curves)
                if df_fig16 is not None:
                    fig, ax = plt.subplots(figsize=(9.0, 6.0), dpi=300)
                    ax.plot(df_fig16["Time_Days"], df_fig16["FineGrid_Landmark_STB_D"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "GeoQuest", "BP", "Roxar", "Chevron"]:
                        col = f"{part}_STB_D"
                        if col in df_fig16:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig16["Time_Days"], df_fig16[col], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                    ax.plot(t_days_bhp, q_oil_p1_stbd, color=fossil_style["color"], linestyle=fossil_style["ls"],
                            linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                    self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Oil Rate (STB/D)", xlim=(0, 2000), ylim=(0, 1000))
                    fig.suptitle("(Fig. 16) Non-pseudo Upscaled Producer 1 Oil Rate - SPE 10 Model 2",
                                 fontsize=self.fontsize_labels - 1, fontweight="bold", y=0.985)
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.01),
                              ncol=4, frameon=True, fancybox=True, facecolor="white", edgecolor="#cccccc",
                              fontsize=10.0, handlelength=1.8, columnspacing=1.0, borderpad=0.4)
                    fig.tight_layout(rect=[0, 0, 1, 0.90])
                    save_p = target_dir / "fig16_nonpseudo_upscaled_producer1_oil_rate_comparison.png"
                    fig.savefig(save_p, bbox_inches="tight", dpi=300)
                    plt.close(fig)
                    saved_files.append(save_p)

                # Fig 19 individual (7 curves)
                if df_fig19 is not None:
                    fig, ax = plt.subplots(figsize=(9.0, 6.0), dpi=300)
                    ax.plot(df_fig19["Time_Days"], df_fig19["FineGrid_Landmark"],
                            color=up_styles["FineGrid_Ref"]["color"], linestyle=up_styles["FineGrid_Ref"]["ls"],
                            linewidth=up_styles["FineGrid_Ref"]["lw"], label=up_styles["FineGrid_Ref"]["label"])
                    for part in ["TotalFinaElf", "GeoQuest", "BP", "Roxar", "Chevron"]:
                        if part in df_fig19:
                            st = up_styles.get(part, {"color": "gray", "ls": "--", "lw": 1.2, "label": part})
                            ax.plot(df_fig19["Time_Days"], df_fig19[part], color=st["color"], linestyle=st["ls"],
                                    linewidth=st["lw"], label=st["label"])
                    ax.plot(t_days_bhp, p1_wcut, color=fossil_style["color"], linestyle=fossil_style["ls"],
                            linewidth=fossil_style["lw"], label=fossil_style["label"], zorder=6)
                    self._apply_standard_formatting(ax, "Time (days)", "Producer 1 Water Cut (-)", xlim=(0, 2000), ylim=(0, 0.8))
                    fig.suptitle("(Fig. 19) Non-pseudo Upscaled Producer 1 Water Cut - SPE 10 Model 2",
                                 fontsize=self.fontsize_labels - 1, fontweight="bold", y=0.985)
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.01),
                              ncol=4, frameon=True, fancybox=True, facecolor="white", edgecolor="#cccccc",
                              fontsize=10.0, handlelength=1.8, columnspacing=1.0, borderpad=0.4)
                    fig.tight_layout(rect=[0, 0, 1, 0.90])
                    save_p = target_dir / "fig19_nonpseudo_upscaled_producer1_water_cut_comparison.png"
                    fig.savefig(save_p, bbox_inches="tight", dpi=300)
                    plt.close(fig)
                    saved_files.append(save_p)

        return saved_files
