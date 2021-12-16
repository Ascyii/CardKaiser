import json
import random
import sys

CARD_FILE = "cardproperties.json"
with open(CARD_FILE, "r") as file:
    CARDPROPERTIES = json.load(file)


class Card:
    def __init__(self, value, suit):
        self.value, self.suit = value, suit

    def __str__(self):
        return f"{self.rank_to_name()}{CARDPROPERTIES['symbols'][self.suit]}"

    def __eq__(self, other):
        return self.value == other.get_value

    def __lt__(self, other):
        return self.value < other.get_value()

    def __gt__(self, other):
        return self.value > other.get_value()

    def show(self):
        print(self)

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def rank_to_name(self) -> str:
        if self.value >= 11:
            return CARDPROPERTIES["values"][1][self.value - 11]
        else:
            return str(self.value)


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
        for _ in range(CARDPROPERTIES["duplications"]):
            for suit in CARDPROPERTIES["suits"]:
                for value in CARDPROPERTIES["values"][0]:
                    self.cards.append(Card(value, suit))
        for card in CARDPROPERTIES["extracards"]:
            self.cards.append(Card(card["value"], card["suit"]))
        for card in CARDPROPERTIES["removedcards"]:
            for i, card_from_cards in enumerate(self.cards):
                if card_from_cards.get_value() == card["value"] and card_from_cards.get_suit() == card["suit"]:
                    self.cards.pop(i)
        self.shuffle()

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
        self.score = 0
        self.current_tricks = []
        self.trick_value = 0

    def __str__(self):
        return f"Team{self.id} with a score of {self.score}"

    def determine_trick_score(self):
        for trick in self.current_tricks:
            self.trick_value += trick.evaluate_value()

    def clear_tricks(self):
        self.current_tricks.clear()
        self.trick_value = 0

    def reset(self):
        self.clear_tricks()
        self.score = 0


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

    def get_winner_of_trick(self, trump):
        winner = Player
        if trump != "N":
            leading_suit = self.current_cards[0][0].get_suit()
            print(leading_suit)
            for card_container in self.current_cards:
                card = card_container[0]
                player_of_card = card_container[1]

        return winner

    def pack_to_trick(self, deck):
        self.clear(deck)

    def play(self, player, card):
        if not self.check_full():
            self.current_cards.append([card, player])
        else:
            raise ValueError("cant play more than 4 cards at once")


class Player:
    name = ""

    def __init__(self, team: Team, name="Player"):
        self.team = team
        self.name = name
        self.hand = []

    def __str__(self):
        return f"I am {self.name} in {self.team} with {len(self.hand)} Cards"

    def __int__(self):
        return len(self.hand)

    def play(self, index, table):
        table.play(self.hand[index].pop(), self)

    def draw(self, deck: Deck, amount: int = 1):
        for _ in range(amount):
            self.hand.append(deck.draw())

    def show(self):
        print(f"{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"[{i + 1}] {card}")

    def introduce(self):
        print(self)

    def clear(self, deck):
        for card in self.hand:
            deck.return_card(card)
        self.hand.clear()

    def sort_hand(self):
        pass


class Game:
    def __init__(self):
        self.running = True
        self.players = []
        self.deck = Deck()
        self.table = Table()
        self.teams = [Team(1), Team(2)]

        self.trump = ""
        self.highest_bid = 6
        self.have_no = True
        self.bidding_team = Team

        for i in range(4):
            team = self.teams[i % 2]
            self.players.append(Player(team, f"Player{i + 1}"))

        self.current_dealer = self.players[random.randrange(4)]
        self.current_bidder = self.next_player(self.current_dealer)
        self.current_player = Player

    def process_commands(self, inp):
        if inp == "end":
            self.running = False
        elif inp == "exit":
            sys.exit(1)
        elif inp == "show":
            self.show_players()
            self.print_jobs()

    def show_players(self):
        for player in self.players:
            player.introduce()

    def print_jobs(self):
        print("-" * 100)
        print(f"The current dealer is: {self.current_dealer.name}")
        print(f"The current bidder is: {self.current_bidder.name}")
        print(f"The current player is: {self.current_player.name}")

    def deal_cards(self):
        while int(self.deck) > 0:
            for player in self.players:
                player.draw(self.deck)

    def next_player(self, player) -> Player:
        index = self.players.index(player)
        new_index = index + 1
        if new_index > len(self.players) - 1:
            new_index = 0
        return self.players[new_index]

    def clear_hands(self):
        for player in self.players:
            player.clear(self.deck)

    def reset(self):
        self.clear_hands()
        self.deck.shuffle()
        self.deal_cards()
        self.show_players()

    def ask_for_input(self):
        inp = str(input(">>> "))
        self.process_commands(inp)
        return inp

    def ask_for_bid(self):
        while True:
            inp = self.ask_for_input()
            try:
                bid_value = int(inp[0:2])
            except ValueError:
                print("! xx (no): xx stands for a number")
                continue
            have_no = False
            if len(inp) > 2:
                if inp[2:4] == "no":
                    have_no = True
            if bid_value == 0:
                print("You passed.")
                break
            elif bid_value == self.highest_bid and not self.have_no and have_no or bid_value > self.highest_bid:
                self.highest_bid = bid_value
                self.have_no = have_no
                self.current_player = self.current_bidder
                self.bidding_team = self.current_bidder.team
                print(f"The new highest bid is {self.highest_bid} with no {self.have_no}")
                break
            print("no valid bid - try again")

    def ask_for_card(self, hand) -> Card:
        while True:
            inp = int(self.ask_for_input())
            try:
                card = hand[inp-1]
                break
            except IndexError:
                print("enter valid index")
        return card

    def round(self):
        for _ in range(len(self.players)):
            print(f"{self.current_bidder.name} is bidding.")
            self.current_bidder.show()
            self.ask_for_bid()

            self.current_bidder = self.next_player(self.current_bidder)
        print(f"{self.current_player} starts with playing.")
        print(f"{self.bidding_team} won the bid with {self.highest_bid} and no {self.have_no}.")
        round_active = True
        while round_active:
            player = self.current_player
            player.show()
            player.play(self.ask_for_card(player.hand), self.table)
            self.current_player = self.next_player(self.current_player)

    def calculate_score(self):
        pass

    def loop(self):
        while self.running:
            self.reset()
            self.round()
            self.calculate_score()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
    sys.exit(1)
