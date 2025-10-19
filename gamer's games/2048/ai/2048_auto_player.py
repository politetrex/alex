import random
import time
import sys
import copy

# 2048 game engine (simplified version)
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
            print(" ".join(str(x).rjust(4) for x in row))
        print()

# AI player using a corner strategy
class AutoPlayer:
    def __init__(self, game):
        self.game = game
        self.moves = 0
        
    def get_best_move(self):
        # Strategy: Prefer moves that keep the highest tile in the corner
        # and maintain a snake-like pattern
        
        # Try each move and evaluate the board state
        best_score = -1
        best_move = 0
        
        for move in range(4):
            test_game = copy.deepcopy(self.game)
            moved = test_game.move(move)
            
            if not moved:
                continue
                
            # Evaluate the board state
            score = self.evaluate_board(test_game.grid)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def evaluate_board(self, grid):
        # Prefer boards with highest values in the top-left corner
        # and values decreasing in a snake pattern
        score = 0
        max_value = 0
        
        # Weight matrix favoring top-left corner
        weights = [
            [15, 14, 13, 12],
            [8, 9, 10, 11],
            [7, 6, 5, 4],
            [0, 1, 2, 3]
        ]
        
        for i in range(4):
            for j in range(4):
                score += grid[i][j] * weights[i][j]
                if grid[i][j] > max_value:
                    max_value = grid[i][j]
        
        # Bonus for having the max value in the corner
        if grid[0][0] == max_value:
            score += max_value * 10
            
        # Penalty for having empty cells away from the snake pattern
        empty_cells = sum(1 for i in range(4) for j in range(4) if grid[i][j] == 0)
        score += empty_cells * 20
        
        return score
    
    def play(self, target=16384, delay=0.1):
        print(f"Starting auto-play to reach {target}...")
        print("Strategy: Corner strategy (top-left) with snake pattern")
        
        while not self.game.is_game_over() and self.game.get_max_tile() < target:
            move = self.get_best_move()
            self.game.move(move)
            self.moves += 1
            
            if self.moves % 50 == 0:
                print(f"Moves: {self.moves}, Score: {self.game.score}, Max Tile: {self.game.get_max_tile()}")
                self.game.display()
                
            time.sleep(delay)
            
        print("\n" + "="*40)
        print("Game Over!")
        print(f"Total moves: {self.moves}")
        print(f"Final score: {self.game.score}")
        print(f"Max tile: {self.game.get_max_tile()}")
        self.game.display()
        
        if self.game.get_max_tile() >= target:
            print("🎉 Successfully reached the target!")
        else:
            print("❌ Failed to reach the target.")

# Main execution
if __name__ == "__main__":
    game = Game2048()
    player = AutoPlayer(game)
    
    # Play with a short delay between moves so you can see what's happening
    player.play(target=16384, delay=0.01)