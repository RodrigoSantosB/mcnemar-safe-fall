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
