"""Dados SINTÉTICOS para fins didáticos. Nunca são resultados do artigo."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .contingency_tables import PairedTable

SYNTHETIC_LABEL = "SINTÉTICO — exemplo didático, não é dado do estudo"

MONITORIA = PairedTable(a=45, b=10, c=30, d=15)
"""Ilustração #1 do roteiro: 100 alunos avaliados antes e depois de uma monitoria (aprovado/reprovado)."""

CAMPANHA = PairedTable(a=42, b=3, c=12, d=43)
"""Ilustração #2 do roteiro: 100 consumidores antes e depois de uma campanha (compraria/não compraria)."""


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
