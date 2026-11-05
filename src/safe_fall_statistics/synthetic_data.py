"""Dados SINTÉTICOS para fins didáticos. Nunca são resultados do artigo."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .contingency_tables import PairedTable

SYNTHETIC_LABEL = "SINTÉTICO — exemplo didático, não é dado do estudo"

EDUCATION_EXAMPLE = PairedTable(a=15, b=3, c=13, d=9)
"""40 alunos respondem à mesma questão antes e depois de uma aula de reforço."""

SMALL_SIGNIFICANT = PairedTable(a=20, b=2, c=10, d=8)
SMALL_NOT_SIGNIFICANT = PairedTable(a=20, b=5, c=9, d=6)
EXACT_VS_ASYMPTOTIC = PairedTable(a=10, b=1, c=7, d=12)
"""Caso pequeno em que o qui-quadrado sem correção rejeita H0 e o exato não."""


def individuals_from_table(table: PairedTable, seed: int = 2018, id_prefix: str = "S") -> pd.DataFrame:
    """Gera microdados individuais (pré, pós) com exatamente as contagens da tabela.

    A ordem dos indivíduos é embaralhada com semente fixa; qualquer ordem gera a
    mesma tabela, portanto o teste não depende dela.
    """
    pre = [1] * table.a + [1] * table.b + [0] * table.c + [0] * table.d
    post = [1] * table.a + [0] * table.b + [1] * table.c + [0] * table.d
    rng = np.random.default_rng(seed)
    order = rng.permutation(table.n)
    df = pd.DataFrame({"pre": np.array(pre)[order], "pos": np.array(post)[order]})
    df.insert(0, "id", [f"{id_prefix}{i + 1:03d}" for i in range(table.n)])
    df.attrs["status"] = SYNTHETIC_LABEL
    return df


def simulate_paired_study(
    n: int, p_pre: float, p_improve: float, p_worsen: float, seed: int = 2018
) -> pd.DataFrame:
    """Simula um estudo pré/pós.

    Cada indivíduo começa correto com prob. ``p_pre``; quem está incorreto passa
    a correto com prob. ``p_improve``; quem está correto passa a incorreto com
    prob. ``p_worsen``.
    """
    rng = np.random.default_rng(seed)
    pre = rng.random(n) < p_pre
    u = rng.random(n)
    post = np.where(pre, u >= p_worsen, u < p_improve)
    df = pd.DataFrame({"id": [f"S{i + 1:03d}" for i in range(n)], "pre": pre.astype(int), "pos": post.astype(int)})
    df.attrs["status"] = SYNTHETIC_LABEL
    return df
