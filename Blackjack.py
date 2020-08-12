from blackjacklib import (
    Card, Deck, Player, DealerAI, UI,
    STAND, HIT, BUST
)
from time import sleep

class Game:

    def __init__(self):
        self._UI = UI()
        self._wins = 0
        self._losses = 0
        self.new_game()

    def deal(self):
        self._deck = Deck()
        self._deck.shuffle()
        self._players = [
            Player([self._deck.card, self._deck.card]),
            Player([self._deck.card, self._deck.card])
        ]

    def new_game(self):
        self.deal()
        self._UI.start(self._wins, self._losses)
        option = input()
        if option == 'q': exit()
        if option == '': self.play()

    def play(self):
        self._UI.play(False, *self._players)
        option = None

        # Player Action
        while (
            option != '0' and
            min(self._players[0].total) <= 21
        ):
            option = input('press 0 to STAND, 1 to HIT: ')
            if option == '1':
                sleep(.25)
                self._players[0].add(self._deck.card)
                self._UI.play(False, *self._players)

        sleep(.25)
        self._UI.play(True, *self._players)

        # Mid Game Evaluation
        if min(self._players[0].total) > 21:
            print('Player BUST. Dealer Won :(')
            self._losses += 1
            print('\npress ENTER to return home')
            if input() == '': self.new_game()

        # Dealer Action
        while(
            DealerAI(self._players[1].total) != STAND and
            DealerAI(self._players[1].total) != BUST
        ):
            sleep(.25)
            self._players[1].add(self._deck.card)
            self._UI.play(True, *self._players)

        # Final Evaluation
        self.Evaluate()
        print('\npress ENTER to return home')
        if input() == '': self.new_game()

    def Evaluate(self):
        player_total = self._players[0].total
        dealer_total = self._players[1].total

        player_bust = min(player_total) > 21
        dealer_bust = min(dealer_total) > 21

        # Check dealer BUST 
        if dealer_bust and not player_bust:
            print('Dealer BUST. Player won!')
            self._wins += 1
            return 0

        player_value = (
            max(player_total) if max(player_total) <= 21
            else min(player_total)
        )
        dealer_value = (
            max(dealer_total) if max(dealer_total) <= 21
            else min(dealer_total)
        )

        # Evaluate Scores
        if player_value > dealer_value:
            print('Player won!')
            self._wins += 1
            return 0
        elif dealer_value > player_value:
            print('Dealer won :(')
            self._losses += 1
            return 1
        else:
            print('Draw.')
            return 2

game = Game()
