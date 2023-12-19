class HiOptIICardCounter:
  def __init__(self, total_decks=6):
    self.total_decks = total_decks
    self.reset_counts()

  def reset_counts(self):
    self.running_count = 0
    self.ace_count = 0
    self.cards_dealt = 0

  def card_value(self, card):
    if card in ['2', '3', '6', '7']:
      return 1
    elif card in ['4', '5']:
      return 2
    elif card in ['10', 'J', 'Q', 'K']:
      return -2
    else:  # 8, 9, Ace
      return 0

  def add_cards(self, cards):
    for card in cards:
      self.running_count += self.card_value(card)
      if card == 'A':
        self.ace_count += 1
      self.cards_dealt += 1

  def get_running_count(self):
    return self.running_count

  def get_true_count(self):
    decks_remaining = self._estimate_decks_remaining()
    return self.running_count / decks_remaining if decks_remaining > 0 else 0

  def _estimate_decks_remaining(self):
    total_cards = self.total_decks * 52
    cards_remaining = total_cards - self.cards_dealt
    return cards_remaining / 52

  def get_ace_count(self):
    return self.ace_count
