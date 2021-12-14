import json
import random

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


class Table:
    pass


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.hand = []

    def __str__(self):
        return f"I am {self.name}"

    def __int__(self):
        return len(self.hand)

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
        self.show_players()

    def process_exit(self):
        if self.user_input == "exit":
            self.running = False

    def show_players(self):
        for player in self.players:
            player.introduce()

    def loop(self):
        while self.running:
            self.user_input = input()
            self.process_exit()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
