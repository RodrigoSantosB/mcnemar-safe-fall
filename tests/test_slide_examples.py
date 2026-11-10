import matplotlib

matplotlib.use("Agg")

import pytest  # noqa: E402

from safe_fall_statistics.slide_examples import (  # noqa: E402
    classic_example_state,
    exact_example_state,
    safe_fall_state,
    slide_examples_widget,
    variants_state,
)


def test_classic_example_matches_document():
    s = classic_example_state(45, 10, 30, 15)
    assert s["chi2"] == pytest.approx(10.0)
    assert s["critical"] == pytest.approx(3.841, abs=5e-4)
    assert s["p"] == pytest.approx(0.001565, abs=5e-7)
    assert s["reject"]
    assert (s["before"], s["after"]) == (pytest.approx(0.55), pytest.approx(0.75))


def test_exact_example_matches_document():
    s = exact_example_state(42, 3, 12, 43)
    assert (s["n"], s["k"]) == (15, 3)
    assert s["probs"][0] == pytest.approx(3.052e-5, rel=1e-3)
    assert s["probs"][3] == pytest.approx(1.389e-2, rel=1e-3)
    assert s["tail"] == pytest.approx(576 / 32768)
    assert s["p"] == pytest.approx(0.03516, abs=5e-6)
    assert (s["before"], s["after"]) == (pytest.approx(0.45), pytest.approx(0.54))
    assert exact_example_state(10, 0, 0, 10)["p"] == 1.0


def test_variants_state_has_four_versions():
    df = variants_state(3, 12).set_index("versão")
    assert len(df) == 4
    assert df.loc["Exata (binomial)", "p"] == pytest.approx(0.03515625)
    assert df.loc["Mid-p exata", "p"] < df.loc["Exata (binomial)", "p"]


def test_safe_fall_state_defaults_to_inferred_and_keeps_margins():
    s = safe_fall_state("Flexão do pescoço")
    assert s["is_inferred"] and (s["table"].b, s["table"].c) == (2, 84)
    alt = safe_fall_state("Flexão do pescoço", b=10)
    assert not alt["is_inferred"]
    assert alt["table"].pre_correct == 28 and alt["table"].post_correct == 110


def test_widget_builds_all_tabs():
    pytest.importorskip("ipywidgets")
    tab = slide_examples_widget()
    assert len(tab.children) == 5


def test_plotly_charts_build():
    import plotly.graph_objects as go

    from safe_fall_statistics import plotly_charts as pc
    from safe_fall_statistics.data_loader import load_published_table1
    from safe_fall_statistics.reconstruction import reconstructed_tables
    from safe_fall_statistics.synthetic_data import CAMPANHA, MONITORIA

    df = load_published_table1()
    figs = [pc.pre_post(df), pc.contingency(MONITORIA), pc.binomial_null(3, 12), pc.binomial_null(0, 0),
            pc.chi2_critical(10.0), pc.transitions(CAMPANHA), pc.exact_vs_asymptotic(15),
            pc.discordant_bars(reconstructed_tables(df)), pc.pvalue_bars(variants_state(3, 12))]
    assert all(isinstance(f, go.Figure) for f in figs)
    tail = figs[2].data[0].marker.color
    assert list(tail[:4]) == [pc.RED] * 4 and tail[7] == pc.CONCORDANT
