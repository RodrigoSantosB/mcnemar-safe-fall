"""Demonstração interativa "Como o McNemar funciona?" (ipywidgets)."""

from __future__ import annotations

from . import plotly_charts as pc
from .contingency_tables import PairedTable
from .mcnemar_analysis import interpret, mcnemar_exact


def demo_state(b: int, c: int, a: int = 0, d: int = 0) -> dict:
    """Tudo o que a demonstração mostra, calculado sem interface (testável)."""
    table = PairedTable(a, b, c, d)
    res = mcnemar_exact(table)
    return {
        "table": table,
        "discordant": table.discordant,
        "statistic": res.statistic,
        "pvalue": res.pvalue,
        "significant": res.significant,
        "consistent": res.consistent,
        "interpretation": interpret(res),
    }


def render(b: int, c: int, a: int = 0, d: int = 0):
    state = demo_state(b, c, a, d)
    pc.contingency(state["table"]).show()
    pc.binomial_null(b, c).show()
    print(
        f"Pares discordantes: b + c = {state['discordant']}   |   "
        f"estatística exata min(b,c) = {state['statistic']:.0f}   |   p exato = {state['pvalue']:.4g}"
    )
    print(state["interpretation"])
    return state


def mcnemar_widget(b: int = 3, c: int = 12, a: int = 15, d: int = 10, max_value: int = 120):
    """Controles deslizantes para b (pioraram) e c (melhoraram)."""
    import ipywidgets as w

    style = {"description_width": "190px"}
    layout = w.Layout(width="520px")
    sb = w.IntSlider(value=b, min=0, max=max_value, description="b — pioraram (C→I)", style=style, layout=layout)
    sc = w.IntSlider(value=c, min=0, max=max_value, description="c — melhoraram (I→C)", style=style, layout=layout)
    sa = w.IntSlider(value=a, min=0, max=max_value, description="a — continuaram corretos", style=style, layout=layout)
    sd = w.IntSlider(value=d, min=0, max=max_value, description="d — continuaram incorretos", style=style, layout=layout)
    note = w.HTML(
        "<i>a</i> e <i>d</i> mudam a tabela, mas <b>não</b> o p-valor: experimente."
    )
    out = w.interactive_output(lambda b, c, a, d: render(b, c, a, d), {"b": sb, "c": sc, "a": sa, "d": sd})
    return w.VBox([w.HBox([w.VBox([sc, sb]), w.VBox([sa, sd])]), note, out])
