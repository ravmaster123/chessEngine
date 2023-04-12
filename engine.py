import mychess
import numpy as np
board = mychess.ChessBoard()
board.setup_board()
state = board.getState()
moves = board.legal_moves()
q_values = {}



epsilon = 0.1  # Set the value of epsilon
if np.random.uniform(0, 1) < epsilon:
    # Select a random action
    legal_moves = board.legal_moves()
    action = np.random.choice(legal_moves)
else:
    # Select the action with the highest Q-value
    q_values_for_state = q_values.get(current_state, {})
    best_action = max(q_values_for_state, key=q_values_for_state.get)
    action = best_action

