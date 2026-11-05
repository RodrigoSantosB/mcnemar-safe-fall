"""Tabela de contingência 2×2 para dados pareados.

Convenção usada em todo o projeto (linhas = pré, colunas = pós)::

                    Pós: correto   Pós: incorreto
    Pré: correto          a               b
    Pré: incorreto        c               d

``b`` = piorou (correto → incorreto); ``c`` = melhorou (incorreto → correto).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd

from .data_validation import validate_paired


@dataclass(frozen=True)
class PairedTable:
    a: int
    b: int
    c: int
    d: int

    def __post_init__(self):
        for name in "abcd":
            value = getattr(self, name)
            if int(value) != value or value < 0:
                raise ValueError(f"Célula {name} deve ser inteiro não negativo (recebido {value}).")

    @classmethod
    def from_paired(cls, pre: Sequence, post: Sequence) -> "PairedTable":
        """Conta as quatro transições a partir de vetores 0/1 (1 = correto)."""
        pre_arr, post_arr = validate_paired(pre, post)
        return cls(
            a=int(np.sum((pre_arr == 1) & (post_arr == 1))),
            b=int(np.sum((pre_arr == 1) & (post_arr == 0))),
            c=int(np.sum((pre_arr == 0) & (post_arr == 1))),
            d=int(np.sum((pre_arr == 0) & (post_arr == 0))),
        )

    @property
    def n(self) -> int:
        return self.a + self.b + self.c + self.d

    @property
    def discordant(self) -> int:
        """Pares discordantes b + c — a única informação usada pelo teste."""
        return self.b + self.c

    @property
    def concordant(self) -> int:
        return self.a + self.d

    @property
    def pre_correct(self) -> int:
        return self.a + self.b

    @property
    def post_correct(self) -> int:
        return self.a + self.c

    def to_array(self) -> np.ndarray:
        """Formato aceito por ``statsmodels.stats.contingency_tables.mcnemar``."""
        return np.array([[self.a, self.b], [self.c, self.d]])

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.to_array(),
            index=["Pré: correto", "Pré: incorreto"],
            columns=["Pós: correto", "Pós: incorreto"],
        )

    def transitions(self) -> pd.DataFrame:
        """Tabela longa com os quatro tipos de transição."""
        return pd.DataFrame(
            {
                "transicao": [
                    "Correto → correto",
                    "Correto → incorreto",
                    "Incorreto → correto",
                    "Incorreto → incorreto",
                ],
                "celula": list("abcd"),
                "n": [self.a, self.b, self.c, self.d],
                "tipo": ["concordante", "discordante", "discordante", "concordante"],
            }
        )
