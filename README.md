# Snake AI using Deep Q-Network (DQN)

This project implements an AI agent to play the classic Snake game using Deep Q-Network (DQN). The AI is trained to optimize the snake's movements and achieve higher scores.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Hinski2/snake.git
   cd snake
   ```
2. Run the AI agent:
   ```bash
   python agent.py
   ```

---- 

## Overview

**AI Model**: Built with PyTorch to implement a DQN.
- **Graphics**: Developed using Pygame.
- **Best Score**: 80
- **Average Score after Training**: 40
- **Model Architecture**: A neural network with one hidden layer of 512 units, using ReLU activation. The input layer has 11 features, and the output layer has 3 units representing the possible actions.
- **State Representation**: The game state consists of 11 values: 3 booleans indicating danger (left, straight, right), 4 booleans indicating the snake's current direction (up, down, left, right), and 4 booleans indicating the relative position of the food.
- **Training**: The model improves significantly after 80 to 100 games.

