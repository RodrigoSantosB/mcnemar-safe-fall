"""Versões ajustáveis dos exemplos mostrados nos slides.

Cada função ``*_state`` calcula o conteúdo de um exemplo sem interface (testável);
cada ``*_tab`` devolve um painel ipywidgets; ``slide_examples_widget`` reúne todos
em abas numeradas pelo slide correspondente. Funciona em Jupyter, VS Code e Colab
(ipywidgets 7 ou 8).
"""

from __future__ import annotations

from math import comb

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import visualizations as viz
from .contingency_tables import PairedTable
from .data_loader import N_TOTAL, load_published_table1
from .mcnemar_analysis import ALPHA, compare_methods, format_p, interpret, mcnemar_exact
from .reconstruction import feasible_range, reconstruct_from_chi2
from .synthetic_data import EDUCATION_EXAMPLE, SMALL_NOT_SIGNIFICANT, SMALL_SIGNIFICANT

MAX_CELL = 120
_STYLE = {"description_width": "170px"}


def _w():
    import ipywidgets as w

    return w


def _slider(description, value, min_value=0, max_value=MAX_CELL):
    w = _w()
    return w.IntSlider(value=value, min=min_value, max=max_value, description=description, style=_STYLE,
                       continuous_update=False, layout=w.Layout(width="480px"))


def _panel(controls, render, note=None):
    """Controles + saída atualizada automaticamente."""
    w = _w()
    out = w.interactive_output(render, controls)
    children = [w.HBox(list(controls.values())) if len(controls) <= 2 else w.VBox(list(controls.values()))]
    if note:
        children.append(w.HTML(f"<span style='color:#666'>{note}</span>"))
    children.append(out)
    return w.VBox(children)


# ---------------------------------------------------------------- slide 8: cálculo passo a passo

def worked_example_state(b: int, c: int) -> dict:
    n = b + c
    k = min(b, c)
    terms = [comb(n, i) for i in range(k + 1)] if n else []
    tail = sum(terms) / 2**n if n else 1.0
    p = min(1.0, 2 * tail) if n else 1.0
    return {"n": n, "k": k, "terms": terms, "tail": tail, "p": p, "significant": p < ALPHA}


def worked_example_render(b: int, c: int):
    s = worked_example_state(b, c)
    n, k = s["n"], s["k"]
    print(f"1. Pares discordantes      n = b + c = {b} + {c} = {n}")
    if n == 0:
        print("   Sem pares discordantes: nada a testar, p = 1.")
        return s
    print(f"2. Distribuição sob H0     B ~ Binomial({n}; 0,5)")
    terms = s["terms"]
    shown = " + ".join(map(str, terms)) if len(terms) <= 8 else " + ".join(map(str, terms[:4])) + " + … + " + str(terms[-1])
    print(f"3. Cauda menor             P(B ≤ {k}) = ({shown}) / 2^{n} = {s['tail']:.6g}")
    print(f"4. Bilateral               p = min(1; 2 × {s['tail']:.6g}) = {s['p']:.6g}")
    verdict = "rejeita H0" if s["significant"] else "não rejeita H0"
    print(f"5. Decisão                 {format_p(s['p'])} {'<' if s['significant'] else '≥'} 0,05 ⇒ {verdict}")
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    viz.plot_binomial_null(b, c, ax=ax)
    plt.show()
    return s


def worked_example_tab(b: int = 2, c: int = 10):
    return _panel({"b": _slider("b — pioraram", b, max_value=60), "c": _slider("c — melhoraram", c, max_value=60)},
                  worked_example_render)


# ---------------------------------------------------------------- slide 9: significativo × não

def _pair_render(b1, c1, b2, c2, a=20, d=7):
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.8), gridspec_kw={"width_ratios": [1, 1.8]})
    for row, (b, c) in enumerate(((b1, c1), (b2, c2))):
        t = PairedTable(a, b, c, d)
        viz.plot_contingency(t, ax=axes[row, 0])
        viz.plot_binomial_null(b, c, ax=axes[row, 1])
    fig.tight_layout()
    plt.show()
    for label, (b, c) in (("Cenário 1", (b1, c1)), ("Cenário 2", (b2, c2))):
        print(f"{label}: " + interpret(mcnemar_exact(PairedTable(a, b, c, d))))


def significance_tab():
    t1, t2 = SMALL_SIGNIFICANT, SMALL_NOT_SIGNIFICANT
    controls = {
        "b1": _slider("Cenário 1 · b", t1.b, max_value=40), "c1": _slider("Cenário 1 · c", t1.c, max_value=40),
        "b2": _slider("Cenário 2 · b", t2.b, max_value=40), "c2": _slider("Cenário 2 · c", t2.c, max_value=40),
    }
    return _panel(controls, lambda b1, c1, b2, c2: _pair_render(b1, c1, b2, c2),
                  "Slide: cenário 1 = (b 2, c 10) → p = 0,039; cenário 2 = (b 5, c 9) → p = 0,424.")


# ---------------------------------------------------------------- slide 10: exato × χ²

def methods_state(n: int, b: int) -> pd.DataFrame:
    b = min(b, n)
    cmp = compare_methods(PairedTable(0, b, n - b, 0))
    rows = [
        ("Exato (binomial)", f"min = {min(b, n - b)}", cmp["p_exato"]),
        ("χ² sem correção", f"{cmp['chi2_sem_correcao']:.2f}", cmp["p_chi2_sem_correcao"]),
        ("χ² com correção", f"{cmp['chi2_com_correcao']:.2f}", cmp["p_chi2_com_correcao"]),
    ]
    df = pd.DataFrame(rows, columns=["método", "estatística", "p"])
    df["rejeita H0 (5%)"] = df["p"] < ALPHA
    return df


def methods_render(n: int, b: int):
    b = min(b, n)
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    viz.plot_exact_vs_asymptotic(n=n, ax=ax)
    ax.axvline(b, color=viz.TEAL, lw=2, alpha=0.6)
    plt.show()
    from IPython.display import display

    df = methods_state(n, b)
    print(f"b = {b}, c = {n - b}")
    display(df.style.format({"p": "{:.4f}"}))
    if df["rejeita H0 (5%)"].nunique() > 1:
        print("⚠ Os métodos levam a conclusões diferentes neste caso.")


def methods_tab(n: int = 8, b: int = 1):
    w = _w()
    sn = _slider("n = b + c", n, 1, 60)
    sb = _slider("b — pioraram", b, 0, 60)

    def sync(change):
        sb.max = sn.value

    sn.observe(sync, names="value")
    sync(None)
    return _panel({"n": sn, "b": sb}, methods_render,
                  "Slide: n = 8, b = 1 → exato 0,070 × χ² sem correção 0,034 (faixas laranja = conclusões divergentes).")


# ---------------------------------------------------------------- slide 18: Safe Fall (inferido)

def safe_fall_state(variable: str, b: int | None = None) -> dict:
    df = load_published_table1()
    row = df.loc[df["variavel_pt"] == variable].iloc[0]
    pre, post = int(row["pre_correct_n"]), int(row["post_correct_n"])
    rec = reconstruct_from_chi2(pre, post, float(row["chi2_reported"]))
    if b is None:
        b = rec.table.b
    c = b + (post - pre)
    table = PairedTable(pre - b, b, c, N_TOTAL - pre - c)
    return {"row": row, "inferred": rec.table, "table": table, "is_inferred": table == rec.table,
            "result": mcnemar_exact(table), "range": feasible_range(pre, post)}


def safe_fall_render(variable: str, b: int):
    s = safe_fall_state(variable, b)
    t, row = s["table"], s["row"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), gridspec_kw={"width_ratios": [1, 1.4, 1.6]})
    tag = "INFERIDO" if s["is_inferred"] else "HIPOTÉTICO (mesmas margens)"
    viz.plot_contingency(t, ax=axes[0], title=f"[{tag}]")
    viz.plot_transitions(t, ax=axes[1])
    viz.plot_binomial_null(t.b, t.c, ax=axes[2])
    fig.tight_layout()
    plt.show()
    chi2 = compare_methods(t)["chi2_com_correcao"]
    print(f"Publicado: pré correto {row.pre_correct_n}, pós correto {row.post_correct_n}, X² = {row.chi2_reported:.3f}")
    print(f"Tabela {tag.lower()}: a={t.a}, b={t.b}, c={t.c}, d={t.d} → χ² corrigido = {chi2:.3f}, "
          f"p exato = {s['result'].pvalue:.3g} ({format_p(s['result'].pvalue)})")
    if not s["is_inferred"]:
        print(f"Com as mesmas margens, b poderia ir de {s['range'][0]} a {s['range'][1]}; "
              f"só b = {s['inferred'].b} reproduz o X² publicado.")


def safe_fall_tab():
    w = _w()
    names = list(load_published_table1()["variavel_pt"])
    dd = w.Dropdown(options=names, value=names[0], description="Comportamento", style=_STYLE,
                    layout=w.Layout(width="480px"))
    sb = _slider("b (pioraram)", 2, 0, 12)

    def sync(change):
        st = safe_fall_state(dd.value)
        lo, hi = st["range"]
        sb.min, sb.max = lo, hi
        sb.value = st["inferred"].b

    dd.observe(sync, names="value")
    sync(None)
    return _panel({"variable": dd, "b": sb}, safe_fall_render,
                  "Valor inicial de b = tabela inferida do artigo. Mova b para ver outras tabelas com as MESMAS margens.")


# ---------------------------------------------------------------- slide 23: p-valor × c

def pvalue_vs_c_render(n: int, c: int):
    c = min(c, n)
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    viz.plot_pvalue_vs_c(n=n, ax=ax)
    ax.bar([c], [mcnemar_exact(PairedTable(0, n - c, c, 0)).pvalue], color="none", edgecolor=viz.NAVY, lw=2.2, width=0.9)
    plt.show()
    r = mcnemar_exact(PairedTable(0, n - c, c, 0))
    print(f"n = {n}, c = {c}, b = {n - c}: {format_p(r.pvalue)} — {'significativo' if r.significant else 'não significativo'}")


def pvalue_vs_c_tab(n: int = 20, c: int = 15):
    sn = _slider("n = b + c", n, 1, 80)
    sc = _slider("c — melhoraram", c, 0, 80)

    def sync(change):
        sc.max = sn.value

    sn.observe(sync, names="value")
    sync(None)
    return _panel({"n": sn, "c": sc}, pvalue_vs_c_render, "Barra contornada = cenário escolhido.")


# ---------------------------------------------------------------- slide 24: educação

def education_render(a: int, b: int, c: int, d: int):
    t = PairedTable(a, b, c, d)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), gridspec_kw={"width_ratios": [1, 1.4, 1.6]})
    viz.plot_contingency(t, ax=axes[0], labels=("Acertou", "Errou"), title="[SINTÉTICO]")
    if t.n:
        viz.plot_transitions(t, ax=axes[1])
    else:
        axes[1].axis("off")
    viz.plot_binomial_null(b, c, ax=axes[2])
    fig.tight_layout()
    plt.show()
    print(f"{t.n} alunos. " + interpret(mcnemar_exact(t)))


def education_tab():
    e = EDUCATION_EXAMPLE
    controls = {"a": _slider("a — acertou → acertou", e.a, max_value=80),
                "b": _slider("b — acertou → errou", e.b, max_value=80),
                "c": _slider("c — errou → acertou", e.c, max_value=80),
                "d": _slider("d — errou → errou", e.d, max_value=80)}
    return _panel(controls, education_render, "Slide: 40 alunos, b = 3, c = 13 → p = 0,021.")


# ---------------------------------------------------------------- todas as abas

def slide_examples_widget():
    """Abas com os exemplos ajustáveis, na ordem dos slides."""
    from .interactive_demo import mcnemar_widget

    w = _w()
    tabs = [
        ("Slide 8 · passo a passo", worked_example_tab()),
        ("Slide 9 · sig. × não sig.", significance_tab()),
        ("Slide 10 · exato × χ²", methods_tab()),
        ("Slide 18 · Safe Fall", safe_fall_tab()),
        ("Slide 22 · demonstração", mcnemar_widget(b=3, c=13, a=15, d=9)),
        ("Slide 23 · p-valor × c", pvalue_vs_c_tab()),
        ("Slide 24 · educação", education_tab()),
    ]
    tab = w.Tab(children=[t[1] for t in tabs])
    for i, (title, _) in enumerate(tabs):
        tab.set_title(i, title)
    return tab
