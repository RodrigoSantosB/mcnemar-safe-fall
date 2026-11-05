import pytest

from safe_fall_statistics.data_loader import N_TOTAL, load_published_table1
from safe_fall_statistics.data_validation import audit_table1, check_row_totals
from safe_fall_statistics.reconstruction import (
    feasible_range,
    reconstruct_from_chi2,
    reconstruct_table1,
)


@pytest.fixture(scope="module")
def table1():
    return load_published_table1()


def test_published_counts_sum_to_n(table1):
    assert check_row_totals(table1).all()


def test_audit_flags_known_divergences(table1):
    audit = audit_table1(table1)
    flagged = set(zip(audit.loc[audit.divergente, "variavel"], audit.loc[audit.divergente, "celula"]))
    # 107/122 = 87,7 %, mas a tabela imprime 90,2 % (mesmo valor da linha do pescoço)
    assert ("Não apoiar as mãos", "post_correct") in flagged
    assert ("Flexão do pescoço", "pre_correct") in flagged
    # A linha do quadril no pós-teste é consistente
    assert ("Flexão do quadril", "post_correct") not in flagged


def test_reconstruction_is_integer_and_feasible_with_continuity_correction(table1):
    rec = reconstruct_table1(table1, correction=True)
    assert rec["viavel"].all()
    assert (rec["X2_recalculado"] == rec["X2_publicado"].round(3)).all()
    assert list(zip(rec.b, rec.c)) == [(2, 84), (0, 106), (2, 104), (0, 105), (2, 50)]


def test_reconstruction_fails_without_continuity_correction(table1):
    rec = reconstruct_table1(table1, correction=False)
    assert not rec["viavel"].any()


def test_reconstructed_tables_reproduce_published_margins(table1):
    for _, r in table1.iterrows():
        rec = reconstruct_from_chi2(r.pre_correct_n, r.post_correct_n, r.chi2_reported)
        t = rec.table
        assert t.n == N_TOTAL
        assert t.pre_correct == r.pre_correct_n
        assert t.post_correct == r.post_correct_n


def test_margins_alone_do_not_identify_table():
    lo, hi = feasible_range(pre_correct=28, post_correct=110)
    assert hi - lo >= 10  # muitas tabelas compatíveis com as mesmas margens
