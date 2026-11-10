from math import comb

import pytest

from safe_fall_statistics.contingency_tables import PairedTable
from safe_fall_statistics.synthetic_data import CAMPANHA, MONITORIA
from safe_fall_statistics.interactive_demo import demo_state
from safe_fall_statistics.mcnemar_analysis import (
    chi2_statistic,
    chi2_critical,
    compare_methods,
    midp_pvalue,
    exact_pvalue_manual,
    exact_pvalue_scipy,
    format_p,
    mcnemar_exact,
)


def test_exact_pvalue_hand_computed():
    # b=2, c=10: p = 2 * (C(12,0)+C(12,1)+C(12,2)) / 2^12 = 158/4096
    assert exact_pvalue_manual(2, 10) == pytest.approx(158 / 4096)
    assert exact_pvalue_manual(2, 10) == pytest.approx(
        2 * sum(comb(12, k) for k in range(3)) / 2**12
    )


def test_zero_discordant_pairs_gives_p_one():
    res = mcnemar_exact(PairedTable(30, 0, 0, 12))
    assert res.pvalue == 1.0
    assert res.pvalue_manual == 1.0
    assert not res.significant
    assert demo_state(0, 0)["pvalue"] == 1.0


@pytest.mark.parametrize("k", [1, 5, 20])
def test_balanced_changes_give_p_one(k):
    assert exact_pvalue_manual(k, k) == 1.0
    assert mcnemar_exact(PairedTable(10, k, k, 10)).pvalue == pytest.approx(1.0)


@pytest.mark.parametrize(
    "b,c", [(0, 1), (1, 7), (2, 10), (5, 9), (3, 13), (2, 84), (0, 106), (2, 50), (40, 25)]
)
def test_manual_scipy_statsmodels_agree(b, c):
    res = mcnemar_exact(PairedTable(10, b, c, 10))
    assert res.consistent
    assert res.pvalue_scipy == pytest.approx(exact_pvalue_scipy(b, c))
    assert res.statistic == min(b, c)


def test_symmetry_in_b_and_c():
    assert exact_pvalue_manual(3, 13) == exact_pvalue_manual(13, 3)


def test_concordant_cells_do_not_change_pvalue():
    assert mcnemar_exact(PairedTable(0, 3, 12, 0)).pvalue == mcnemar_exact(PairedTable(500, 3, 12, 77)).pvalue


def test_chi2_statistics():
    assert chi2_statistic(1, 7, correction=False) == pytest.approx(36 / 8)
    assert chi2_statistic(1, 7, correction=True) == pytest.approx(25 / 8)
    assert chi2_statistic(0, 0, correction=True) == 0.0


def test_exact_and_asymptotic_can_disagree():
    cmp = compare_methods(PairedTable(10, 1, 7, 12))
    assert cmp["p_exato"] > 0.05
    assert cmp["p_chi2_sem_correcao"] < 0.05


def test_format_p_never_prints_zero():
    assert format_p(1e-30) == "p < 0,001"
    assert format_p(0.0386) == "p = 0,039"


def test_midp_matches_definition():
    # n = 15, k = 3: 2·[P(X ≤ 2) + 0,5·P(X = 3)]
    assert midp_pvalue(3, 12) == pytest.approx(2 * ((1 + 15 + 105) + 455 / 2) / 2**15)
    assert midp_pvalue(0, 0) == 1.0
    assert midp_pvalue(5, 5) <= 1.0


def test_chi2_critical_value():
    assert chi2_critical() == pytest.approx(3.8415, abs=1e-4)


def test_document_illustrations():
    m = compare_methods(MONITORIA)
    assert m["chi2_sem_correcao"] == pytest.approx(10.0)
    assert m["p_chi2_sem_correcao"] == pytest.approx(0.001565, abs=5e-7)
    assert compare_methods(CAMPANHA)["p_exato"] == pytest.approx(0.03516, abs=5e-6)
