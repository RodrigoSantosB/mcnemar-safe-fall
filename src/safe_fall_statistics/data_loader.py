"""Leitura dos dados publicados no artigo."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

N_TOTAL = 122
"""Número de crianças avaliadas no pré e no pós-teste (Seção 2.1 do artigo)."""

SOURCE = (
    "DelCastillo-Andrés et al. (2018), Int. J. Environ. Res. Public Health 15:2669, "
    "Tabela 1. doi:10.3390/ijerph15122669 (CC BY 4.0)"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_published_table1(path: str | Path | None = None) -> pd.DataFrame:
    """Carrega a Tabela 1 exatamente como publicada (sem correções)."""
    path = Path(path) if path is not None else DATA_DIR / "table1_published.csv"
    df = pd.read_csv(path)
    df.attrs["source"] = SOURCE
    return df
