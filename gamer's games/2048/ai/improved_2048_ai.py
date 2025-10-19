import random
import time
import sys
import copy
import numpy as np

# 2048 game engine (improved version)
class Game2048:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.add_tile()
        self.add_tile()
        
    def add_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # In easy mode, we only get 2s
            self.grid[i][j] = 2
            
    def move(self, direction):
        # 0: up, 1: right, 2: down, 3: left
        moved = False
        original_grid = copy.deepcopy(self.grid)
        
        if direction == 0:  # Up
            for j in range(4):
                for i in range(1, 4):
                    if self.grid[i][j] != 0:
                        row = i
                        while row > 0 and self.grid[row-1][j] == 0:
                            self.grid[row-1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row -= 1
                            moved = True
                        if row > 0 and self.grid[row-1][j] == self.grid[row][j]:
                            self.grid[row-1][j] *= 2
                            self.score += self.grid[row-1][j]
                            self.grid[row][j] = 0
                            moved = True
                            
        elif direction == 1:  # Right
            for i in range(4):
                for j in range(2, -1, -1):
                    if self.grid[i][j] != 0:
                        col = j
                        while col < 3 and self.grid[i][col+1] == 0:
                            self.grid[i][col+1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col += 1
                            moved = True
                        if col < 3 and self.grid[i][col+1] == self.grid[i][col]:
                            self.grid[i][col+1] *= 2
                            self.score += self.grid[i][col+1]
                            self.grid[i][col] = 0
                            moved = True
                            
        elif direction == 2:  # Down
            for j in range(4):
                for i in range(2, -1, -1):
                    if self.grid[i][j] != 0:
                        row = i
                        while row < 3 and self.grid[row+1][j] == 0:
                            self.grid[row+1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row += 1
                            moved = True
                        if row < 3 and self.grid[row+1][j] == self.grid[row][j]:
                            self.grid[row+1][j] *= 2
                            self.score += self.grid[row+1][j]
                            self.grid[row][j] = 0
                            moved = True
                            
        elif direction == 3:  # Left
            for i in range(4):
                for j in range(1, 4):
                    if self.grid[i][j] != 0:
                        col = j
                        while col > 0 and self.grid[i][col-1] == 0:
                            self.grid[i][col-1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col -= 1
                            moved = True
                        if col > 0 and self.grid[i][col-1] == self.grid[i][col]:
                            self.grid[i][col-1] *= 2
                            self.score += self.grid[i][col-1]
                            self.grid[i][col] = 0
                            moved = True
        
        if moved:
            self.add_tile()
        else:
            # If no move happened, restore the original grid
            self.grid = original_grid
            
        return moved
    
    def is_game_over(self):
        # Check if there are any empty cells
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                
        # Check if there are any possible merges
        for i in range(4):
            for j in range(4):
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
                    
        return True
    
    def get_max_tile(self):
        return max(max(row) for row in self.grid)
    
    def display(self):
        print("Score:", self.score)
        for row in self.grid:
            print(" ".join(str(x).rjust(5) for x in row))
        print()

# Improved AI player using expectimax algorithm
class AutoPlayer:
    def __init__(self, game):
        self.game = game
        self.moves = 0
        
    def get_best_move(self):
        best_score = -float('inf')
        best_move = 0
        
        # Try each possible move
        for move in range(4):
            game_copy = copy.deepcopy(self.game)
            moved = game_copy.move(move)
            
            if not moved:
                continue
                
            # Evaluate the board after this move
            score = self.expectimax(game_copy, 2, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def expectimax(self, game_state, depth, is_max_turn):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate_board(game_state.grid)
            
        if is_max_turn:
            # Player's turn - try all moves
            best_score = -float('inf')
            
            for move in range(4):
                game_copy = copy.deepcopy(game_state)
                moved = game_copy.move(move)
                
                if not moved:
                    continue
                    
                score = self.expectimax(game_copy, depth - 1, False)
                best_score = max(best_score, score)
                
            return best_score
        else:
            # Chance node - consider all possible tile placements
            empty_cells = [(i, j) for i in range(4) for j in range(4) if game_state.grid[i][j] == 0]
            total_score = 0
            
            for i, j in empty_cells:
                # Try placing a 2 (only possibility in easy mode)
                game_copy = copy.deepcopy(game_state)
                game_copy.grid[i][j] = 2
                score = self.expectimax(game_copy, depth - 1, True)
                total_score += score
                
            return total_score / len(empty_cells) if empty_cells else 0
    
    def evaluate_board(self, grid):
        # Multiple evaluation heuristics
        
        # 1. Empty cells count (more is better)
        empty_cells = sum(1 for i in range(4) for j in range(4) if grid[i][j] == 0)
        
        # 2. Monotonicity - values should be increasing/decreasing in a pattern
        monotonicity = self.monotonicity_score(grid)
        
        # 3. Smoothness - adjacent tiles should have similar values
        smoothness = self.smoothness_score(grid)
        
        # 4. Maximum value position (prefer in corner)
        max_value = 0
        max_pos = (0, 0)
        for i in range(4):
            for j in range(4):
                if grid[i][j] > max_value:
                    max_value = grid[i][j]
                    max_pos = (i, j)
        
        corner_bonus = 0
        if max_pos in [(0, 0), (0, 3), (3, 0), (3, 3)]:
            corner_bonus = max_value * 10
        
        # Weighted combination of heuristics
        return (empty_cells * 20 + 
                monotonicity * 1.5 + 
                smoothness * 0.1 + 
                corner_bonus)
    
    def monotonicity_score(self, grid):
        # Check if rows and columns are monotonic
        score = 0
        
        # Check rows
        for i in range(4):
            for j in range(3):
                if grid[i][j] >= grid[i][j+1]:
                    score += 1
                if grid[i][3-j] >= grid[i][2-j]:
                    score += 1
        
        # Check columns
        for j in range(4):
            for i in range(3):
                if grid[i][j] >= grid[i+1][j]:
                    score += 1
                if grid[3-i][j] >= grid[2-i][j]:
                    score += 1
                    
        return score
    
    def smoothness_score(self, grid):
        # Measure how smooth the grid is (adjacent tiles with similar values)
        smoothness = 0
        
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    # Check right neighbor
                    if j < 3 and grid[i][j+1] != 0:
                        smoothness -= abs(grid[i][j] - grid[i][j+1])
                    # Check bottom neighbor
                    if i < 3 and grid[i+1][j] != 0:
                        smoothness -= abs(grid[i][j] - grid[i+1][j])
                        
        return smoothness
    
    def play(self, target=16384, delay=0.1, max_moves=5000):
        print(f"Starting auto-play to reach {target}...")
        print("Strategy: Expectimax algorithm with depth 2")
        
        while (not self.game.is_game_over() and 
               self.game.get_max_tile() < target and 
               self.moves < max_moves):
            
            move = self.get_best_move()
            self.game.move(move)
            self.moves += 1
            
            if self.moves % 100 == 0:
                print(f"Moves: {self.moves}, Score: {self.game.score}, Max Tile: {self.game.get_max_tile()}")
                self.game.display()
                
            time.sleep(delay)
            
        print("\n" + "="*50)
        print("Game Over!")
        print(f"Total moves: {self.moves}")
        print(f"Final score: {self.game.score}")
        print(f"Max tile: {self.game.get_max_tile()}")
        self.game.display()
        
        if self.game.get_max_tile() >= target:
            print("🎉 Successfully reached the target!")
        else:
            print("❌ Failed to reach the target.")
            
        return self.game.get_max_tile() >= target

# Simple strategy for comparison
class SimpleCornerPlayer:
    def __init__(self, game):
        self.game = game
        self.moves = 0
        self.last_move = None
        
    def get_move(self):
        # Simple strategy: prefer right and down moves, but avoid getting stuck
        # in a loop by occasionally making different moves
        
        # If we just moved right, try down
        if self.last_move == 1:
            return 2
        
        # If we just moved down, try right
        if self.last_move == 2:
            return 1
            
        # Default to right move
        return 1
    
    def play(self, target=16384, delay=0.1, max_moves=5000):
        print(f"Starting simple corner strategy to reach {target}...")
        
        while (not self.game.is_game_over() and 
               self.game.get_max_tile() < target and 
               self.moves < max_moves):
            
            move = self.get_move()
            moved = self.game.move(move)
            
            if moved:
                self.last_move = move
                self.moves += 1
            
            if self.moves % 100 == 0:
                print(f"Moves: {self.moves}, Score: {self.game.score}, Max Tile: {self.game.get_max_tile()}")
                self.game.display()
                
            time.sleep(delay)
            
        print("\n" + "="*50)
        print("Game Over!")
        print(f"Total moves: {self.moves}")
        print(f"Final score: {self.game.score}")
        print(f"Max tile: {self.game.get_max_tile()}")
        self.game.display()
        
        if self.game.get_max_tile() >= target:
            print("🎉 Successfully reached the target!")
        else:
            print("❌ Failed to reach the target.")
            
        return self.game.get_max_tile() >= target

# Run multiple games to test success rate
def test_strategy(strategy_class, num_games=10, target=16384):
    successes = 0
    max_tiles = []
    
    for i in range(num_games):
        print(f"\n=== Game {i+1}/{num_games} ===")
        game = Game2048()
        
        if strategy_class == AutoPlayer:
            player = AutoPlayer(game)
            success = player.play(target=target, delay=0, max_moves=10000)
        else:
            player = SimpleCornerPlayer(game)
            success = player.play(target=target, delay=0, max_moves=10000)
            
        if success:
            successes += 1
        max_tiles.append(game.get_max_tile())
        
        print(f"Current success rate: {successes}/{i+1} ({successes/(i+1)*100:.1f}%)")
        print(f"Max tiles achieved: {max_tiles}")
    
    print(f"\n=== Final Results ===")
    print(f"Success rate: {successes}/{num_games} ({successes/num_games*100:.1f}%)")
    print(f"Average max tile: {sum(max_tiles)/len(max_tiles):.0f}")
    print(f"Best result: {max(max_tiles)}")

# Main execution
if __name__ == "__main__":
    # Test the simple strategy first
    print("Testing simple corner strategy...")
    test_strategy(SimpleCornerPlayer, num_games=5, target=16384)
    
    # Test the expectimax strategy
    print("\n\nTesting expectimax strategy...")
    test_strategy(AutoPlayer, num_games=5, target=16384)