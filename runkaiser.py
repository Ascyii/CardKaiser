class Card:
    def __init__(self, value, suit):
        self.value, self.suit = value, suit

    def __str__(self):
        return f"{self.value} of {self.suit}"


class Game:
    def __init__(self):
        self.running = True
        self.user_input = str

    def process_exit(self):
        if self.user_input == "exit":
            self.running = False

    def loop(self):
        while self.running:
            self.user_input = input()
            self.process_exit()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
