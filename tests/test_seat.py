"""
  " Tests for seat.py
  """
import pytest
from ..src import card
from ..src import player
from ..src import seat


@pytest.fixture
def s():
    s = seat.Seat(1)
    return s


@pytest.fixture
def p():
    p = player.Player("Erik")
    p.bank = 1000
    return p


def test_init_newseat_playerNone(s):
    assert s.player is None


# Test that the players name shows up
def test_str_playersitting_returnsName(s, p):
    s.sitdown(p)
    assert s.__str__() == 'Erik'


# If no player is sitting, returns 'Open Seat'
def test_str_empty_returnsOpenSeat(s):
    assert s.__str__() == 'Open Seat'


# Same seat, no player, are equal
def test_eq_sameseat_noplayer_returnsTrue(s):
    seatcopy = s
    assert s == seatcopy


# Different seats, not equal
def test_eq_different_returnsFalse(s):
    s2 = seat.Seat(2)
    assert s != s2


# Different seats, same players, not equal
def test_eq_diffseats_sameplayers_returnsFalse(s, p):
    s2 = seat.Seat(2)
    s.sitdown(p)
    s2.sitdown(p)
    assert s != s2


# Same seats, same players, equal
def test_eq_sameseats_sameplayers_returnsTrue(s, p):
    s2 = seat.Seat(1)
    s.sitdown(p)
    s2.sitdown(p)
    assert s == s2


def test_eq_sameplayers_diffstacks_returnsFalse(s, p):
    """ Same seats, same players, diff stacks, not equal """
    s2 = seat.Seat(1)
    s.sitdown(p)
    s2.sitdown(p)
    s.buy_chips(100)
    s2.buy_chips(300)
    assert s != s2


def test_sitdown_player_isnotEmpty(s, p):
    s.sitdown(p)
    assert s.vacant() is False


def test_sitdown_player_matchesSeatPlayer(s, p):
    s.sitdown(p)
    assert s.player == p


def test_standup_existingplayer_isempty(s, p):
    s.sitdown(p)
    s.standup()
    assert s.vacant()


def test_standup_playerwithchips_0chips(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    s.standup()
    assert s.stack == 0


def test_standup_playersitting_returnsPlayer(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.standup() == p


def test_vacant_emptyseat_returnsTrue(s):
    assert s.vacant()


def test_occupied_emptyseat_returnsFalse(s):
    assert s.occupied() == False


def test_occupied_filledseat_returnsTrue(s, p):
    s.sitdown(p)
    assert s.occupied()


def test_hashand_emptyseat_returnsFalse(s):
    assert s.has_hand() is False


def test_hashand_filledseat_nohand_returnsFalse(s, p):
    s.sitdown(p)
    assert s.has_hand() is False


def test_hashand_1card_returnsTrue(s, p):
    s.sitdown(p)
    s.hand.add(card.Card('A', 's'))
    assert s.has_hand()


def test_haschips_playerboughtchips_returnsTrue(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.has_chips()


def test_haschips_playerdidnotbuychips_returnsFalse(s, p):
    s.sitdown(p)
    assert s.has_chips() is False


def test_buychips_emptyseat_raiseValueError(s):
    with pytest.raises(ValueError):
        s.buy_chips(100)


def test_buychips_negamount_raiseValueError(s, p):
    s.sitdown(p)
    with pytest.raises(ValueError):
        s.buy_chips(-1)


def test_buychips_exceedsplayerbank_raiseException(s, p):
    s.sitdown(p)
    with pytest.raises(ValueError):
        s.buy_chips(100000000)


def test_buychips_100_returns100(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.stack == 100


def test_buychips_buy100twice_returns200(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    s.buy_chips(100)
    assert s.stack == 200


def test_win_negamount_raiseException(s, p):
    s.sitdown(p)
    with pytest.raises(ValueError):
        s.win(-1)


def test_win_100_stackis100(s, p):
    s.sitdown(p)
    s.win(100)
    assert s.stack == 100


def test_bet_stack100_bets10_returns10(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.bet(10) == 10


def test_bet_stack100_bets10_stack90(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    s.bet(10)
    assert s.stack == 90


#  def test_bet_broke_raiseException():
    #  s.sitdown(p)
    #  assertRaises(ValueError, s.bet, 10)


def test_bet_stack100_bets100_return100(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.bet(100) == 100


def test_bet_overstack_returnsStack(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    assert s.bet(1000) == 100


def test_bet_stack100_bets0_raiseException(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    with pytest.raises(ValueError):
        s.bet(0)


def test_bet_stack100_betsNegative_raiseException(s, p):
    s.sitdown(p)
    s.buy_chips(100)
    with pytest.raises(ValueError):
        s.bet(-1)


# Folding 1 card. Player has no cards
def test_fold_1card_handisempty(s):
    c = card.Card('A', 's')
    s.hand.add(c)
    s.fold()
    assert len(s.hand) == 0


# Folding 1 card. Returns 1 card.
def test_fold_1card_return1card(s):
    c = card.Card('A', 's')
    s.hand.add(c)
    h = s.fold()
    assert len(h) == 1


# Folding 0 cards, Returns empty list.
def test_fold_0cards_returnEmptyList(s):
    h = s.fold()
    assert len(h) == 0
