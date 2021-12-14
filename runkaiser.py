import json
import random
import sys

card_file = "cardproperties.json"
with open(card_file, "r") as file:
    cardproperties = json.load(file)


class Card:
    def __init__(self, value, suit):
        self.value, self.suit = value, suit

    def __str__(self):
        return f"{self.value}{cardproperties['symbols'][self.suit]}"

    def show(self):
        print(self)

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def __str__(self):
        return f"the deck currently contains {len(self.cards)} cards"

    def __int__(self):
        return len(self.cards)

    def build(self):
        self.cards.clear()
        for _ in range(cardproperties["duplications"]):
            for suit in cardproperties["suits"]:
                for value in cardproperties["values"]:
                    self.cards.append(Card(value, suit))
        for card in cardproperties["extracards"]:
            self.cards.append(Card(card["value"], card["suit"]))
        for card in cardproperties["removedcards"]:
            for i, card_from_cards in enumerate(self.cards):
                if card_from_cards.get_value() == card["value"] and card_from_cards.get_suit() == card["suit"]:
                    self.cards.pop(i)

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for card in self.cards:
            card.show()

    def cut(self):
        i = random.randrange(len(self.cards))
        cut1 = self.cards[:i]
        cut2 = self.cards[i:]
        self.cards = cut2 + cut1

    def draw(self):
        return self.cards.pop()

    def return_card(self, card):
        self.cards.append(card)


class Trick:
    def __init__(self, cards):
        self.cards = cards
        self.value = 1
        self.evaluate_value()

    def evaluate_value(self):
        for i, card in enumerate(self.cards):
            if card.get_value() == 3 and card.get_suit() == "H":
                self.value -= 3
            if card.get_value() == 5 and card.get_suit() == "S":
                self.value += 5
        return self.value


class Team:
    def __init__(self, team_id):
        self.id = team_id
        self.tricks = []
        self.score = 0
        self.current_tricks = []
        self.trick_value = 0

    def determine_trick_score(self):
        for trick in self.current_tricks:
            self.trick_value += trick.evaluate_value()


class Table:
    def __int__(self):
        self.current_cards = []

    def clear(self, deck):
        for card in self.current_cards:
            deck.return_card(card)
        self.current_cards.clear()

    def check_full(self):
        if len(self.current_cards) >= 4:
            return True
        else:
            return False

    def play(self, card):
        if not self.check_full():
            self.current_cards.append(card)
        else:
            raise ValueError("cant play more than 4 cards at once")


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.hand = []

    def __str__(self):
        return f"I am {self.name}"

    def __int__(self):
        return len(self.hand)

    def play(self, index, table):
        table.play(self.hand[index].pop())

    def draw(self, deck: Deck, amount: int = 1):
        for _ in range(amount):
            self.hand.append(deck.draw())

    def show(self):
        print(f"{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"[{i+1}] {card}")

    def introduce(self):
        print(self)


class Game:
    def __init__(self):
        self.running = True
        self.user_input = str
        self.players = []
        self.deck = Deck()
        for i in range(4):
            self.players.append(Player(f"Player{i+1}"))

    def process_exit(self):
        if self.user_input == "exit":
            self.running = False

    def show_players(self):
        for player in self.players:
            player.introduce()

    def loop(self):
        while self.running:
            self.user_input = input(">>> ")
            self.process_exit()


def main():
    game = Game()
    game.deck.show()


if __name__ == "__main__":
    main()
    sys.exit(1)
