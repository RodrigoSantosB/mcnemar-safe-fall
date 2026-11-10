"""Versões ajustáveis dos exemplos mostrados nos slides.

Cada função ``*_state`` calcula o conteúdo de um exemplo sem interface (testável);
cada ``*_tab`` devolve um painel ipywidgets; ``slide_examples_widget`` reúne todos
em abas numeradas pelo slide correspondente. Funciona em Jupyter, VS Code e Colab
(ipywidgets 7 ou 8).
"""

from __future__ import annotations

from math import comb

import pandas as pd

from . import plotly_charts as pc
from .contingency_tables import PairedTable
from .data_loader import N_TOTAL, load_published_table1
from .mcnemar_analysis import ALPHA, chi2_critical, compare_methods, format_p, mcnemar_exact
from .reconstruction import feasible_range, reconstruct_from_chi2
from .synthetic_data import CAMPANHA, MONITORIA

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


# ---------------------------------------------------------------- slide 10: as quatro variantes

def variants_state(b: int, c: int) -> pd.DataFrame:
    cmp = compare_methods(PairedTable(0, b, c, 0))
    rows = [
        ("Clássica (assintótica)", f"χ² = {cmp['chi2_sem_correcao']:.3f}", cmp["p_chi2_sem_correcao"]),
        ("Com correção (Edwards)", f"χ² = {cmp['chi2_com_correcao']:.3f}", cmp["p_chi2_com_correcao"]),
        ("Exata (binomial)", f"k = {min(b, c)}", cmp["p_exato"]),
        ("Mid-p exata", f"k = {min(b, c)}", cmp["p_midp"]),
    ]
    df = pd.DataFrame(rows, columns=["versão", "estatística", "p"])
    df["rejeita H0 (5%)"] = df["p"] < ALPHA
    return df


def variants_render(b: int, c: int):
    from IPython.display import display

    n = b + c
    print(f"b = {b}, c = {c}, n = b + c = {n} — "
          + ("n ≥ 25: as aproximações χ² são adequadas." if n >= 25 else "n < 25: prefira a exata ou a mid-p."))
    df = variants_state(b, c)
    display(df.style.format({"p": "{:.6f}"}))
    if df["rejeita H0 (5%)"].nunique() > 1:
        print("Atenção: as versões levam a conclusões diferentes neste caso.")
    pc.pvalue_bars(df).show()


def variants_tab(b: int = CAMPANHA.b, c: int = CAMPANHA.c):
    return _panel({"b": _slider("b — (+, −)", b, max_value=60), "c": _slider("c — (−, +)", c, max_value=60)},
                  variants_render, "Começa na Ilustração #2 (b = 3, c = 12). Com muitos discordantes, as quatro convergem.")


# ---------------------------------------------------------------- slide 15: Ilustração #1 (clássico)

def classic_example_state(a: int, b: int, c: int, d: int, alpha: float = ALPHA) -> dict:
    t = PairedTable(a, b, c, d)
    cmp = compare_methods(t)
    crit = chi2_critical(alpha)
    stat, p = cmp["chi2_sem_correcao"], cmp["p_chi2_sem_correcao"]
    return {"table": t, "n": b + c, "chi2": stat, "critical": crit, "p": p,
            "reject": stat > crit and p < alpha,
            "before": t.pre_correct / t.n if t.n else float("nan"),
            "after": t.post_correct / t.n if t.n else float("nan")}


def classic_example_render(a: int, b: int, c: int, d: int):
    s = classic_example_state(a, b, c, d)
    print(f"Etapa 1  a = {a}, b = {b}, c = {c}, d = {d};  n = b + c = {s['n']}")
    print("Etapa 2  H0: π1+ = π+1   ×   H1: π1+ ≠ π+1")
    if s["n"] == 0:
        print("Sem pares discordantes: nada a testar.")
        return s
    print(f"Etapa 3.1  χ² = ({b} − {c})² / ({b} + {c}) = {(b - c) ** 2} / {s['n']} = {s['chi2']:.4g}")
    print(f"Etapa 3.2  χ²crítico(0,05; 1) = {s['critical']:.3f}")
    print(f"Etapa 3.3  p-valor = {s['p']:.6g}")
    verdict = "Rejeita-se H0" if s["reject"] else "Não se rejeita H0"
    print(f"Etapa 3.4  {verdict}. Aprovados: {s['before']:.0%} antes → {s['after']:.0%} depois.")
    pc.contingency(s["table"], labels=("Aprovado", "Reprovado"), axis_titles=("Antes", "Depois")).show()
    pc.chi2_critical(s["chi2"]).show()
    return s


def classic_example_tab():
    t = MONITORIA
    controls = {"a": _slider("a — aprovado → aprovado", t.a), "b": _slider("b — aprovado → reprovado", t.b),
                "c": _slider("c — reprovado → aprovado", t.c), "d": _slider("d — reprovado → reprovado", t.d)}
    return _panel(controls, classic_example_render, "Slide: 45, 10, 30, 15 → χ² = 10, p = 0,001565.")


# ---------------------------------------------------------------- slide 17: Ilustração #2 (exato)

def exact_example_state(a: int, b: int, c: int, d: int) -> dict:
    t = PairedTable(a, b, c, d)
    n, k = b + c, min(b, c)
    probs = [comb(n, i) / 2**n for i in range(k + 1)] if n else []
    tail = sum(probs) if n else 1.0
    p = min(1.0, 2 * tail) if n else 1.0
    return {"table": t, "n": n, "k": k, "probs": probs, "tail": tail, "p": p, "significant": p < ALPHA,
            "before": t.pre_correct / t.n if t.n else float("nan"),
            "after": t.post_correct / t.n if t.n else float("nan")}


def exact_example_render(a: int, b: int, c: int, d: int):
    s = exact_example_state(a, b, c, d)
    n, k = s["n"], s["k"]
    print(f"Etapa 1  a = {a}, b = {b}, c = {c}, d = {d};  n = b + c = {n}")
    print("Etapa 2  H0: π1+ = π+1   ×   H1: π1+ ≠ π+1")
    if n == 0:
        print("Sem pares discordantes: nada a testar, p = 1.")
        return s
    print(f"Etapa 3.1  X ~ Bin({n}; 0,5), k = min(b, c) = {k}")
    shown = list(enumerate(s["probs"]))
    if len(shown) > 8:
        shown = shown[:4] + shown[-2:]
    for i, pr in shown:
        print(f"   P(X = {i}) = C({n},{i}) · 0,5^{n} = {pr:.4g}")
    print(f"   P(X ≤ {k}) = {s['tail']:.6g}")
    print(f"   p-valor = 2 · P(X ≤ {k}) = {2 * s['tail']:.6g}" + ("  (limitado a 1)" if 2 * s["tail"] > 1 else ""))
    verdict = "Rejeita-se H0" if s["significant"] else "Não se rejeita H0"
    print(f"Etapa 3.2  {verdict}. Intenção de compra: {s['before']:.0%} antes → {s['after']:.0%} depois.")
    pc.contingency(s["table"], labels=("Compraria", "Não compraria"), axis_titles=("Antes", "Depois")).show()
    pc.binomial_null(b, c).show()
    return s


def exact_example_tab():
    t = CAMPANHA
    controls = {"a": _slider("a — compraria → compraria", t.a), "b": _slider("b — compraria → não", t.b),
                "c": _slider("c — não → compraria", t.c), "d": _slider("d — não → não", t.d)}
    return _panel(controls, exact_example_render, "Slide: 42, 3, 12, 43 → n = 15, k = 3, p = 0,03516.")


# ---------------------------------------------------------------- slide 25: Safe Fall (inferido)

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
    tag = "INFERIDO" if s["is_inferred"] else "HIPOTÉTICO (mesmas margens)"
    pc.contingency(t, title=f"Tabela 2 × 2 — {tag}").show()
    pc.transitions(t, title=f"Transições pré → pós — {variable}").show()
    pc.binomial_null(t.b, t.c).show()
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


# ---------------------------------------------------------------- todas as abas

def slide_examples_widget():
    """Abas com os exemplos ajustáveis, na ordem dos slides."""
    from .interactive_demo import mcnemar_widget

    w = _w()
    c = CAMPANHA
    tabs = [
        ("Slide 10 · variantes", variants_tab()),
        ("Slide 15 · Ilustração #1", classic_example_tab()),
        ("Slide 17 · Ilustração #2", exact_example_tab()),
        ("Slide 25 · Safe Fall", safe_fall_tab()),
        ("Slide 29 · demonstração", mcnemar_widget(b=c.b, c=c.c, a=c.a, d=c.d)),
    ]
    tab = w.Tab(children=[t[1] for t in tabs])
    for i, (title, _) in enumerate(tabs):
        tab.set_title(i, title)
    return tab
