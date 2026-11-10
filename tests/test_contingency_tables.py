import numpy as np
import pytest

from safe_fall_statistics.contingency_tables import PairedTable
from safe_fall_statistics.data_validation import validate_paired
from safe_fall_statistics.synthetic_data import CAMPANHA, individuals_from_table, simulate_paired_study


def test_from_paired_counts_each_transition():
    pre = [1, 1, 1, 0, 0, 0, 0]
    post = [1, 0, 1, 1, 1, 0, 1]
    t = PairedTable.from_paired(pre, post)
    assert (t.a, t.b, t.c, t.d) == (2, 1, 3, 1)


def test_sample_total_preserved():
    df = simulate_paired_study(n=137, p_pre=0.3, p_improve=0.6, p_worsen=0.1, seed=7)
    t = PairedTable.from_paired(df["pre"], df["pos"])
    assert t.n == 137
    assert t.pre_correct == df["pre"].sum()
    assert t.post_correct == df["pos"].sum()


def test_discordant_pairs_identified():
    t = PairedTable(a=26, b=2, c=84, d=10)
    assert t.discordant == 86
    assert t.concordant == 36
    assert t.post_correct - t.pre_correct == t.c - t.b


def test_round_trip_individuals_to_table():
    df = individuals_from_table(CAMPANHA, seed=1)
    assert PairedTable.from_paired(df["pre"], df["pos"]) == CAMPANHA


def test_to_array_layout_matches_statsmodels_convention():
    t = PairedTable(1, 2, 3, 4)
    np.testing.assert_array_equal(t.to_array(), [[1, 2], [3, 4]])


@pytest.mark.parametrize("bad", [-1, 2.5])
def test_invalid_cells_rejected(bad):
    with pytest.raises(ValueError):
        PairedTable(bad, 0, 0, 0)


def test_missing_values_rejected():
    with pytest.raises(ValueError, match="ausente"):
        validate_paired([1, 0, None], [1, 1, 0])


def test_unpaired_lengths_rejected():
    with pytest.raises(ValueError, match="pareados"):
        validate_paired([1, 0, 1], [1, 1])


def test_non_dichotomous_rejected():
    with pytest.raises(ValueError, match="dicotômica"):
        validate_paired([1, 0, 2], [1, 1, 0])


def test_boolean_input_accepted():
    pre, post = validate_paired([True, False], [True, True])
    assert pre.tolist() == [1, 0] and post.tolist() == [1, 1]
