from typing import Union

WINNING_POSITIONS: list[tuple[int, int, int]] = [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7),
]


class UpdateError(Exception):
    pass


class Player:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value

    def get_input(self) -> int:
        return int(input(f"{self.name}'s Turn: "))


class Position:
    def __init__(self, name: str):
        self.name: str = name
        self.value: Union[str, None] = None

    def __repr__(self):
        return f"Position(input_value={self.input_value})"

    def __str__(self):
        return self.value if self.value else " "

    def update(self, value: str) -> None:
        if self.value:
            raise UpdateError(
                f"Cannot update this position from {self.value} to {value}."
            )
        else:
            self.value = value


class Board:
    def __init__(self):
        self._position_map: dict[int, Position] = {
            1: Position("bottom left"),
            2: Position("bottom center"),
            3: Position("bottom right"),
            4: Position("middle left"),
            5: Position("middle center"),
            6: Position("middle right"),
            7: Position("top left"),
            8: Position("top center"),
            9: Position("top right"),
        }

    def update(self, input_value: int, value: str) -> None:
        self._position_map[input_value].update(value)

    @property
    def positions(self) -> list[Position]:
        return list(self._position_map.values())

    @property
    def has_open_positions(self) -> bool:
        return bool([p.value for p in self.positions if p.value is None])

    def display(self) -> None:
        print(
            f"""

 {self._position_map[7]} | {self._position_map[8]} | {self._position_map[9]}
-----------
 {self._position_map[4]} | {self._position_map[5]} | {self._position_map[6]}
-----------
 {self._position_map[1]} | {self._position_map[2]} | {self._position_map[3]}

"""
        )


class Game:
    def __init__(self):
        self.board: Board = Board()
        self.players: list[Player] = [Player("Player 1", "X"), Player("Player 2", "O")]
        self.active_game: bool = True

    @property
    def _is_won(self) -> bool:
        board_values = self.board._position_map
        status: bool

        for c in WINNING_POSITIONS:
            if board_values[c[0]].value == board_values[c[1]].value == board_values[
                c[2]
            ].value and board_values[c[0]].value in ["X", "O"]:
                status = True
                break
            else:
                status = False

        return status

    def _player_turn(self, player):
        try:
            self.board.update(player.get_input(), player.value)
        except ValueError:
            print("Please use the number pad to enter a number between 1 and 9.")
            self._player_turn(player)
        except UpdateError as e:
            print(e)
            self._player_turn(player)

    def play(self):
        print(
            "WELCOME TO TIC TAC TOE\n\n"
            "This game is played with the number pad. To select a position, enter the\n"
            "number that corresponds to the same location on the number pad\n"
            "(e.g. the top-left corner is 7)."
        )
        self.board.display()

        while self.active_game:
            for p in self.players:
                self._player_turn(p)
                self.board.display()

                if self._is_won:
                    print(f"{p.name} wins!")
                    self.active_game = False
                    break
                elif not self.board.has_open_positions:
                    print("Game Over! No open positions")
                    self.active_game = False
                    break

        print("Exiting game...")


if __name__ == "__main__":
    game = Game()
    game.play()
