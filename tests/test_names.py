"""
  " Tests for names.py
  """
from ..src import names


def test_randomnames_10_returns10names():
    namelist = names.random_names(10, names.pokerplayers)
    assert len(namelist) == 10


def test_randomnames_10_isset():
    qty = 10
    namelist = names.random_names(qty, names.pokerplayers)
    assert len(set(namelist)) == qty


def test_isvalidname_2char_returnsFalse():
    name = 'qz'
    assert names.is_validname(name) is False


def test_isvalidname_20char_returnsTrue():
    name = 'qzqzqzqzqzqzqzqzqzqz'
    assert names.is_validname(name)


def test_isvalidname_21char_returnsFalse():
    name = 'qzqzqzqzqzqzqzqzqzqzz'
    assert len(name) == 21
    assert names.is_validname(name) is False


def test_isvalidname_10char_returnsFalse():
    name = 'eriktheguy'
    assert names.is_validname(name)


def test_hassurrchar_angle_returnsTrue():
    name = 'eriktheguy>'
    assert names.has_surr_char(name)


def test_hassurrchar_brace_returnsTrue():
    name = 'eriktheguy}'
    assert names.has_surr_char(name)


def test_hassurrchar_parentheses_returnsTrue():
    name = '(eriktheguy)'
    assert names.has_surr_char(name)


def test_hassurrchar_bracket_returnsTrue():
    name = '[eriktheguy]'
    assert names.has_surr_char(name)


def test_hassurrchar_fslash_returnsTrue():
    name = '/eriktheguy/'
    assert names.has_surr_char(name)


def test_hassurrchar_bslash_returnsTrue():
    name = 'eriktheguy\\'
    assert names.has_surr_char(name)


def test_hassurrchar_tilde_returnsFalse():
    name = '~eriktheguy'
    assert names.has_surr_char(name) is False


def test_hassurrchar_backtick_returnsTrue():
    name = '`eriktheguy'
    assert names.has_surr_char(name)


def test_hassurrchar_caret_returnsFalse():
    name = '^eriktheguy'
    assert names.has_surr_char(name) is False


def test_hassurrchar_singlequote_returnsTrue():
    name = '\'eriktheguy'
    assert names.has_surr_char(name)


def test_hassurrchar_normal_returnsFalsej():
    name = 'eriktheguy'
    assert names.has_surr_char(name) is False
