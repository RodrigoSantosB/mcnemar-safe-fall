import matplotlib

matplotlib.use("Agg")

import pytest  # noqa: E402

from safe_fall_statistics.slide_examples import (  # noqa: E402
    methods_state,
    safe_fall_state,
    slide_examples_widget,
    worked_example_state,
)


def test_worked_example_matches_slide():
    s = worked_example_state(2, 10)
    assert s["terms"] == [1, 12, 66]
    assert s["p"] == pytest.approx(158 / 4096)
    assert worked_example_state(0, 0)["p"] == 1.0


def test_methods_state_reproduces_slide_table():
    df = methods_state(8, 1).set_index("método")
    assert df.loc["Exato (binomial)", "p"] == pytest.approx(0.0703125)
    assert df.loc["χ² sem correção", "p"] == pytest.approx(0.0339, abs=1e-4)
    assert not df.loc["Exato (binomial)", "rejeita H0 (5%)"]


def test_safe_fall_state_defaults_to_inferred_and_keeps_margins():
    s = safe_fall_state("Flexão do pescoço")
    assert s["is_inferred"] and (s["table"].b, s["table"].c) == (2, 84)
    alt = safe_fall_state("Flexão do pescoço", b=10)
    assert not alt["is_inferred"]
    assert alt["table"].pre_correct == 28 and alt["table"].post_correct == 110


def test_widget_builds_all_tabs():
    pytest.importorskip("ipywidgets")
    tab = slide_examples_widget()
    assert len(tab.children) == 7
