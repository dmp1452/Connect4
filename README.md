Connect 4 Game with AI
Overview
This is a Connect 4 game implemented using Python and Pygame. The game features a player-vs-player mode and a player-vs-AI mode. The AI opponent utilizes the minimax algorithm with alpha-beta pruning to decide its moves.

Installation
Ensure you have Python installed (version 3.7 or higher recommended).

Install the required libraries using pip:

sh
Copy code
pip install pygame numpy
Download the game files and save them in the same directory.

Game Components
1. Board Class
Manages the game board, tile placement, and checking for winning conditions.
Key methods:
place(row, col, player): Places a player's tile on the board.
is_full(): Checks if the board is full.
get_choices(): Gets the list of valid moves.
final_state(): Evaluates the board state to determine if there's a winner or the board is full.
check_win(): Checks for winning conditions.

2. AI Class
Implements the AI using the minimax algorithm with alpha-beta pruning.
Key methods:
eval(main_board): Evaluates the board and decides the best move.
minimax(board, maximizing, alpha, beta, level): Recursively evaluates possible moves to determine the optimal one.

3. Game Class
Manages the game state, rendering, and user interactions.
Key methods:
lines(): Draws the grid lines.
buttons(): Draws the control buttons.
make_move(col): Makes a move for the current player.
draw_fig(row, col, player): Draws the player's tile on the board.

4. Helper Functions
message(message): Displays messages on the screen.
Running the Game
Run the main.py script to start the game:

sh
Copy code
python main.py
Use the mouse to interact with the game:

Click on the top bar to select game mode (PvP or AI).
Click on a column to place your tile.
The game will alternate turns between players or between the player and the AI. The AI will automatically calculate and make its move.

Controls
PvP Mode: Player vs Player mode.
AI Starts: AI vs Player mode where AI goes first.
AI You Start: AI vs Player mode where the player goes first.
Dependencies
pygame: Used for rendering the game window and handling user input.
numpy: Used for managing the game board as a matrix.
