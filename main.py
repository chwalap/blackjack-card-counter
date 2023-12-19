import tkinter as tk
from tkinter import ttk
from hiopt2 import HiOptIIBlackjackStrategy


def select_card(who, card):
    add_to_hand(who, card)


def advanced_blackjack_recommendation(player_hand, dealer_hand, true_count):
    converted_player_hand = [10 if card in ['J', 'Q', 'K'] else 11 if card == 'A' else int(card) for card in player_hand]
    print(converted_player_hand)
    player_total = sum(converted_player_hand)
    dealer_card = None
    if dealer_hand:
        dealer_card = 10 if dealer_hand[0] in ['J', 'Q', 'K'] else 11 if dealer_hand[0] == 'A' else int(dealer_hand[0])
    can_split = len(player_hand) == 2 and player_hand[0] == player_hand[1]

    # Splitting rules
    if can_split:
        pair = player_hand[0]
        if pair in [8, 11]:  # Always split Aces and 8s
            return 'Split'
        elif pair == 10:  # Never split 10s
            return 'Stand'
        elif pair == 9 and dealer_card and dealer_card not in [7, 10, 11]:  # Split 9s except against 7, 10, or Ace
            return 'Split'
        elif pair == 7 and dealer_card and dealer_card < 8:  # Split 7s against dealer's 2-7
            return 'Split'
        elif pair == 6 and dealer_card and dealer_card < 7:  # Split 6s against dealer's 2-6
            return 'Split'
        elif pair == 4 and dealer_card and dealer_card in [5, 6]:  # Split 4s only against dealer's 5 or 6
            return 'Split'
        elif pair == 3 and dealer_card and dealer_card < 8:  # Split 3s against dealer's 2-7
            return 'Split'
        elif pair == 2 and dealer_card and dealer_card < 8:  # Split 2s against dealer's 2-7
            return 'Split'

    # Doubling down rules
    if len(player_hand) == 2:  # Typically, doubling is allowed only on the first move
        if player_total == 11:  # Double on 11
            return 'Double'
        elif player_total == 10 and dealer_card and dealer_card < 10:  # Double on 10 against dealer's 9 or lower
            return 'Double'
        elif player_total == 9 and dealer_card and dealer_card in [3, 4, 5, 6]:  # Double on 9 against dealer's 3-6
            return 'Double'
        # More rules can be added here

    # Basic strategy adjusted by true count
    if player_total >= 17:
        return 'Stand'
    elif player_total >= 13 and dealer_card and dealer_card < 7:
        return 'Stand'
    elif player_total == 12 and dealer_card and dealer_card < 4:
        return 'Hit'
    elif player_total < 11:
        return 'Hit'

    # Adjustments based on true count
    if true_count > 1 and player_total >= 16 and dealer_card and dealer_card >= 7:
        return 'Stand'  # More conservative play at higher counts
    elif true_count < -1 and player_total <= 14 and dealer_card and dealer_card >= 7:
        return 'Hit'  # More aggressive play at lower counts

    return 'Hit'  # Default action


def add_to_hand(who, card):
    global player_hand, dealer_hand
    if who == 'player':
        player_hand = update_hand(player_hand, card)
        strategy.add_cards([str(card)])
    else:
        dealer_hand = update_hand(dealer_hand, card)

    true_count = strategy.counter.get_true_count()
    rec = advanced_blackjack_recommendation(player_hand, dealer_hand, true_count)
    recommendation.set(rec)
    update_bet_and_insurance()


def update_hand(hand, card):
  hand.append(card)
  return hand


def update_bet_and_insurance():
    bet_size.set(f"Bet Size: ${strategy.get_bet_size()}")
    insurance.set("Take Insurance" if strategy.should_take_insurance() else "Don't Take Insurance")


def next_game():
    global player_hand, dealer_hand
    player_hand, dealer_hand = [], []
    recommendation.set('')
    update_bet_and_insurance()


def create_card_buttons(root, who, start_row):
    button_size = 3
    ttk.Label(root, text=who).grid(column=0, row=start_row, sticky='w')
    card_values = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
    for i, card_value in enumerate(card_values, start=1):
        btn_idx = i - 1
        if who == 'dealer':
            btn_idx += len(card_values)

        btn.append(tk.Button(root, text=card_value, command=lambda card_value=card_value: select_card(who, card_value)))
        btn[btn_idx].grid(column=1 + (i-1) % 6, row=start_row + ((i-1) // 6), padx=5, pady=5)
        btn[btn_idx].config(height=button_size, width=button_size, relief='raised', borderwidth=2)


root = tk.Tk()
root.title("Blackjack Helper")

style = ttk.Style(root)
style.configure('Selected.TButton', background='lightgrey')

player_hand, dealer_hand = [], []
strategy = HiOptIIBlackjackStrategy()
recommendation = tk.StringVar()
bet_size = tk.StringVar()
insurance = tk.StringVar()

btn = []

create_card_buttons(root, 'player', 1)
create_card_buttons(root, 'dealer', 4)

# Recommendation, Bet Size, Insurance and New Game
ttk.Label(root, text="Recommendation:").grid(column=0, row=12, sticky='w')
ttk.Label(root, textvariable=recommendation).grid(column=1, row=12, columnspan=3)
ttk.Label(root, textvariable=bet_size).grid(column=0, row=13, columnspan=3)
ttk.Label(root, textvariable=insurance).grid(column=0, row=14, columnspan=3)
next_game_btn = ttk.Button(root, text="Next Game", command=next_game)
next_game_btn.grid(column=0, row=[15])

root.mainloop()
