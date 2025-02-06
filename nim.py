import random, math, csv, time
import matplotlib.pyplot as plt
import seaborn as sns

# Initial board state
game_board = [1, 3, 5, 7]
records = []
trains = int(input("How Many Times Should I Train? "))
training = False
my_turn = True
winner = ""

class Record:
    def __init__(self, board, pile_move, tile_move, score=0):
        self.board = board
        self.pile_move = pile_move
        self.tile_move = tile_move
        self.score = score or 0  # Start at 0 to allow both rewards & penalties

def ai_choice():
    valid_piles = [i for i in range(len(game_board)) if game_board[i] != 0]

    if len(records) > 0 and not training:
        best_move = None
        best_score = -math.inf

        for record in records:
            if record.board == ''.join(map(str, game_board)):
                if record.score > best_score:
                    best_score = record.score
                    best_move = (record.pile_move, record.tile_move)

        if best_move and random.random() > 0.1:  # 90% of the time, choose smartly
            print("Found A Smart Move")
            return best_move

    # Exploration: Choose a random move
    pile = random.choice(valid_piles)
    tile = random.randint(1, game_board[pile])
    return pile, tile

def check_winner():
    if game_board.count(1) == 1 and all(num in (0, 1) for num in game_board):
        return "Human" if my_turn else "AI"
    elif all(num == 0 for num in game_board):
        return "Nobody"
    else:
        return ""

def show_board():
    global my_turn, winner
    print("--------------------")
    for i in range(len(game_board)):
        print(f"Pile {i} => {game_board[i]}")

    if winner:
        print(f"'{winner}' Is The Winner")
    elif my_turn:
        pile = int(input("Pile Number: "))
        tile = int(input("Tiles To Remove: "))
        game_board[pile] -= tile
    else:
        pile, tile = ai_choice()
        print(f"AI removes {tile} tiles from pile {pile}")
        game_board[pile] -= tile

    winner = check_winner()
    my_turn = not my_turn

def train():
    global winner, records, my_turn, training
    training = True
    temp = []

    while not winner:
        pile, tile = ai_choice()
        if my_turn:  
            temp.append(Record(''.join(map(str, game_board)), pile, tile))
        game_board[pile] -= tile
        winner = check_winner()
        my_turn = not my_turn

    # If AI won, reward all moves in `temp`
    if winner == "Human":
        for temp_record in temp:
            for existing_record in records:
                if (existing_record.board == temp_record.board and
                    existing_record.pile_move == temp_record.pile_move and
                    existing_record.tile_move == temp_record.tile_move):

                    existing_record.score += 5  # Increase score for winning moves
                    break
            else:
                temp_record.score = 5  # New record starts with a reward
                records.append(temp_record)

    # If AI lost, penalize all moves in `temp`
    elif winner == "AI":
        for temp_record in temp:
            for existing_record in records:
                if (existing_record.board == temp_record.board and
                    existing_record.pile_move == temp_record.pile_move and
                    existing_record.tile_move == temp_record.tile_move):

                    existing_record.score -= 2  # Penalize bad moves
                    break
            else:
                temp_record.score = -2  # New bad record starts with penalty
                records.append(temp_record)

def plot_records(records):
    # Extract data for plotting
    boards = [record.board for record in records if record.board!="1357"]
    pile_moves = [record.pile_move for record in records if record.board!="1357"]
    tile_moves = [record.tile_move for record in records if record.board!="1357"]
    scores = [record.score for record in records if record.board!="1357"]

    # Combine data into a list of tuples for sorting
    data = list(zip(boards, pile_moves, tile_moves, scores))

    # Sort by score (descending for top 10, ascending for bottom 10)
    sorted_data = sorted(data, key=lambda x: x[3], reverse=True)
    top_10 = sorted_data[:10]
    bottom_10 = sorted_data[-10:]

    # Function to create a bar plot
    def create_bar_plot(data, title):
        labels = [f"{board}\nPile: {pile}, Tile: {tile}" for board, pile, tile, _ in data]
        values = [score for _, _, _, score in data]

        plt.figure(figsize=(6, 5))
        sns.barplot(x=labels, y=values, palette="viridis", hue=labels, legend=False)
        plt.title(title, fontsize=16)
        plt.ylabel("Score", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    # Plot top 10 highest scores
    create_bar_plot(top_10, "Top 10 Moves with Highest Scores")

    # Plot top 10 lowest scores
    create_bar_plot(bottom_10, "Top 10 Moves with Lowest Scores")
    plt.show()
def import_data():
    global records
    with open("csv_files/nim_data.csv","r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(Record(row["Board"], int(row["Pile"]), int(row["Tile"]), int(row["Score"])))
def main():
    global game_board, winner, training, my_turn
    if input("Can I use external data?(Y/N) ").capitalize()=="Y":
        import_data()
    print(f"{len(records)} Data Imported Successfully!")
    # Training Phase
    progress_bar = ['_' for _ in range(30)]
    for _ in range(trains):
        train()
        game_board = [1, 3, 5, 7]
        winner = ""
        my_turn = True
        progress_bar[math.floor(_/trains*30)] = "■"
        print(f"[{''.join(progress_bar)}] Training ({_+1:04})/({trains})", end="\r")
        time.sleep(0.001)
    if training:
        print("\033[K",end="\r")
        print("Training Done!✅")
    # Export data
    if training and input("Can I Use The Training Data Externally? ").capitalize() == "Y":
        with open("csv_files/nim_data.csv", "w", newline="") as file:
            writer = csv.DictWriter(file,fieldnames=["Board","Pile","Tile","Score"])
            writer.writeheader()
            writer.writerows([{"Board":r.board, "Pile": r.pile_move, "Tile":r.tile_move, "Score":r.score} for r in records])
    # Show data on the graphs
    training = False
    plot_records(records)

    # Game Phase
    for _ in range(int(input("How Many Games Would You Play? "))):
        game_board = [1,3,5,7]
        winner = ""
        my_turn = True
        while not winner:
            show_board()
        show_board()
        print("Game Over!🎯")

main()