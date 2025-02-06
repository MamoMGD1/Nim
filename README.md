# Nim AI Game - README

## Overview
This project implements an AI-powered version of the Nim game, where a human player competes against an AI that learns from experience. The AI uses reinforcement learning to improve its strategy over multiple training sessions and can store learned data for future use.

## Features
- **AI Learning**: The AI refines its moves through reinforcement learning by rewarding winning strategies and penalizing losing ones.
- **Training Mode**: The AI can train for a specified number of iterations to improve its performance.
- **Game Mode**: The trained AI competes against the human player using learned strategies.
- **Data Persistence**: Learned game records can be saved and loaded from a CSV file.
- **Visualization**: The game displays statistics on AI moves using Seaborn and Matplotlib.

## Requirements
Ensure you have the following installed:
- Python 3.x
- Matplotlib (`pip install matplotlib`)
- Seaborn (`pip install seaborn`)

## Installation
1. Clone the repository or download the files.
2. Navigate to the project directory.
3. Install dependencies


## How to Run
1. Run the python file "nim.py"
2. Specify how many training iterations the AI should perform.
3. Choose whether to import previous training data (import for the best performance).
4. Play against the AI once training is complete.
5. You might also want to update the csv file if you have trained your agent (DON'T DO IT IF YOU HAVEN'T IMPORTED THE DATA FROM THE CSV FILE).

## Gameplay Instructions
- The game board consists of four piles: `[1, 3, 5, 7]`.
- On each turn, a player selects a pile and removes a specified number of tiles.
- The player forced to remove the last tile loses.
- The AI will attempt to optimize its strategy based on past training.

## AI Training Mechanism
- **Exploration vs. Exploitation**: The AI mostly chooses the best-known move but occasionally explores new moves.
- **Scoring System**:
  - Winning moves receive a **+5 score boost**.
  - Losing moves receive a **-2 penalty**.
- **Data Export**: After training, the AI's learned strategies can be saved to `csv_files/nim_data.csv`.
- **Training Milestones**:
  - After 1,000+ Trainings: The model learns to prefer advantageous moves over obviously bad ones. It starts recognizing basic winning patterns.
  - After 5,000+ Trainings: The model develops a deeper understanding of all possible moves, identifying sequences that lead to wins or losses.
  - After 10,000+ Trainings: The model can accurately categorize moves into best, good, neutral, bad, and worst, optimizing its decision-making strategy effectively.

## Data Visualization
After training, the AI's top and bottom 10 moves (based on score) are displayed using bar plots.

## File Structure
```
├── nim.py        # Main game script
├── csv_files/       # Directory for training data
│   ├── nim_data.csv # Saved AI learning data
├── README.md        # Project documentation
```

## Future Improvements
- Implementing a more advanced reinforcement learning algorithm such as Q-learning.
- Adding a GUI for better user interaction.
- Allowing AI vs. AI matches for automated training.

## License
This project is open-source and free to use. Contributions are welcome!

