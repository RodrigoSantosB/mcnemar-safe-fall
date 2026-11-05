"""Validação de dados: auditoria da Tabela 1 e checagem de dados pareados."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

from .data_loader import N_TOTAL

_PCT_COLUMNS = {
    "pre_correct": ("pre_correct_n", "pre_correct_pct_reported"),
    "pre_incorrect": ("pre_incorrect_n", "pre_incorrect_pct_reported"),
    "post_correct": ("post_correct_n", "post_correct_pct_reported"),
    "post_incorrect": ("post_incorrect_n", "post_incorrect_pct_reported"),
}


def audit_table1(df: pd.DataFrame, n_total: int = N_TOTAL) -> pd.DataFrame:
    """Compara cada porcentagem impressa com a recalculada (n / N · 100).

    A tolerância é meia unidade da precisão impressa: 0,05 p.p. para valores com
    uma casa decimal e 0,5 p.p. para valores impressos como inteiros (ex.: "87").
    Diferenças acima disso não se explicam por arredondamento e são marcadas como
    ``divergente``. Nada é corrigido.
    """
    rows = []
    for _, r in df.iterrows():
        for label, (n_col, pct_col) in _PCT_COLUMNS.items():
            recalculated = 100 * r[n_col] / n_total
            diff = r[pct_col] - recalculated
            tol = 0.5 if float(r[pct_col]).is_integer() else 0.05
            rows.append(
                {
                    "variavel": r["variavel_pt"],
                    "celula": label,
                    "n": int(r[n_col]),
                    "pct_publicada": r[pct_col],
                    "pct_recalculada": round(recalculated, 2),
                    "diferenca_pp": round(diff, 2),
                    "divergente": abs(diff) > tol + 1e-9,
                }
            )
    return pd.DataFrame(rows)


def check_row_totals(df: pd.DataFrame, n_total: int = N_TOTAL) -> pd.Series:
    """True quando correto + incorreto = N, no pré e no pós."""
    pre = df["pre_correct_n"] + df["pre_incorrect_n"] == n_total
    post = df["post_correct_n"] + df["post_incorrect_n"] == n_total
    return pd.Series((pre & post).values, index=df["variavel_pt"], name="totais_ok")


def validate_paired(pre: Sequence, post: Sequence) -> tuple[np.ndarray, np.ndarray]:
    """Valida duas medidas dicotômicas do mesmo conjunto de indivíduos.

    Exige mesmo comprimento, ausência de valores faltantes e codificação 0/1
    (ou booleana). Retorna os vetores como ``np.ndarray`` de inteiros.
    """
    pre_s = pd.Series(pre)
    post_s = pd.Series(post)
    if len(pre_s) != len(post_s):
        raise ValueError(
            f"Pré ({len(pre_s)}) e pós ({len(post_s)}) têm tamanhos diferentes: "
            "os dados não são pareados."
        )
    missing = pre_s.isna() | post_s.isna()
    if missing.any():
        raise ValueError(
            f"{int(missing.sum())} indivíduo(s) com valor ausente; o McNemar exige o par completo."
        )
    for name, s in (("pré", pre_s), ("pós", post_s)):
        values = set(pd.unique(s.astype(int)))
        if not values <= {0, 1}:
            raise ValueError(f"Medida {name} não é dicotômica 0/1: valores {sorted(values)}.")
    return pre_s.astype(int).to_numpy(), post_s.astype(int).to_numpy()
