import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button

class Card:
    FACES = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, face, suit):
        self._face = face
        self._suit = suit    

    @property
    def face(self):
        return self._face

    @property
    def suit(self):
        return self._suit

    @property
    def image_number(self):
        return f"English_pattern_{self.face.lower()}_of_{self.suit.lower()}.png"

    @property
    def cardNumber(self):
        if self.face == 'Ace':
            return 11  
        elif self.face in ['Jack', 'Queen', 'King']:
            return 10
        else:
            return int(self.face)
            
    def adjustAceValue(self, cardTotal):
        if cardTotal > 21:
            return 1
        return 11

    def __repr__(self):
        return f"Card(face='{self.face}', suit='{self.suit}')"

    def __str__(self):
        return f"{self.face} of {self.suit}"


class DeckOfCards:
    NUMBER_OF_CARDS = 52

    def __init__(self):
        self._current_card = 0
        self._deck = [
            Card(Card.FACES[count % 13], Card.SUITS[count // 13]) 
            for count in range(DeckOfCards.NUMBER_OF_CARDS)
        ]

    def shuffle(self):
        self._current_card = 0
        random.shuffle(self._deck)

    def deal_card(self):
        if self._current_card < DeckOfCards.NUMBER_OF_CARDS:
            card = self._deck[self._current_card]
            self._current_card += 1
            return card
        return None

def calculate_total(cards):
    total = sum(card.cardNumber for card in cards)
    num_aces = sum(1 for card in cards if card.face == 'Ace')

    while total > 21 and num_aces > 0:
        total -= 10
        num_aces -= 1

    return total

def display_hand(player_cards, dealer_cards):
    img_dir = os.path.join(os.getcwd(), "card_images")

    fig, axes = plt.subplots(2, 1, figsize=(2 * max(len(player_cards), len(dealer_cards)), 3))
    fig.suptitle("Blackjack Game", fontsize=16)

    # Display player's cards
    for i in range(len(player_cards)):
        img_path = os.path.join(img_dir, player_cards[i].image_number)
        img = mpimg.imread(img_path)
        axes[0].imshow(img, extent=[i, i + 1, 0, 1])

    axes[0].axis('off')
    axes[0].set_title("Player's Cards", fontsize=14, weight='bold')

    # Display dealer's cards
    for i in range(len(dealer_cards)):
        img_path = os.path.join(img_dir, dealer_cards[i].image_number)
        img = mpimg.imread(img_path)
        axes[1].imshow(img, extent=[i, i + 1, 0, 1])

    axes[1].axis('off')
    axes[1].set_title("Dealer's Cards", fontsize=14, weight='bold')

    axes[0].set_xlim(0, len(player_cards))
    axes[1].set_xlim(0, len(dealer_cards))

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)

    # Add buttons for hit and stand
    ax_hit = plt.axes([0.1, 0.01, 0.1, 0.05])
    ax_stand = plt.axes([0.3, 0.01, 0.1, 0.05])
    button_hit = Button(ax_hit, 'Hit')
    button_stand = Button(ax_stand, 'Stand')

    def on_hit(event):
        card = deck.deal_card()
        player_cards.append(card)
        display_hand(player_cards, [dealer_first_card])
        player_total = calculate_total(player_cards)
        print("\nPlayer's Total:", player_total)
        if player_total > 21:
            print("Player busts. Dealer wins!")
            plt.close(fig)
        elif player_total == 21:
            print("Blackjack! Player wins!")
            plt.close(fig)

    def on_stand(event):
        print("\nPlayer stands.")
        plt.close(fig)

    button_hit.on_clicked(on_hit)
    button_stand.on_clicked(on_stand)

    plt.show()

def main():
    global deck
    global dealer_first_card

    player_cards = []
    dealer_cards = []

    deck = DeckOfCards()
    deck.shuffle()

    print("Player's Cards:")
    for _ in range(2):
        card = deck.deal_card()
        print(card)
        player_cards.append(card)

    print("\nDealer's Card:")
    dealer_first_card = deck.deal_card()
    dealer_cards.append(dealer_first_card)
    print(dealer_first_card)
    dealer_cards.append(deck.deal_card())

    display_hand(player_cards, [dealer_first_card])

    # Wait for user interaction through buttons in the plot
    plt.show()

    # Continue dealer logic after player stands
    while calculate_total(dealer_cards) < 17:
        card = deck.deal_card()
        dealer_cards.append(card)

    player_total = calculate_total(player_cards)
    dealer_total = calculate_total(dealer_cards)
    print("\nPlayer's Total:", player_total)
    print("Dealer's Total:", dealer_total)

    display_hand(player_cards, dealer_cards)

    if dealer_total > 21 or player_total > dealer_total:
        print("Player wins!")
    elif player_total < dealer_total:
        print("Dealer wins!")
    else:
        print("It's a tie!")

main()
