from random import randint

class Card:

  suits = ('S', 'H', 'C', 'D')
  ranks = tuple(['A', *list(range(2, 11)), 'J', 'Q', 'K'])
  values = tuple([*list(range(1, 11)), *[10] * 3])

  def __init__(self, rank, suit):
    self._rank = rank
    self._suit = suit

  def get_suit(self): return self._suit
  def get_rank(self): return self._rank

  def get_value(self):
      return Card.values[Card.ranks.index(self._rank)]

  def __str__(self): return str(self._rank) + self._suit

  value = property(get_value)

class Deck:

  def __init__(self):
    self.cards = []
    for suit in Card.suits:
      for rank in Card.ranks:
        self.cards.append(Card(rank, suit))

  def deal_card(self): return self.cards.pop(0)
  def get_size(self): return len(self.cards)

  def shuffle(self):
      def gen(l):
        idxs = list(range(0, l))
        for i in range(l - 1, -1, -1):
            yield idxs.pop(randint(0, i))
      self.cards = [self.cards[i] for i in gen(len(self.cards))]

  size = property(get_size)
  card = property(deal_card)

class Player:
    def __init__(self, hand=[]):
        self._hand = hand

    def get_hand(self): return self._hand
    def set_hand(self, hand): self._hand = hand
    def add(self, card): self._hand.append(card)

    def get_total(self):
        return sum(list(map(lambda card : card.value, self._hand)))

    def __str__(self): return str(self._hand)

    hand = property(get_hand, set_hand)
    total = property(get_total)

class Account:

    def __init__(self, balance=0):
        self._balance = balance

    def get_balance(self): return self._balance

    def withdraw(self, amt):
        self._balance -= amt
        return self._balance

    def deposit(self, amt):
        self._balance += amt
        return self._balance

    balance = property(get_balance)
