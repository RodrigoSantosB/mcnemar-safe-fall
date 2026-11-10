"""Teste de McNemar: versão exata (binomial) e aproximações qui-quadrado.

Sob H0 cada par discordante tem a mesma chance de ser "piorou" (b) ou
"melhorou" (c), logo, condicionado a n = b + c::

    B ~ Binomial(n, 0,5)

P-valor exato bilateral (distribuição simétrica)::

    p = min(1, 2 · P(B ≤ min(b, c)))

que coincide com a regra "somar as probabilidades ≤ à do valor observado"
usada por ``scipy.stats.binomtest`` quando p0 = 0,5.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb

import numpy as np
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar

from .contingency_tables import PairedTable

ALPHA = 0.05


def binomial_null_pmf(n: int) -> np.ndarray:
    """P(B = k), k = 0..n, sob H0: B ~ Binomial(n, 0,5)."""
    return stats.binom.pmf(np.arange(n + 1), n, 0.5)


def exact_pvalue_manual(b: int, c: int) -> float:
    """P-valor exato bilateral calculado "à mão" com aritmética racional.

    p = 2 · Σ_{k=0}^{min(b,c)} C(n, k) / 2^n, limitado a 1.
    Com b = c = 0 não há informação contra H0 e p = 1.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = Fraction(sum(comb(n, i) for i in range(k + 1)), 2**n)
    return float(min(Fraction(1), 2 * tail))


def midp_pvalue(b: int, c: int) -> float:
    """P-valor mid-p: 2 · [P(X < k) + 0,5 · P(X = k)], k = min(b, c), limitado a 1."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    below = Fraction(sum(comb(n, i) for i in range(k)), 2**n)
    at = Fraction(comb(n, k), 2**n)
    return float(min(Fraction(1), 2 * (below + at / 2)))


def chi2_critical(alpha: float = ALPHA) -> float:
    """Valor crítico da qui-quadrado com 1 gl (3,841 para α = 0,05)."""
    return float(stats.chi2.isf(alpha, df=1))


def exact_pvalue_scipy(b: int, c: int) -> float:
    """Validação independente via ``scipy.stats.binomtest`` (bilateral)."""
    if b + c == 0:
        return 1.0
    return float(stats.binomtest(b, b + c, 0.5, alternative="two-sided").pvalue)


def chi2_statistic(b: int, c: int, correction: bool) -> float:
    """Estatística assintótica: (|b−c| − corr)² / (b + c), corr = 1 (Edwards) ou 0."""
    if b + c == 0:
        return 0.0
    diff = abs(b - c) - (1 if correction else 0)
    return max(diff, 0) ** 2 / (b + c)


def chi2_pvalue(b: int, c: int, correction: bool) -> float:
    return float(stats.chi2.sf(chi2_statistic(b, c, correction), df=1))


@dataclass(frozen=True)
class McNemarResult:
    table: PairedTable
    statistic: float
    """Estatística do teste exato = min(b, c) (convenção do statsmodels)."""
    pvalue: float
    pvalue_manual: float
    pvalue_scipy: float
    alpha: float = ALPHA

    @property
    def significant(self) -> bool:
        return self.pvalue < self.alpha

    @property
    def consistent(self) -> bool:
        """Manual, scipy e statsmodels concordam (tolerância relativa 1e-9)."""
        return bool(
            np.isclose(self.pvalue, self.pvalue_manual, rtol=1e-9, atol=1e-300)
            and np.isclose(self.pvalue, self.pvalue_scipy, rtol=1e-9, atol=1e-300)
        )

    def summary(self) -> dict:
        t = self.table
        return {
            "a": t.a,
            "b (piorou)": t.b,
            "c (melhorou)": t.c,
            "d": t.d,
            "discordantes": t.discordant,
            "estatística min(b,c)": self.statistic,
            "p exato": self.pvalue,
            "p formatado": format_p(self.pvalue),
            "significativo (5%)": self.significant,
        }


def mcnemar_exact(table: PairedTable, alpha: float = ALPHA) -> McNemarResult:
    """Teste exato de McNemar via statsmodels, validado por duas outras rotas."""
    res = sm_mcnemar(table.to_array(), exact=True)
    return McNemarResult(
        table=table,
        statistic=float(res.statistic),
        pvalue=float(res.pvalue),
        pvalue_manual=exact_pvalue_manual(table.b, table.c),
        pvalue_scipy=exact_pvalue_scipy(table.b, table.c),
        alpha=alpha,
    )


def compare_methods(table: PairedTable) -> dict:
    """As quatro variantes: χ² clássico, χ² com correção de Edwards, exato e mid-p."""
    b, c = table.b, table.c
    sm_uncorr = sm_mcnemar(table.to_array(), exact=False, correction=False)
    sm_corr = sm_mcnemar(table.to_array(), exact=False, correction=True)
    return {
        "b": b,
        "c": c,
        "n_discordantes": b + c,
        "p_exato": exact_pvalue_manual(b, c),
        "chi2_sem_correcao": float(sm_uncorr.statistic),
        "p_chi2_sem_correcao": float(sm_uncorr.pvalue),
        "chi2_com_correcao": float(sm_corr.statistic),
        "p_chi2_com_correcao": float(sm_corr.pvalue),
        "p_midp": midp_pvalue(b, c),
    }


def format_p(p: float, decimals: int = 3) -> str:
    """Notação de relatório: nunca "p = 0,000"."""
    threshold = 10 ** (-decimals)
    if p < threshold:
        return f"p < {threshold:.{decimals}f}".replace(".", ",")
    return f"p = {p:.{decimals}f}".replace(".", ",")


def odds_ratio_discordant(table: PairedTable) -> float:
    """Razão de chances pareada c/b (direção e magnitude da mudança)."""
    if table.b == 0:
        return float("inf") if table.c > 0 else float("nan")
    return table.c / table.b


def interpret(result: McNemarResult) -> str:
    """Interpretação em linguagem aplicada."""
    t = result.table
    n = t.discordant
    if n == 0:
        return (
            "Nenhum indivíduo mudou de resposta (b = c = 0): o teste não tem informação "
            "para detectar mudança; p = 1."
        )
    direction = (
        "mais indivíduos melhoraram do que pioraram"
        if t.c > t.b
        else "mais indivíduos pioraram do que melhoraram"
        if t.b > t.c
        else "as mudanças estão equilibradas"
    )
    verdict = (
        f"Rejeitamos H0 ao nível de {result.alpha:.0%}"
        if result.significant
        else f"Não rejeitamos H0 ao nível de {result.alpha:.0%}"
    )
    return (
        f"Entre os {n} pares discordantes, {t.c} melhoraram e {t.b} pioraram — {direction}. "
        f"Sob H0 esperaríamos {n / 2:.1f}".replace(".", ",") + f" em cada sentido. {format_p(result.pvalue)}. "
        f"{verdict}: "
        + (
            "a proporção de acertos mudou entre pré e pós."
            if result.significant
            else "os dados são compatíveis com ausência de mudança."
        )
    ).replace(".0%", "%")
