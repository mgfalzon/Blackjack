from clilib import Display
import pokerlib

# Constants
STAND = 0
HIT = 2
BUST = 3

class Card(pokerlib.Card):
    def __init__(self, rank, suit):
        super().__init__(rank, suit)

    def get_value(self):
      value = pokerlib.Card.get_value(self)
      return (1, 11) if value == 1 else (value, value)

    value = property(get_value)

class Deck(pokerlib.Deck):

  def __init__(self):
    super().__init__()
    self.cards = []
    for suit in Card.suits:
      for rank in Card.ranks:
        self.cards.append(Card(rank, suit))

class Player(pokerlib.Player):
    def __init__(self, hand=[]):
        super().__init__(hand)

    def get_total(self):
        values = list(map(lambda card : card.value, self._hand))
        totalA = sum(list(map(lambda tup : tup[0], values)))
        totalB = sum(list(map(lambda tup : tup[1], values)))
        return (totalA, totalB)

    total = property(get_total)

def DealerAI(totals):
    # BUST
    if totals[0] > 21 and totals[1] > 21:
        return BUST
    # STAND
    for total in totals:
        if total >= 17 and total <= 21:
            return STAND
    # HIT
    return HIT

class UI(Display):
    def __init__(self):
        super().__init__()

    def start(self, w, l):
        self.render('''
Welcome to Blackjack!
---------------------

  Wins:    {}
  Losses:  {}


  (press ENTER to play, ESC to exit)
        ''', w, l)

    def play(self, show_dealer, *players):
        dealer_hand = players[1].hand
        if not show_dealer:
            dealer_hand = [
                players[1].hand[0],
                *[
                    '??' for i in range(len(players[1].hand) - 1)
                ]
            ]

        self.render('''
Cards:
{}
TOTAL: {}


Dealer:
{}
TOTAL: {}

''',
        Display.multiAppend(*list(map(
            lambda card : UI.card(str(card)), players[0].hand
        ))), UI.totalFormat(players[0].total),

        Display.multiAppend(*list(map(
            lambda card : UI.card(str(card)), dealer_hand
        ))),
        UI.totalFormat(players[1].total) if show_dealer else '??'
    )


    def card(val):
        l = r = val
        if len(val) == 2:
            l = val + ' '
            r = ' ' + val
        s = ''
        if 'S' in val: s = '♠'
        elif 'H' in val: s = '♥'
        elif 'C' in val: s = '♣'
        elif 'D' in val: s = '♦'
        else: s = ' '
        return '''
 -------------   
| {}         |  
|             |  
|             |  
|             |  
|      {}      |  
|             |  
|             |  
|             |  
|         {} |  
 -------------   '''.format(l, s, r)

    # ERROR: had many cards, BLACKJACK, said BUST
    def totalFormat(tup):
        # No Ace
        if tup[0] == tup[1]:
           return 'BUST' if tup[0] > 21 else tup[0]
        # Ace (no BUST)
        elif tup[0] <= 21 and tup[1] <= 21:
           return '{} or {}'.format(tup[0], tup[1])
        # BUST
        elif tup[0] >= 21 and tup[1] >= 21:
           return 'BUST'
        # Ace (BUST)
        return tup[0] if tup[0] <= 21 else tup[1]
