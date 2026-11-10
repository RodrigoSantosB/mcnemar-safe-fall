"""Gera todas as figuras usadas nos slides em results/figures/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402

from safe_fall_statistics import visualizations as viz  # noqa: E402
from safe_fall_statistics.contingency_tables import PairedTable  # noqa: E402
from safe_fall_statistics.data_loader import load_published_table1  # noqa: E402
from safe_fall_statistics.reconstruction import reconstructed_tables  # noqa: E402
from safe_fall_statistics.synthetic_data import CAMPANHA, MONITORIA  # noqa: E402

OUT = ROOT / "results" / "figures"
COLAB_URL = ("https://colab.research.google.com/github/RodrigoSantosB/mcnemar-safe-fall/"
             "blob/main/notebooks/01_mcnemar_safe_fall.ipynb")


def colab_qr(path: Path) -> None:
    import qrcode

    qr = qrcode.QRCode(border=1, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(COLAB_URL)
    qr.make_image(fill_color=viz.NAVY, back_color="white").save(path)


def body_schematic(path: Path) -> None:
    """Esquema didático (vista lateral) das cinco respostas avaliadas pela INFOSECA.

    Ilustração conceitual da postura observada, não instrução de execução.
    """
    from matplotlib.patches import Circle
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.0))

    def limb(ax, p, q, color=viz.NAVY, lw=9):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, solid_capstyle="round", zorder=3)

    def marker(ax, xy, num, color):
        ax.add_patch(Circle(xy, 0.085, color=color, zorder=6))
        ax.text(*xy, str(num), ha="center", va="center", color="white", fontsize=12, weight="bold", zorder=7)

    # Postura protegida: costas arredondadas, queixo no peito, quadril e joelhos flexionados
    ax = axes[0]
    import numpy as np
    C, r = np.array([0.0, 0.47]), 0.42
    ang = np.radians(np.linspace(-60, -240, 60))
    ax.plot(C[0] + r * np.cos(ang), C[1] + r * np.sin(ang), color=viz.NAVY, lw=11, solid_capstyle="round", zorder=3)
    H = tuple(C + r * np.array([np.cos(np.radians(-60)), np.sin(np.radians(-60))]))
    S = tuple(C + r * np.array([np.cos(np.radians(120)), np.sin(np.radians(120))]))
    limb(ax, S, (-0.08, 0.93), lw=8)
    ax.add_patch(Circle((0.0, 1.03), 0.16, color=viz.NAVY, zorder=4))
    K, A = (0.56, 0.62), (0.9, 0.38)
    limb(ax, H, K); limb(ax, K, A)
    E, Hd = (0.18, 0.86), (0.5, 0.98)
    limb(ax, S, E, lw=7); limb(ax, E, Hd, lw=7)
    for xy, n in [((-0.3, 1.1), 1), ((0.64, 1.07), 2), ((-0.58, 0.42), 3), ((0.36, 0.05), 4), ((0.72, 0.76), 5)]:
        marker(ax, xy, n, viz.TEAL)
    ax.set_title("Resposta protegida (correta)", color=viz.TEAL, loc="left")

    # Postura não protegida
    ax = axes[1]
    H, S = (0.15, 0.25), (-0.6, 0.42)
    limb(ax, H, S, lw=11)
    limb(ax, S, (-0.8, 0.5), lw=8)
    ax.add_patch(Circle((-0.9, 0.52), 0.16, color=viz.NAVY, zorder=4))
    K, A = (0.65, 0.33), (1.15, 0.17)
    limb(ax, H, K); limb(ax, K, A)
    E, Hd = (-0.82, 0.22), (-0.98, 0.03)
    limb(ax, S, E, lw=7); limb(ax, E, Hd, lw=7)
    for xy, n in [((-0.72, 0.72), 1), ((-1.12, 0.12), 2), ((-0.22, 0.5), 3), ((0.2, 0.5), 4), ((0.68, 0.55), 5)]:
        marker(ax, xy, n, viz.RED)
    ax.set_title("Resposta não protegida (incorreta)", color=viz.RED, loc="left")

    for ax in axes:
        ax.axhline(0, color=viz.GRAY, lw=2)
        ax.fill_between([-1.4, 1.4], -0.12, 0, color=viz.LIGHT)
        ax.set_xlim(-1.35, 1.35); ax.set_ylim(-0.08, 1.3)
        ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    viz.save(fig, path)


def formula(path: Path, tex: str, color: str, size: int = 26) -> None:
    """Fórmula renderizada com mathtext (fundo transparente) para os slides."""
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, tex, fontsize=size, color=color)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=250, transparent=True, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def demo_snapshot(path: Path, b: int = CAMPANHA.b, c: int = CAMPANHA.c, a: int = CAMPANHA.a,
                  d: int = CAMPANHA.d) -> None:
    """Mesma figura produzida pelo widget do notebook (estado inicial = Ilustração #2)."""
    fig = plt.figure(figsize=(11, 3.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.9])
    viz.plot_contingency(PairedTable(a, b, c, d), ax=fig.add_subplot(gs[0]))
    viz.plot_binomial_null(b, c, ax=fig.add_subplot(gs[1]))
    fig.tight_layout()
    viz.save(fig, path)


def main() -> None:
    df = load_published_table1()
    tables = reconstructed_tables(df)

    viz.save(viz.plot_pre_post(df), OUT / "pre_post_publicado.png")

    viz.save(
        viz.plot_discordant_bars(tables, note="Tabelas 2×2 INFERIDAS a partir das margens e do X² publicados (não são dados originais)."),
        OUT / "discordantes_inferidos.png",
    )

    viz.save(viz.plot_binomial_null(CAMPANHA.b, CAMPANHA.c), OUT / "binomial_b3_c12.png")
    viz.save(viz.plot_chi2_critical(10.0), OUT / "chi2_monitoria.png")

    neck = tables["Flexão do pescoço"]
    viz.save(viz.plot_transitions(neck), OUT / "fluxo_pescoco_inferido.png")
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    viz.plot_contingency(neck, ax=ax)
    viz.save(fig, OUT / "tabela_pescoco_inferida.png")

    body_schematic(OUT / "esquema_respostas.png")
    plt.rcParams["mathtext.fontset"] = "stix"
    formula(OUT / "formula_inversao.png", r"$b+c=\dfrac{(|c-b|-1)^2}{X^2}$", "white")
    # Bloco I — fórmulas do roteiro (documento "Teste de McNemar")
    f = {
        "estimadores": r"$\hat\pi_{11}=\dfrac{a}{N},\ \ \hat\pi_{10}=\dfrac{b}{N},\ \ \hat\pi_{01}=\dfrac{c}{N},\ \ \hat\pi_{00}=\dfrac{d}{N}$",
        "marginais": r"$\pi_{1+}=\pi_{11}+\pi_{10}\qquad \pi_{+1}=\pi_{11}+\pi_{01}$",
        "marginais_amostra": r"$\hat\pi_{1+}=\dfrac{a+b}{N}\qquad \hat\pi_{+1}=\dfrac{a+c}{N}$",
        "h_marginais": r"$H_0:\ \pi_{1+}=\pi_{+1}\qquad H_1:\ \pi_{1+}\neq\pi_{+1}$",
        "h_cancela": r"$\pi_{11}+\pi_{10}=\pi_{11}+\pi_{01}$",
        "h_discordantes": r"$H_0:\ \pi_{10}=\pi_{01}\qquad H_1:\ \pi_{10}\neq\pi_{01}$",
        "p_direcao": r"$p=\dfrac{\pi_{10}}{\pi_{10}+\pi_{01}}\ \Rightarrow\ \mathrm{sob}\ H_0:\ p=0{,}5$",
        "b_binomial": r"$B\sim \mathrm{Bin}(n;\,0{,}5),\quad \mu=\dfrac{n}{2},\quad \sigma^2=\dfrac{n}{4}$",
        "z": r"$z=\dfrac{b-\mu}{\sqrt{\sigma^2}}=\dfrac{b-\frac{n}{2}}{\sqrt{\frac{n}{4}}}=\dfrac{b-\frac{b+c}{2}}{\sqrt{\frac{b+c}{4}}}=\dfrac{b-c}{\sqrt{b+c}}$",
        "v_classica": r"$\chi^2=\dfrac{(b-c)^2}{b+c}$",
        "v_edwards": r"$\chi^2=\dfrac{(|b-c|-1)^2}{b+c}$",
        "v_exata": r"$p=2\cdot P(X\leq k)$",
        "v_midp": r"$p=2\cdot[P(X<k)+0{,}5\,P(X=k)]$",
        "pmf": r"$P(X=k)=\binom{n}{k}\,p^{k}\cdot q^{\,n-k}$",
        "pmf05": r"$P(X=k)=\binom{n}{k}\cdot(0{,}5)^{k}\cdot(0{,}5)^{n-k}$",
        "ex1_chi2": r"$\chi^2=\dfrac{(10-30)^2}{10+30}=\dfrac{400}{40}=10$",
        "ex1_crit": r"$\chi^2_{cr\'itico}=\chi^2_{0{,}05;\,1}=3{,}841$",
        "ex2_p": r"$p_{valor}=2\cdot\sum_{i=0}^{3}\binom{15}{i}\cdot(0{,}5)^{i}\cdot(0{,}5)^{15-i}$",
    }
    for name, tex in f.items():
        formula(OUT / f"f_{name}.png", tex, viz.NAVY)
    formula(OUT / "f_chi2_branco.png", r"$\chi^2=\dfrac{(b-c)^2}{b+c}$", "white")
    formula(OUT / "f_pvalor_branco.png", r"$p_{valor}=2\cdot\sum_{i=0}^{k}P(X=i)$", "white")
    formula(OUT / "f_h_discordantes_branco.png", f["h_discordantes"], "white")
    demo_snapshot(OUT / "demo_b3_c12.png")
    colab_qr(OUT / "qr_colab.png")
    print("figuras em", OUT)


if __name__ == "__main__":
    main()
