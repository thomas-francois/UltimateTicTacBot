
# Ultimate TicTacBot

Welcome to Ultimate TicTacBot, a project that aims to create a powerful bot for a custom variant of Ultimate Tic Tac Toe. 

## The game

The game **Ultimate Tic Tac Toe** is an extended version of the classic Tic Tac Toe game where each cell contains a smaller Tic Tac Toe board. In this classic rendition, players aim to secure three smaller boards in a row to win.

However, in this project's variant, the objective shifts to accumulating the highest number of points.

Points are earned by achieving three symbols in a row on a board. Importantly, a single board can host multiple points, accommodating successful moves from both players.

<p align="center">
	<img src="https://github.com/thomas-francois/UltimateTicTacBot/assets/103375765/6f9ac1a2-b2ef-4128-b7e9-042e4a256ee2" width="60%" />	
</p>


## Features
This project focuses on creating an intelligent bot capable of playing this custom variant with strategic decision-making.
- **Custom Variant Support:** The project implements the game engine including an API for this custom game variant along with a standalone game display module.

- **Configurability:** The project provides options for configuring the bot's difficulty level, search depth, and other parameters, allowing users to tailor the experience to their preferences.
 
- **Artificial Intelligence:** Utilizing algorithms, the bot aims to make intelligent moves based on the current state of the game.

- **Tournament mode:** Employing threading capabilities, the engine can concurrently run multiple games, facilitating the comparison of different bots and assessing their strengths against one another. This feature enhances the project's versatility for comprehensive bot evaluations in a tournament setting.


## Optimization and Strategies

To enhance the bot's performance and decision-making capabilities, the project incorporates the following optimization techniques and strategies:

-   **~~Minimax~~, Negamax:** The bot employs the Minimax algorithm to minimize the potential loss and maximize the potential gain, ensuring optimal decision-making in a turn-based game. Negamax simplifies the implementation of the Minimax algorithm by removing redundancy in code, reducing the overhead and making the code faster overall.
    
-   **Alpha-Beta Pruning:** Enhancing the Minimax algorithm, the bot utilizes Alpha-Beta Pruning to reduce the number of nodes evaluated in the search tree, improving computational efficiency.

Optimizations tested but not deemed useful.
> -   **Move Ordering using Iterative Deepening:** To minimize the number of nodes searched, prioritizing the evaluation of the best nodes early on is crucial for achieving more  aggressive pruning quickly. Leveraging Iterative Deepening, the algorithm incorporates the best moves from the preceding search to initiate the subsequent, deeper search, optimizing the decision-making process.
>
> -   **Transposition Table:** The project incorporates a Transposition Table to store previously calculated positions, preventing redundant calculations and accelerating the decision-making process by reusing stored evaluations.

## Requirements

Ensure you have the following prerequisites installed before running the project:

- [Python 3](https://www.python.org/downloads/) or later
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (Included with Python standard library)

## Contributions

Contributions are welcome!
Whether you're interested in fixing bugs, adding features, or improving documentation, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
