#!/usr/bin/env python3
import pickle
import combos


def write_handcombos():
    print('Enumerating unique 5-card hands by value')
    unique_hands = combos.get_unique_5cardhands()

    with open('handcombos.dat', 'wb') as db:
        pickle.dump(unique_hands, db)
