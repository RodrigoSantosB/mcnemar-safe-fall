"""Gráficos no padrão visual da apresentação (paleta CIn-UFPE)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath

from .contingency_tables import PairedTable
from .mcnemar_analysis import ALPHA, binomial_null_pmf, chi2_pvalue, exact_pvalue_manual, format_p

RED = "#DB1E2F"
DARK_RED = "#AF0421"
NAVY = "#0E2A36"
TEAL = "#1C7C8C"
ORANGE = "#E7A23B"
GRAY = "#666666"
LIGHT = "#EEF1F3"
GRID = "#D9DEE2"

IMPROVED = TEAL
WORSENED = RED
CONCORDANT = "#B8C4CB"


def _register_carlito() -> None:
    """Carlito é métrica-compatível com Calibri (fonte do template); registra se instalada."""
    from matplotlib import font_manager

    if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist):
        return
    for path in font_manager.findSystemFonts():
        if "Carlito" in Path(path).name:
            font_manager.fontManager.addfont(path)


def apply_style() -> None:
    _register_carlito()
    plt.rcParams.update(
        {
            "font.family": ["Carlito", "DejaVu Sans"],
            "font.size": 12,
            "axes.edgecolor": GRID,
            "axes.labelcolor": NAVY,
            "axes.titlecolor": NAVY,
            "axes.titleweight": "bold",
            "axes.titlesize": 14,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": GRAY,
            "ytick.color": GRAY,
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "figure.facecolor": "white",
        }
    )


apply_style()


def _source(ax, text: str) -> None:
    ax.figure.text(0.01, -0.02, text, fontsize=8.5, color=GRAY, style="italic", ha="left", va="top")


def plot_pre_post(df: pd.DataFrame, n_total: int = 122, ax=None, source: str | None = None):
    """Haltere (dumbbell): % de respostas corretas antes e depois, por comportamento."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 4.6))
    d = df.iloc[::-1].reset_index(drop=True)
    y = np.arange(len(d))
    pre = 100 * d["pre_correct_n"] / n_total
    post = 100 * d["post_correct_n"] / n_total
    ax.hlines(y, pre, post, color=GRID, lw=6, zorder=1)
    ax.scatter(pre, y, s=150, color=GRAY, zorder=3, label="Pré-teste")
    ax.scatter(post, y, s=150, color=RED, zorder=3, label="Pós-teste")
    for yi, p0, p1, n0, n1 in zip(y, pre, post, d["pre_correct_n"], d["post_correct_n"]):
        ax.text(p0 - 3.2, yi, f"{n0}", ha="right", va="center", color=GRAY, fontsize=11)
        ax.text(p1 + 3.2, yi, f"{n1}", ha="left", va="center", color=RED, fontsize=11, weight="bold")
        ax.text(103 + 9, yi, f"+{p1 - p0:.1f} p.p.", ha="left", va="center", color=NAVY, fontsize=11)
        ax.text(103 + 31, yi, "p < 0,001", ha="left", va="center", color=TEAL, fontsize=11, weight="bold")
    ax.set_yticks(y, d["variavel_pt"])
    ax.set_xlim(-8, 155)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("% de crianças com resposta correta (contagem / 122, recalculada)")
    ax.axvline(100, color=GRID, lw=1)
    ax.text(103 + 9, len(d) - 0.35, "variação", color=GRAY, fontsize=10)
    ax.text(103 + 31, len(d) - 0.35, "McNemar", color=GRAY, fontsize=10)
    ax.legend(loc="lower center", bbox_to_anchor=(0.32, 1.0), ncol=2, frameon=False)
    ax.tick_params(axis="y", length=0, labelsize=12, labelcolor=NAVY)
    ax.spines["left"].set_visible(False)
    if source:
        _source(ax, source)
    return ax


def plot_contingency(table: PairedTable, ax=None, title: str | None = None, labels=("Correto", "Incorreto")):
    """Matriz 2×2 com as células discordantes b e c destacadas."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.8, 4.2))
    cells = {(0, 0): ("a", table.a), (0, 1): ("b", table.b), (1, 0): ("c", table.c), (1, 1): ("d", table.d)}
    colors = {"a": LIGHT, "d": LIGHT, "b": WORSENED, "c": IMPROVED}
    for (r, col), (name, value) in cells.items():
        x, y = col, 1 - r
        ax.add_patch(
            FancyBboxPatch((x + 0.04, y + 0.04), 0.92, 0.92, boxstyle="round,pad=0,rounding_size=0.06",
                           fc=colors[name], ec="none")
        )
        fg = "white" if name in "bc" else NAVY
        ax.text(x + 0.5, y + 0.58, str(value), ha="center", va="center", fontsize=26, weight="bold", color=fg)
        ax.text(x + 0.5, y + 0.25, name, ha="center", va="center", fontsize=13, style="italic", color=fg)
    ax.set_xlim(-0.55, 2.05)
    ax.set_ylim(-0.1, 2.45)
    ax.text(1.0, 2.3, "Pós-teste", ha="center", fontsize=12, weight="bold", color=NAVY)
    ax.text(-0.5, 1.0, "Pré-teste", ha="center", va="center", rotation=90, fontsize=12, weight="bold", color=NAVY)
    for i, lab in enumerate(labels):
        ax.text(i + 0.5, 2.08, lab, ha="center", fontsize=11, color=GRAY)
        ax.text(-0.08, 1.5 - i, lab, ha="right", va="center", fontsize=11, color=GRAY, rotation=90)
    ax.axis("off")
    if title:
        ax.set_title(title, loc="left")
    return ax


def plot_binomial_null(b: int, c: int, ax=None, alpha: float = ALPHA):
    """Distribuição Binomial(b+c, 0,5) sob H0 com as caudas do p-valor exato."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7.5, 3.8))
    n = b + c
    if n == 0:
        ax.text(0.5, 0.5, "b + c = 0: sem pares discordantes", ha="center", va="center", transform=ax.transAxes,
                color=GRAY, fontsize=13)
        ax.axis("off")
        return ax
    k = np.arange(n + 1)
    pmf = binomial_null_pmf(n)
    lo, hi = min(b, c), max(b, c)
    in_tail = (k <= lo) | (k >= hi)
    ax.bar(k, pmf, color=np.where(in_tail, RED, CONCORDANT), width=0.8 if n < 60 else 1.0, edgecolor="none")
    ax.axvline(b, color=NAVY, ls="--", lw=1.4)
    ymax = pmf.max()
    ax.text(b + 0.25, ymax * 1.08, f" b observado = {b}", ha="left", color=NAVY, fontsize=11)
    ax.set_ylim(0, ymax * 1.22)
    from matplotlib.ticker import MaxNLocator

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(f"B = nº de pares discordantes que pioraram (de n = {n})")
    ax.set_ylabel("P(B = k) sob H₀")
    p = exact_pvalue_manual(b, c)
    ax.set_title(f"Binomial({n}; 0,5) — {format_p(p)} (área vermelha)", loc="left")
    if n > 40:
        center, spread = n / 2, 4 * np.sqrt(n) / 2
        ax.set_xlim(max(-1, min(lo, center - spread) - 2), min(n + 1, max(hi, center + spread) + 2))
    return ax


def plot_transitions(table: PairedTable, ax=None, title: str | None = None):
    """Diagrama de fluxo pré → pós com as quatro transições."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7.2, 4.2))
    n = table.n
    gap = 0.04
    h = lambda v: v / n * (1 - gap)  # noqa: E731
    pre_c, pre_i = table.pre_correct, table.n - table.pre_correct
    post_c, post_i = table.post_correct, table.n - table.post_correct
    # nós: (y_base, altura)
    left = {"C": (1 - h(pre_c), h(pre_c)), "I": (0, h(pre_i))}
    right = {"C": (1 - h(post_c), h(post_c)), "I": (0, h(post_i))}
    xl, xr, w = 0.0, 1.0, 0.06
    for side, x, nodes, counts in ((0, xl, left, (pre_c, pre_i)), (1, xr, right, (post_c, post_i))):
        for (key, (y0, hh)), cnt in zip(nodes.items(), counts):
            color = TEAL if key == "C" else GRAY
            ax.add_patch(plt.Rectangle((x - (w if side == 0 else 0), y0), w, hh, color=color))
            label = f"{'Correto' if key == 'C' else 'Incorreto'}\n{cnt}"
            ax.text(x - w - 0.02 if side == 0 else x + w + 0.02, y0 + hh / 2, label,
                    ha="right" if side == 0 else "left", va="center", fontsize=11, color=NAVY)
    flows = [("C", "C", table.a, CONCORDANT), ("C", "I", table.b, WORSENED),
             ("I", "C", table.c, IMPROVED), ("I", "I", table.d, CONCORDANT)]
    cursor_l = {k: v[0] + v[1] for k, v in left.items()}
    cursor_r = {k: v[0] + v[1] for k, v in right.items()}
    for src, dst, v, color in flows:
        if v == 0:
            continue
        hh = h(v)
        y1t = cursor_l[src]; y1b = y1t - hh; cursor_l[src] = y1b
        y2t = cursor_r[dst]; y2b = y2t - hh; cursor_r[dst] = y2b
        x0, x1 = xl, xr
        verts = [(x0, y1t), (0.5, y1t), (0.5, y2t), (x1, y2t), (x1, y2b), (0.5, y2b), (0.5, y1b), (x0, y1b), (x0, y1t)]
        codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4, MplPath.LINETO,
                 MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4, MplPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MplPath(verts, codes), fc=color, ec="none", alpha=0.75 if color != CONCORDANT else 0.55))
    ax.text(xl - w / 2, 1.06, "Pré-teste", ha="center", fontsize=12, weight="bold", color=NAVY)
    ax.text(xr + w / 2, 1.06, "Pós-teste", ha="center", fontsize=12, weight="bold", color=NAVY)
    ax.text(0.5, -0.1, f"melhorou (c) = {table.c}", color=IMPROVED, ha="right", fontsize=11, weight="bold")
    ax.text(0.53, -0.1, f"   piorou (b) = {table.b}", color=WORSENED, ha="left", fontsize=11, weight="bold")
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-0.15, 1.12)
    ax.axis("off")
    if title:
        ax.set_title(title, loc="left")
    return ax


def plot_exact_vs_asymptotic(n: int = 10, ax=None):
    """P-valor em função de b (n = b + c fixo) para os três procedimentos."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7.5, 3.8))
    bs = np.arange(0, n + 1)
    exact = [exact_pvalue_manual(b, n - b) for b in bs]
    unc = [chi2_pvalue(b, n - b, False) for b in bs]
    cor = [chi2_pvalue(b, n - b, True) for b in bs]
    ax.plot(bs, exact, "o-", color=RED, lw=2.2, label="Exato (binomial)")
    ax.plot(bs, unc, "s--", color=NAVY, lw=1.6, label="χ² sem correção")
    ax.plot(bs, cor, "^:", color=ORANGE, lw=1.8, label="χ² com correção de continuidade")
    ax.axhline(ALPHA, color=GRAY, lw=1)
    ax.text(n + 0.2, ALPHA, "α = 0,05", va="center", color=GRAY, fontsize=10)
    ax.set_yscale("log")
    ax.set_ylim(min(min(exact), min(unc)) / 2, 1.5)
    ax.set_xlabel(f"b (pioraram), com b + c = {n}")
    ax.set_ylabel("p-valor (escala log)")
    ax.legend(frameon=False, fontsize=10, loc="lower center")
    disagree = [b for b, e, u in zip(bs, exact, unc) if (e < ALPHA) != (u < ALPHA)]
    for b in disagree:
        ax.axvspan(b - 0.4, b + 0.4, color=ORANGE, alpha=0.15, lw=0)
    ax.set_title(f"Com poucos pares discordantes (n = {n}) os métodos divergem", loc="left")
    return ax


def plot_discordant_bars(tables: dict[str, PairedTable], ax=None, note: str | None = None):
    """Pares discordantes (b × c) por comportamento."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8.5, 4.0))
    names = list(tables)[::-1]
    y = np.arange(len(names))
    b = np.array([tables[k].b for k in names])
    c = np.array([tables[k].c for k in names])
    ax.barh(y, c, color=IMPROVED, label="c — melhorou (incorreto → correto)")
    ax.barh(y, -b, color=WORSENED, label="b — piorou (correto → incorreto)")
    for yi, bi, ci in zip(y, b, c):
        ax.text(ci + 1.5, yi, str(ci), va="center", color=IMPROVED, weight="bold")
        ax.text(-bi - 1.5, yi, str(bi), va="center", ha="right", color=WORSENED, weight="bold")
    ax.axvline(0, color=NAVY, lw=1)
    ax.set_yticks(y, names)
    ax.set_xlim(-14, 122)
    ax.set_xlabel("Nº de crianças (pares discordantes)")
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=2, fontsize=10)
    ax.tick_params(axis="y", length=0, labelsize=12, labelcolor=NAVY)
    ax.spines["left"].set_visible(False)
    if note:
        _source(ax, note)
    return ax


def plot_pvalue_vs_c(n: int = 20, ax=None):
    """Para n discordantes fixos: como o p-valor exato varia com o desequilíbrio b × c."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7.5, 3.6))
    cs = np.arange(0, n + 1)
    ps = np.array([exact_pvalue_manual(n - c, c) for c in cs])
    colors = np.where(ps < ALPHA, RED, CONCORDANT)
    ax.bar(cs, ps, color=colors, width=0.75)
    ax.axhline(ALPHA, color=NAVY, lw=1, ls="--")
    ax.text(n + 0.6, ALPHA + 0.02, "α = 0,05", color=NAVY, fontsize=10, ha="right")
    ax.set_xlabel(f"c = nº que melhoraram (b = {n} − c)")
    ax.set_ylabel("p-valor exato")
    ax.set_title(f"Equilíbrio (c ≈ b) → p alto; desequilíbrio → p baixo (n = {n})", loc="left")
    return ax


def save(fig_or_ax, path: str | Path) -> Path:
    fig = fig_or_ax.figure if hasattr(fig_or_ax, "figure") else fig_or_ax
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return path
