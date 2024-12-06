import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal(self):
        return [self.cards[i::4] for i in range(4)]  # プレイヤー4人に均等配分

def calculate_hcp(hand):
    points = {'J': 1, 'Q': 2, 'K': 3, 'A': 4}
    return sum(points.get(card.rank, 0) for card in hand)

def determine_declarer_and_dummy(hands):
    hcp_scores = [calculate_hcp(hand) for hand in hands]
    team_1_score = hcp_scores[0] + hcp_scores[2]
    team_2_score = hcp_scores[1] + hcp_scores[3]
    if team_1_score > team_2_score:
        declarer, dummy = (0, 2) if hcp_scores[0] > hcp_scores[2] else (2, 0)
    else:
        declarer, dummy = (1, 3) if hcp_scores[1] > hcp_scores[3] else (3, 1)
    return declarer, dummy, hcp_scores

def format_hand(hand, with_numbers=False):
    suits = {'♠': [], '♥': [], '♦': [], '♣': []}
    for idx, card in enumerate(hand):
        suits[card.suit].append((f"{idx + 1}", card.rank) if with_numbers else card.rank)

    formatted_hand = []
    for suit, cards in suits.items():
        if with_numbers:
            formatted_hand.append(f"{suit} " + " ".join(f"{num}:{rank}" for num, rank in cards))
        else:
            formatted_hand.append(f"{suit} {' '.join(cards)}")
    return '\n'.join(formatted_hand)

def display_seating(declarer, dummy):
    roles = ["Declarer", "Dummy"]
    seating = ["You (South)", "Player 2 (West)", "Player 3 (North)", "Player 4 (East)"]

    # Display roles
    for role, position in zip(roles, [declarer, dummy]):
        seating[position] += f" ({role})"

    print("\nSeating arrangement:")
    print("                      Player 3 (North)")
    print("               -----------------------")
    print("               |                   |")
    print(f"Player 2 (West) |                   | Player 4 (East)")
    print("               |                   |")
    print("               -----------------------")
    print(f"                      You (South)")

    print("\nRoles assigned:")
    for i, seat in enumerate(seating):
        print(f"{seat}")

def play_trick(hands, starting_player, dummy, declarer):
    trick = []
    leading_suit = None

    for i in range(4):
        player = (starting_player + i) % 4

        if player == dummy:  # ダミーのターン
            print("\nDummy's hand (visible to all):")
            print(format_hand(hands[dummy]))
            if player == (declarer + 2) % 4:
                print("Declarer chooses a card for the dummy.")
            card = hands[dummy].pop(0)  # ここでは最初のカードを選択（戦略強化可能）
        elif player == 0:  # ユーザーのターン
            print("\nYour hand:")
            print(format_hand(hands[0], with_numbers=True))
            while True:
                try:
                    choice = int(input("Choose a card to play (enter the number shown before the card): ")) - 1
                    if 0 <= choice < len(hands[0]):
                        card = hands[0].pop(choice)
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:  # AIのターン
            valid_cards = hands[player]
            if leading_suit:
                valid_cards = [card for card in hands[player] if card.suit == leading_suit] or hands[player]
            card = valid_cards[0]
            hands[player].remove(card)

        trick.append((player, card))

        if i == 0:
            leading_suit = card.suit

    # トリックの勝者を決定
    winning_card = max(
        (card for player, card in trick if card.suit == leading_suit),
        key=lambda c: Deck.ranks.index(c.rank)
    )
    winner = next(player for player, card in trick if card == winning_card)
    return winner, trick

def mini_bridge_game():
    deck = Deck()
    hands = deck.deal()
    player_is_human = True  # あなたがPlayer 1と仮定

    declarer, dummy, hcp_scores = determine_declarer_and_dummy(hands)

    display_seating(declarer, dummy)

    print("\nHands:")
    for i, hand in enumerate(hands):
        if i == 0 and player_is_human:
            print(f"Your hand:\n{format_hand(hand)}\nHCP: {hcp_scores[i]}")
        elif i == dummy:
            print(f"Player {i + 1} (Dummy's hand):\n{format_hand(hand)}\nHCP: {hcp_scores[i]}")
        else:
            print(f"Player {i + 1} hand: (hidden)")

    starting_player = (declarer + 1) % 4  # ディクレアラーの左手

    tricks_won = [0, 0, 0, 0]

    # プレイフェーズ
    for _ in range(13):  # 13トリックを行う
        winner, trick = play_trick(hands, starting_player, dummy, declarer)
        tricks_won[winner] += 1
        starting_player = winner
        print(f"Trick: {trick} | Winner: Player {winner + 1}")

    # スコアリング
    team_1_score = tricks_won[0] + tricks_won[2]
    team_2_score = tricks_won[1] + tricks_won[3]
    print(f"\nFinal Scores:")
    print(f"Team 1 (You and Player 3): {team_1_score}")
    print(f"Team 2 (Player 2 and Player 4): {team_2_score}")

# ゲームを開始
mini_bridge_game()
