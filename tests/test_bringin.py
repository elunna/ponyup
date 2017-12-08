from ..src import tools

def test_bringin_stud5_no_ties_returns5(self):
    # Stud5 deal: seat 5 has lowest card, 9
    tools.deal_stud5(t, matchingranks=0)
    t.set_bringin()
    assert t.TOKENS['BI'] == 5


def test_bringin_stud5_2tied_returns1(self):
    # Stud5 deal: 2 Tied ranks
    tools.deal_stud5(t, matchingranks=2)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud5_3tied_returns1(self):
    # Stud5 deal: 3 Tied ranks
    tools.deal_stud5(t, matchingranks=3)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud5_4tied_returns1(self):
    # Stud5 deal: 4 Tied ranks
    tools.deal_stud5(t, matchingranks=4)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_no_ties_returns6(self):
    # Stud7 deal: seat 5 has lowest card, 9
    tools.deal_stud5(t, matchingranks=0)
    t.set_bringin()
    assert t.TOKENS['BI'] == 5


def test_bringin_stud7_2tied_returns1(self):
    # Stud7 deal: 2 Tied ranks
    tools.deal_stud5(t, matchingranks=2)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_3tied_returns1(self):
    # Stud7 deal: 3 Tied ranks
    tools.deal_stud5(t, matchingranks=3)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_4tied_returns1(self):
    # Stud7 deal: 4 Tied ranks
    tools.deal_stud5(t, matchingranks=4)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


