"""Inferência das tabelas 2×2 do Safe Fall a partir do que foi publicado.

As margens sozinhas NÃO identificam a tabela: elas fixam apenas a diferença
``c − b = (pós correto) − (pré correto)``, mas não ``b + c``. Porém a Tabela 1
também publica um "X²". Se esse X² for o qui-quadrado de McNemar com correção
de continuidade (o que o SPSS reporta para McNemar), então::

    X² = (|c − b| − 1)² / (b + c)   ⇒   b + c = (|c − b| − 1)² / X²

e o par (b, c) fica determinado. A hipótese é testável: ``b + c`` precisa sair
inteiro, as células precisam ser não negativas e o X² recalculado precisa
reproduzir o publicado nas 3 casas decimais impressas. O resultado é uma **inferência**, não um dado original.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .contingency_tables import PairedTable
from .data_loader import N_TOTAL


@dataclass(frozen=True)
class Reconstruction:
    variable: str
    table: PairedTable | None
    discordant_raw: float
    """(|D| − 1)² / X² antes de arredondar — deveria ser ~inteiro."""
    integer_gap: float
    feasible: bool
    chi2_check: float | None
    hypothesis: str


def reconstruct_from_chi2(
    pre_correct: int,
    post_correct: int,
    chi2: float,
    n_total: int = N_TOTAL,
    correction: bool = True,
    variable: str = "",
    integer_tol: float = 0.05,
) -> Reconstruction:
    diff = post_correct - pre_correct  # = c − b
    numerator = (abs(diff) - (1 if correction else 0)) ** 2
    raw = numerator / chi2
    n_disc = round(raw)
    gap = abs(raw - n_disc)
    hypothesis = "qui-quadrado com correção de continuidade" if correction else "qui-quadrado sem correção"

    table = None
    feasible = False
    chi2_check = None
    if gap <= integer_tol and (n_disc - abs(diff)) % 2 == 0 and n_disc >= abs(diff):
        b = (n_disc - diff) // 2
        c = n_disc - b
        a = pre_correct - b
        d = (n_total - pre_correct) - c
        if min(a, b, c, d) >= 0:
            chi2_check = (abs(b - c) - (1 if correction else 0)) ** 2 / (b + c)
            # o X² recalculado precisa reproduzir o publicado nas 3 casas impressas
            if abs(chi2_check - chi2) <= 0.0005 + 1e-12:
                table = PairedTable(a, b, c, d)
                feasible = True
    return Reconstruction(variable, table, raw, gap, feasible, chi2_check, hypothesis)


def reconstruct_table1(df: pd.DataFrame, correction: bool = True) -> pd.DataFrame:
    """Aplica a inferência às cinco linhas da Tabela 1."""
    rows = []
    for _, r in df.iterrows():
        rec = reconstruct_from_chi2(
            int(r["pre_correct_n"]),
            int(r["post_correct_n"]),
            float(r["chi2_reported"]),
            correction=correction,
            variable=r["variavel_pt"],
        )
        t = rec.table
        rows.append(
            {
                "variavel": rec.variable,
                "b+c (bruto)": round(rec.discordant_raw, 4),
                "viavel": rec.feasible,
                "a": t.a if t else None,
                "b": t.b if t else None,
                "c": t.c if t else None,
                "d": t.d if t else None,
                "X2_publicado": r["chi2_reported"],
                "X2_recalculado": round(rec.chi2_check, 3) if rec.chi2_check is not None else None,
            }
        )
    out = pd.DataFrame(rows)
    out.attrs["status"] = "INFERIDO — não é dado original do artigo"
    return out


def reconstructed_tables(df: pd.DataFrame) -> dict[str, PairedTable]:
    """Dicionário variável → PairedTable inferida (somente linhas viáveis)."""
    out = {}
    for _, r in df.iterrows():
        rec = reconstruct_from_chi2(
            int(r["pre_correct_n"]), int(r["post_correct_n"]), float(r["chi2_reported"])
        )
        if rec.feasible:
            out[r["variavel_pt"]] = rec.table
    return out


def feasible_range(pre_correct: int, post_correct: int, n_total: int = N_TOTAL) -> tuple[int, int]:
    """Faixa de b compatível só com as margens (mostra que margens não bastam)."""
    diff = post_correct - pre_correct
    b_min = max(0, -diff)
    b_max = min(pre_correct, n_total - post_correct)
    return b_min, b_max
