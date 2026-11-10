"""Gráficos interativos do notebook, todos em ``plotly.graph_objects``.

Equivalentes interativos de ``visualizations`` (matplotlib, usado só nas figuras
dos slides). Mesmas cores e mesma leitura estatística: vermelho = piorou (b) ou
região de rejeição, verde-azulado = melhorou (c), cinza = concordantes.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

from .contingency_tables import PairedTable
from .mcnemar_analysis import ALPHA, binomial_null_pmf, chi2_pvalue, exact_pvalue_manual, format_p, midp_pvalue

RED = "#DB1E2F"
NAVY = "#0E2A36"
TEAL = "#1C7C8C"
ORANGE = "#E7A23B"
GRAY = "#666666"
LIGHT = "#EEF1F3"
GRID = "#D9DEE2"
CONCORDANT = "#B8C4CB"

FONT = "Lato, Carlito, Calibri, Arial, sans-serif"


def style(fig: go.Figure, title: str, xaxis: str | None = None, yaxis: str | None = None,
          height: int = 420, subtitle: str | None = None) -> go.Figure:
    """Layout comum: fonte, título centralizado, margens, eixos e legenda."""
    text = f"<b>{title}</b>" + (f"<br><span style='font-size:13px;color:{GRAY}'>{subtitle}</span>" if subtitle else "")
    fig.update_layout(
        template="simple_white",
        title=dict(text=text, x=0.5, xanchor="center", font=dict(size=18, color=NAVY)),
        font=dict(family=FONT, size=13, color=NAVY),
        height=height,
        autosize=True,
        margin=dict(l=70, r=40, t=95 if subtitle else 70, b=110),
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=12)),
        hoverlabel=dict(font=dict(family=FONT, size=13)),
    )
    fig.update_xaxes(title_text=xaxis, gridcolor=GRID, zeroline=False)
    fig.update_yaxes(title_text=yaxis, gridcolor=GRID, zeroline=False)
    return fig


def pre_post(df: pd.DataFrame, n_total: int = 122, source: str | None = None) -> go.Figure:
    """Haltere: % de respostas corretas antes e depois, por comportamento (contagem / n)."""
    d = df.iloc[::-1]
    names = list(d["variavel_pt"])
    pre = 100 * d["pre_correct_n"] / n_total
    post = 100 * d["post_correct_n"] / n_total
    fig = go.Figure()
    for name, p0, p1 in zip(names, pre, post):
        fig.add_trace(go.Scatter(x=[p0, p1], y=[name, name], mode="lines", line=dict(color=GRID, width=8),
                                 hoverinfo="skip", showlegend=False))
    for label, vals, counts, color in (("Pré-teste", pre, d["pre_correct_n"], GRAY),
                                       ("Pós-teste", post, d["post_correct_n"], RED)):
        fig.add_trace(go.Scatter(
            x=vals, y=names, mode="markers+text", name=label, text=counts,
            textposition="middle left" if label == "Pré-teste" else "middle right",
            marker=dict(size=16, color=color), textfont=dict(color=color),
            customdata=np.stack([counts, post - pre], axis=-1),
            hovertemplate="%{y}<br>" + label + ": %{customdata[0]}/" + str(n_total)
                          + " = %{x:.1f}%<br>variação: +%{customdata[1]:.1f} p.p.<extra></extra>"))
    style(fig, "Respostas corretas antes e depois do Safe Fall", "% de crianças com resposta correta (contagem / 122)",
          None, height=470, subtitle=source)
    fig.update_xaxes(range=[-8, 108], tickvals=[0, 25, 50, 75, 100])
    return fig


def contingency(table: PairedTable, labels=("Correto", "Incorreto"), axis_titles=("Pré-teste", "Pós-teste"),
                title: str = "Tabela 2 × 2 pareada") -> go.Figure:
    """Tabela 2×2 com os discordantes b e c destacados."""
    names = [["a", "b"], ["c", "d"]]
    values = [[table.a, table.b], [table.c, table.d]]
    meaning = [["concordante", "discordante (+ → −)"], ["discordante (− → +)", "concordante"]]
    code = [[0, 1], [2, 0]]
    fig = go.Figure(go.Heatmap(
        z=code, x=[f"{axis_titles[1]}: {lab}" for lab in labels], y=[f"{axis_titles[0]}: {lab}" for lab in labels],
        colorscale=[[0, LIGHT], [0.33, LIGHT], [0.34, RED], [0.66, RED], [0.67, TEAL], [1, TEAL]],
        zmin=0, zmax=2, showscale=False, xgap=6, ygap=6,
        text=[[f"<b>{values[r][c]}</b><br><i>{names[r][c]}</i>" for c in range(2)] for r in range(2)],
        texttemplate="%{text}", textfont=dict(size=20),
        customdata=meaning, hovertemplate="%{y} · %{x}<br>%{customdata}<extra></extra>"))
    style(fig, title, height=360)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_xaxes(side="top", showgrid=False)
    fig.update_layout(margin=dict(t=110))
    return fig


def binomial_null(b: int, c: int, alpha: float = ALPHA) -> go.Figure:
    """Binomial(b + c; 0,5) sob H₀, com as duas caudas que compõem o p-valor exato."""
    n = b + c
    fig = go.Figure()
    if n == 0:
        fig.add_annotation(text="b + c = 0: sem pares discordantes", showarrow=False, font=dict(size=15, color=GRAY))
        return style(fig, "Distribuição sob H₀", height=300)
    k = np.arange(n + 1)
    pmf = binomial_null_pmf(n)
    lo, hi = min(b, c), max(b, c)
    tail = (k <= lo) | (k >= hi)
    fig.add_trace(go.Bar(x=k, y=pmf, marker_color=np.where(tail, RED, CONCORDANT),
                         customdata=np.where(tail, "na cauda (soma no p-valor)", "fora da cauda"),
                         hovertemplate="B = %{x}<br>P(B = %{x}) = %{y:.4g}<br>%{customdata}<extra></extra>",
                         showlegend=False))
    fig.add_vline(x=b, line=dict(color=NAVY, dash="dash", width=1.5),
                  annotation_text=f"b observado = {b}", annotation_position="top right")
    p = exact_pvalue_manual(b, c)
    style(fig, f"Binomial({n}; 0,5) sob H₀", f"B = nº de discordantes do tipo (+, −), de n = {n}", "P(B = k)",
          subtitle=f"{format_p(p, 4)} = soma das barras vermelhas")
    if n > 40:
        spread = 2 * np.sqrt(n)
        fig.update_xaxes(range=[max(-1, min(lo, n / 2 - spread) - 2), min(n + 1, max(hi, n / 2 + spread) + 2)])
    return fig


def chi2_critical(statistic: float, alpha: float = ALPHA) -> go.Figure:
    """Densidade χ² (1 gl) com a região crítica e a estatística observada."""
    crit = float(stats.chi2.isf(alpha, df=1))
    xmax = max(8.0, statistic * 1.25)
    x = np.linspace(0.05, xmax, 600)
    y = stats.chi2.pdf(x, df=1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=NAVY, width=2.5), name="χ² com 1 gl",
                             hovertemplate="χ² = %{x:.2f}<br>densidade = %{y:.4f}<extra></extra>"))
    xr = x[x >= crit]
    fig.add_trace(go.Scatter(x=np.r_[crit, xr, xr[-1]], y=np.r_[0, stats.chi2.pdf(xr, df=1), 0], fill="toself",
                             fillcolor="rgba(219,30,47,0.75)", line=dict(width=0), name=f"região crítica (α = {alpha:g})",
                             hoverinfo="skip"))
    fig.add_vline(x=crit, line=dict(color=RED, dash="dash"), annotation_text=f"crítico = {crit:.3f}",
                  annotation_position="top right")
    fig.add_vline(x=statistic, line=dict(color=TEAL, width=3), annotation_text=f"observado = {statistic:g}",
                  annotation_position="top left")
    style(fig, "Distribuição qui-quadrado com 1 grau de liberdade", "χ²", "densidade",
          subtitle=f"p-valor = P(χ² ≥ {statistic:g}) = {stats.chi2.sf(statistic, df=1):.6g}")
    fig.update_yaxes(range=[0, 0.8])
    fig.update_xaxes(range=[0, xmax])
    return fig


def transitions(table: PairedTable, title: str = "Transições entre as duas medidas",
                labels=("Correto", "Incorreto"), moments=("Pré", "Pós")) -> go.Figure:
    """Fluxo medida 1 → medida 2 (Sankey) com as quatro transições a, b, c, d."""
    nodes = [f"{moments[0]}: {labels[0]}", f"{moments[0]}: {labels[1]}",
             f"{moments[1]}: {labels[0]}", f"{moments[1]}: {labels[1]}"]
    fig = go.Figure(go.Sankey(
        arrangement="fixed",
        node=dict(label=nodes, color=[TEAL, GRAY, TEAL, GRAY], pad=24, thickness=18,
                  x=[0.01, 0.01, 0.99, 0.99], y=[0.2, 0.8, 0.2, 0.8]),
        link=dict(source=[0, 0, 1, 1], target=[2, 3, 2, 3], value=[table.a, table.b, table.c, table.d],
                  color=["rgba(184,196,203,.6)", "rgba(219,30,47,.75)", "rgba(28,124,140,.75)", "rgba(184,196,203,.6)"],
                  customdata=["a — permaneceu", "b — (+ → −)", "c — (− → +)", "d — permaneceu"],
                  hovertemplate="%{customdata}: %{value}<extra></extra>")))
    return style(fig, title, height=380, subtitle=f"c = {table.c} (− → +)   ·   b = {table.b} (+ → −)")


def exact_vs_asymptotic(n: int = 15, alpha: float = ALPHA) -> go.Figure:
    """P-valor em função de b, com n = b + c fixo, para os quatro procedimentos."""
    bs = np.arange(0, n + 1)
    series = [("Exato (binomial)", [exact_pvalue_manual(b, n - b) for b in bs], RED, "solid", "circle"),
              ("Mid-p exato", [midp_pvalue(b, n - b) for b in bs], ORANGE, "dot", "diamond"),
              ("χ² clássico", [chi2_pvalue(b, n - b, False) for b in bs], NAVY, "dash", "square"),
              ("χ² com correção (Edwards)", [chi2_pvalue(b, n - b, True) for b in bs], TEAL, "dashdot", "triangle-up")]
    fig = go.Figure()
    exact, classic = series[0][1], series[2][1]
    for b, e, u in zip(bs, exact, classic):
        if (e < alpha) != (u < alpha):
            fig.add_vrect(x0=b - 0.4, x1=b + 0.4, fillcolor=ORANGE, opacity=0.15, line_width=0)
    for name, ps, color, dash, symbol in series:
        fig.add_trace(go.Scatter(x=bs, y=ps, mode="lines+markers", name=name, line=dict(color=color, dash=dash),
                                 marker=dict(symbol=symbol, size=8),
                                 hovertemplate=name + "<br>b = %{x}, c = " + f"{n} − b" + "<br>p = %{y:.4g}<extra></extra>"))
    fig.add_hline(y=alpha, line=dict(color=GRAY, width=1), annotation_text=f"α = {alpha:g}",
                  annotation_position="bottom right")
    style(fig, f"P-valor das quatro versões com n = b + c = {n}", "b (discordantes do tipo + → −)",
          "p-valor (escala log)", height=440,
          subtitle="faixas laranja: exato e χ² clássico levam a conclusões diferentes")
    fig.update_yaxes(type="log")
    fig.update_layout(legend=dict(y=-0.25), margin=dict(b=130))
    return fig


def discordant_bars(tables: dict[str, PairedTable], note: str | None = None) -> go.Figure:
    """Pares discordantes b (à esquerda) e c (à direita) por comportamento."""
    names = list(tables)[::-1]
    b = [tables[k].b for k in names]
    c = [tables[k].c for k in names]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=names, x=c, orientation="h", name="c — melhorou (incorreto → correto)",
                         marker_color=TEAL, text=c, textposition="outside",
                         hovertemplate="%{y}<br>c = %{x}<extra></extra>"))
    fig.add_trace(go.Bar(y=names, x=[-v for v in b], orientation="h", name="b — piorou (correto → incorreto)",
                         marker_color=RED, text=b, textposition="outside", customdata=b,
                         hovertemplate="%{y}<br>b = %{customdata}<extra></extra>"))
    style(fig, "Pares discordantes por comportamento", "nº de crianças", None, height=440, subtitle=note)
    fig.update_layout(barmode="relative")
    fig.update_traces(cliponaxis=False)
    fig.update_xaxes(range=[-15, 130])
    return fig


def pvalue_bars(df: pd.DataFrame, alpha: float = ALPHA) -> go.Figure:
    """Barras horizontais com o p-valor de cada versão (colunas ``versão`` e ``p``)."""
    colors = [TEAL, NAVY, RED, ORANGE][: len(df)]
    fig = go.Figure(go.Bar(y=df["versão"], x=df["p"], orientation="h", marker_color=colors,
                           text=[f"{p:.4g}" for p in df["p"]], textposition="outside",
                           hovertemplate="%{y}<br>p = %{x:.6g}<extra></extra>"))
    fig.add_vline(x=alpha, line=dict(color=GRAY, dash="dash"), annotation_text=f"α = {alpha:g}")
    style(fig, "P-valor por versão do teste", "p-valor", None, height=320)
    fig.update_yaxes(autorange="reversed")
    return fig
