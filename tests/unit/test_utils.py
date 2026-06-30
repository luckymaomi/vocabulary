from core.utils import natural_sort_key, normalize_word


def test_normalize_word_keeps_letters_hyphen_and_apostrophe():
    assert normalize_word("  Mother's-in-law!!!  ") == "mother's-in-law"


def test_normalize_word_handles_none():
    assert normalize_word(None) == ""


def test_natural_sort_key_orders_numbers_by_value():
    names = ["S10-20.txt", "S2-10.txt", "S1-2.txt"]
    assert sorted(names, key=natural_sort_key) == ["S1-2.txt", "S2-10.txt", "S10-20.txt"]
