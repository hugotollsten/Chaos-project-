import tkinter as tk
from tkinter import messagebox
import chaoticrand

ROWS = 3
COLS = 4
CARDS_PER_PLAYER = ROWS * COLS
class SkyjoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chaotic SKYJO - Two Player")
        self.root.geometry("1100x680")
        self.root.minsize(950, 600)

        self.shuffle = chaoticrand.ChaoticShuffle()
        self.deck = []
        self.discard_pile = []
        self.players = []
        self.current_player = 0
        self.mode = "idle"
        self.drawn_card = None
        self.game_over = False

        self.build_interface()
        self.new_game()

    def create_deck(self):
        deck = []

        # Simplified SKYJO-style distribution
        for value in range(-2, 13):
            deck.extend([value] * 8)

        self.shuffle.shuffle(deck)
        return deck

    def create_player(self):
        cards = []

        for _ in range(CARDS_PER_PLAYER):
            cards.append({
                "value": self.deck.pop(),
                "visible": False,
                "removed": False
            })

        positions = list(range(CARDS_PER_PLAYER))
        self.shuffle.shuffle(positions)

        for index in positions[:2]:
            cards[index]["visible"] = True

        return cards

    def new_game(self):
        self.shuffle = chaoticrand.ChaoticShuffle()

        self.deck = self.create_deck()
        self.players = [
            self.create_player(),
            self.create_player()
        ]

        self.discard_pile = [self.deck.pop()]
        self.current_player = 0
        self.mode = "idle"
        self.drawn_card = None
        self.game_over = False

        self.result_label.config(text="")
        self.event_label.config(text="")
        self.update_interface()

    # -------------------------------------------------
    # GUI
    # -------------------------------------------------

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="CHAOTIC SKYJO",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.root,
            text="Two-player game using a logistic-map chaotic random number generator",
            font=("Arial", 11)
        )
        subtitle.pack()

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=12)

        self.player_label = tk.Label(
            info_frame,
            text="Player 1's Turn",
            font=("Arial", 16, "bold")
        )
        self.player_label.grid(row=0, column=0, padx=20)

        self.deck_label = tk.Label(
            info_frame,
            text="Deck: 0",
            font=("Arial", 12)
        )
        self.deck_label.grid(row=0, column=1, padx=20)

        self.chaos_label = tk.Label(
            info_frame,
            text="Chaos x: 0.000000",
            font=("Courier", 11)
        )
        self.chaos_label.grid(row=0, column=2, padx=20)

        center_frame = tk.Frame(self.root)
        center_frame.pack(pady=5)

        discard_frame = tk.LabelFrame(
            center_frame,
            text="Discard Pile",
            padx=15,
            pady=10
        )
        discard_frame.grid(row=0, column=0, padx=20)

        self.discard_label = tk.Label(
            discard_frame,
            text="?",
            width=5,
            height=2,
            font=("Arial", 22, "bold"),
            relief="raised",
            borderwidth=3
        )
        self.discard_label.pack()

        actions_frame = tk.LabelFrame(
            center_frame,
            text="Actions",
            padx=15,
            pady=10
        )
        actions_frame.grid(row=0, column=1, padx=20)

        self.take_discard_button = tk.Button(
            actions_frame,
            text="Take Discard",
            width=18,
            command=self.take_discard
        )
        self.take_discard_button.pack(pady=4)

        self.draw_button = tk.Button(
            actions_frame,
            text="Draw From Deck",
            width=18,
            command=self.draw_from_deck
        )
        self.draw_button.pack(pady=4)

        self.drawn_frame = tk.LabelFrame(
            center_frame,
            text="Drawn Card",
            padx=15,
            pady=10
        )
        self.drawn_frame.grid(row=0, column=2, padx=20)

        self.drawn_label = tk.Label(
            self.drawn_frame,
            text="-",
            width=5,
            height=2,
            font=("Arial", 22, "bold"),
            relief="sunken",
            borderwidth=2
        )
        self.drawn_label.pack()

        drawn_buttons = tk.Frame(self.drawn_frame)
        drawn_buttons.pack(pady=(7, 0))

        self.replace_drawn_button = tk.Button(
            drawn_buttons,
            text="Replace Card",
            command=self.choose_replace_drawn
        )
        self.replace_drawn_button.pack(side="left", padx=3)

        self.discard_drawn_button = tk.Button(
            drawn_buttons,
            text="Discard + Reveal",
            command=self.choose_discard_drawn
        )
        self.discard_drawn_button.pack(side="left", padx=3)

        self.instruction_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "italic")
        )
        self.instruction_label.pack(pady=8)

        # Non-modal game message area. This avoids opening a messagebox
        # in the middle of a mouse/button event.
        self.event_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold")
        )
        self.event_label.pack(pady=(0, 4))

        # -------------------------------------------------
        # BOTH PLAYER CARD GRIDS
        # -------------------------------------------------

        boards_frame = tk.Frame(self.root)
        boards_frame.pack(pady=5)

        # Player 1 board
        self.player1_frame = tk.LabelFrame(
            boards_frame,
            text="Player 1",
            padx=10,
            pady=10,
            borderwidth=3
        )
        player1_frame = self.player1_frame
        player1_frame.grid(row=0, column=0, padx=15, sticky="n")

        # Player 2 board
        self.player2_frame = tk.LabelFrame(
            boards_frame,
            text="Player 2",
            padx=10,
            pady=10,
            borderwidth=3
        )
        player2_frame = self.player2_frame
        player2_frame.grid(row=0, column=1, padx=15, sticky="n")

        self.player_card_buttons = [[], []]

        for player_number, frame in enumerate(
            [player1_frame, player2_frame]
        ):
            for i in range(CARDS_PER_PLAYER):
                row = i // COLS
                col = i % COLS

                button = tk.Button(
                    frame,
                    text="?",
                    width=7,
                    height=3,
                    font=("Arial", 14, "bold"),
                    cursor="hand2",
                    takefocus=True,
                    command=lambda index=i, p=player_number:
                        self.card_clicked_for_player(p, index)
                )

                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4
                )

                self.player_card_buttons[player_number].append(button)

        score_frame = tk.Frame(self.root)
        score_frame.pack(pady=10)

        self.player1_status = tk.Label(
            score_frame,
            text="Player 1: 0/12 visible",
            font=("Arial", 11)
        )
        self.player1_status.grid(row=0, column=0, padx=25)

        self.player2_status = tk.Label(
            score_frame,
            text="Player 2: 0/12 visible",
            font=("Arial", 11)
        )
        self.player2_status.grid(row=0, column=1, padx=25)

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        tk.Button(
            bottom_frame,
            text="New Game",
            width=14,
            command=self.new_game
        ).pack(side="left", padx=5)

        tk.Button(
            bottom_frame,
            text="How RNG Works",
            width=14,
            command=self.show_rng_info
        ).pack(side="left", padx=5)

        tk.Button(
            bottom_frame,
            text="Quit",
            width=14,
            command=self.root.destroy
        ).pack(side="left", padx=5)

    # -------------------------------------------------
    # GAME ACTIONS
    # -------------------------------------------------

    def take_discard(self):
        if self.game_over or self.mode != "idle":
            return

        self.mode = "replace_discard"
        self.update_interface()

    def draw_from_deck(self):
        if self.game_over or self.mode != "idle":
            return

        self.recycle_deck_if_needed()

        if not self.deck:
            messagebox.showwarning("Deck Empty", "There are no cards left to draw.")
            return

        self.drawn_card = self.deck.pop()
        self.mode = "draw_choice"
        self.update_interface()

    def choose_replace_drawn(self):
        if self.mode != "draw_choice":
            return

        self.mode = "replace_drawn"
        self.update_interface()

    def choose_discard_drawn(self):
        if self.mode != "draw_choice":
            return

        self.discard_pile.append(self.drawn_card)
        self.drawn_card = None
        self.mode = "reveal"
        self.update_interface()

    def card_clicked_for_player(self, player_number, index):
        """
        Both players' boards are visible, but only the current
        player's cards can be used during that player's turn.
        """
        if player_number != self.current_player:
            return

        self.card_clicked(index)

    def card_clicked(self, index):
        if self.game_over:
            return

        player = self.players[self.current_player]
        card = player[index]

        if card.get("removed", False):
            return

        if self.mode == "replace_discard":
            incoming = self.discard_pile.pop()

            old_value = card["value"]

            player[index] = {
                "value": incoming,
                "visible": True,
                "removed": False
            }

            self.discard_pile.append(old_value)
            self.end_turn()

        elif self.mode == "replace_drawn":
            old_value = card["value"]

            player[index] = {
                "value": self.drawn_card,
                "visible": True,
                "removed": False
            }

            self.discard_pile.append(old_value)
            self.drawn_card = None
            self.end_turn()

        elif self.mode == "reveal":
            if card["visible"]:
                messagebox.showinfo(
                    "Already Visible",
                    "Choose a face-down card."
                )
                return

            card["visible"] = True
            self.end_turn()

    # -------------------------------------------------
    # TURN / SCORE LOGIC
    # -------------------------------------------------

    def end_turn(self):
        # Check for matching vertical columns before switching players.
        self.check_matching_columns(self.players[self.current_player])

        if self.all_visible(self.players[self.current_player]):
            self.finish_game()
            return

        # Reset turn state before redrawing the interface.
        self.mode = "idle"
        self.drawn_card = None
        self.current_player = 1 - self.current_player

        self.recycle_deck_if_needed()
        self.update_interface()

        # Let Tkinter process the redraw immediately after a completed turn.
        self.root.update_idletasks()

    def check_matching_columns(self, player):
        """
        Remove a vertical column if all 3 cards are visible
        and have the same value.

        Column indexes:
        0,4,8   1,5,9   2,6,10   3,7,11
        """
        removed_columns = []

        for col in range(COLS):
            indexes = [
                col,
                col + COLS,
                col + (2 * COLS)
            ]

            cards = [player[i] for i in indexes]

            if all(
                card["visible"] and not card.get("removed", False)
                for card in cards
            ):
                values = [card["value"] for card in cards]

                if values[0] == values[1] == values[2]:
                    for card in cards:
                        self.discard_pile.append(card["value"])
                        card["removed"] = True

                    removed_columns.append(col + 1)

        if removed_columns:
            columns_text = ", ".join(str(c) for c in removed_columns)

            # Do NOT open a modal messagebox here. This function is called
            # during a card click, and a popup can interrupt Tkinter's
            # button event sequence and make the UI feel stuck.
            self.event_label.config(
                text=f"Column(s) {columns_text} removed!"
            )

            # Clear the message later without blocking the UI.
            self.root.after(
                1800,
                lambda: self.event_label.config(text="")
            )

    def all_visible(self, player):
        return all(
            card.get("removed", False) or card["visible"]
            for card in player
        )

    def visible_count(self, player):
        return sum(
            1
            for card in player
            if card.get("removed", False) or card["visible"]
        )

    def score(self, player):
        return sum(
            card["value"]
            for card in player
            if not card.get("removed", False)
        )

    def recycle_deck_if_needed(self):
        if self.deck or len(self.discard_pile) <= 1:
            return

        top_card = self.discard_pile.pop()

        self.deck = self.discard_pile[:]
        self.discard_pile = [top_card]

        self.shuffle.shuffle(self.deck)

    def finish_game(self):
        self.game_over = True
        self.mode = "idle"
        self.drawn_card = None

        # Reveal every card that is still in play.
        # Removed cards stay marked as removed.
        for player in self.players:
            for card in player:
                if not card.get("removed", False):
                    card["visible"] = True

        score1 = self.score(self.players[0])
        score2 = self.score(self.players[1])

        if score1 < score2:
            result = "Player 1 wins!"
        elif score2 < score1:
            result = "Player 2 wins!"
        else:
            result = "It is a tie!"

        self.result_label.config(
            text=f"{result}   Player 1: {score1}   Player 2: {score2}"
        )

        # Redraw both boards so all remaining card values are visible.
        self.update_interface()
        self.root.update_idletasks()

        # Show the result only after the GUI has finished revealing the cards.
        messagebox.showinfo(
            "Game Over",
            f"{result}\n\n"
            f"Player 1 score: {score1}\n"
            f"Player 2 score: {score2}\n\n"
            "Lowest score wins."
        )

    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    def print_all_cards(self):
        """
        Print every card for both players to the terminal.

        Format:
        value(V) = visible
        value(H) = hidden
        value(R) = removed
        """

        print("\n" + "=" * 60)
        print("CURRENT GAME STATE")
        print("=" * 60)

        for player_number, player in enumerate(self.players, start=1):
            print(f"Player {player_number}:")

            for row in range(ROWS):
                row_cards = []

                for col in range(COLS):
                    index = row * COLS + col
                    card = player[index]

                    if card.get("removed", False):
                        status = "R"
                    elif card["visible"]:
                        status = "V"
                    else:
                        status = "H"

                    row_cards.append(
                        f"{card['value']:>2}({status})"
                    )

                print("  " + "  ".join(row_cards))

            print()

        print(f"Current player: Player {self.current_player + 1}")
        print(f"Mode: {self.mode}")
        print(f"Drawn card: {self.drawn_card}")
        print(
            "Top discard:",
            self.discard_pile[-1] if self.discard_pile else None
        )
        print(f"Cards left in deck: {len(self.deck)}")
        print("=" * 60)

    def update_interface(self):
        player = self.players[self.current_player]

        self.player_label.config(
            text=f"Player {self.current_player + 1}'s Turn"
            if not self.game_over
            else "Round Finished"
        )

        # Visually highlight the active player's board.
        if self.game_over:
            self.player1_frame.config(relief="groove")
            self.player2_frame.config(relief="groove")
        elif self.current_player == 0:
            self.player1_frame.config(relief="solid")
            self.player2_frame.config(relief="groove")
        else:
            self.player1_frame.config(relief="groove")
            self.player2_frame.config(relief="solid")

        self.deck_label.config(
            text=f"Deck: {len(self.deck)}"
        )

        self.chaos_label.config(
            text=f"Chaos x: {self.shuffle.x:.8f}"
        )

        if self.discard_pile:
            self.discard_label.config(
                text=str(self.discard_pile[-1])
            )

        if self.drawn_card is None:
            self.drawn_label.config(text="-")
        else:
            self.drawn_label.config(
                text=str(self.drawn_card)
            )

        instructions = {
            "idle": "Choose Take Discard or Draw From Deck.",
            "replace_discard":
                "Click one of your cards to replace it with the discard card.",
            "draw_choice":
                "Choose Replace Card or Discard + Reveal.",
            "replace_drawn":
                "Click one of your cards to replace it with the drawn card.",
            "reveal":
                "Click one face-down card to reveal it."
        }

        instruction = instructions.get(self.mode, "")
        if not self.game_over:
            instruction = (
                f"Player {self.current_player + 1}: " + instruction
            )

        self.instruction_label.config(text=instruction)

        # Update both player boards
        for player_number in range(2):
            board_player = self.players[player_number]

            for i, button in enumerate(
                self.player_card_buttons[player_number]
            ):
                card = board_player[i]

                if card.get("removed", False):
                    button.config(
                        text="X",
                        relief="flat",
                        state="disabled",
                        cursor="arrow"
                    )
                    continue
                else:
                    button.config(cursor="hand2")

                if self.game_over or card["visible"]:
                    button.config(
                        text=str(card["value"]),
                        relief="raised"
                    )
                else:
                    button.config(
                        text="?",
                        relief="ridge"
                    )

                # Other player's board is always view-only.
                if (
                    self.game_over
                    or player_number != self.current_player
                ):
                    button.config(state="disabled")

                elif self.mode in (
                    "replace_discard",
                    "replace_drawn"
                ):
                    button.config(state="normal")

                elif self.mode == "reveal":
                    if card["visible"]:
                        button.config(state="disabled")
                    else:
                        button.config(state="normal")

                else:
                    button.config(state="disabled")

        idle = (
            self.mode == "idle"
            and not self.game_over
        )

        self.take_discard_button.config(
            state="normal" if idle else "disabled"
        )

        self.draw_button.config(
            state="normal" if idle else "disabled"
        )

        draw_choice = (
            self.mode == "draw_choice"
            and not self.game_over
        )

        self.replace_drawn_button.config(
            state="normal" if draw_choice else "disabled"
        )

        self.discard_drawn_button.config(
            state="normal" if draw_choice else "disabled"
        )

        self.player1_status.config(
            text=(
                "Player 1: "
                f"{self.visible_count(self.players[0])}/12 visible"
            )
        )

        self.player2_status.config(
            text=(
                "Player 2: "
                f"{self.visible_count(self.players[1])}/12 visible"
            )
        )

        # Print the complete state every time the UI refreshes.
        #self.print_all_cards()

    def show_rng_info(self):
        messagebox.showinfo(
            "Chaotic Random Number Generator",
            "This game uses the logistic map:\n\n"
            "x(n+1) = k*x(n)*(1-x(n))\n\n"
        )