from card_counter import HiOptIICardCounter

class HiOptIIBlackjackStrategy:
  def __init__(self, total_decks=6, base_bet=10):
    self.counter = HiOptIICardCounter(total_decks)
    self.base_bet = base_bet

  def reset_game(self):
    self.counter.reset_counts()

  def add_cards(self, cards):
    self.counter.add_cards(cards)

  def get_bet_size(self):
    true_count = self.counter.get_true_count()
    if true_count <= 1:
      return self.base_bet  # Minimum bet
    elif true_count <= 2:
      return self.base_bet * 2  # Increase bet moderately
    elif true_count <= 4:
      return self.base_bet * 4  # Increase bet more significantly
    else:
      return self.base_bet * 6  # Maximum bet

  def should_take_insurance(self):
    ace_count = self.counter.get_ace_count()
    decks_remaining = self.counter._estimate_decks_remaining()
    if decks_remaining > 0 and ace_count / decks_remaining > 1 / 3:
      return True
    return False
