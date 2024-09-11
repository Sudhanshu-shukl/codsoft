import math

def print_board(board):
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print()

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_tie(board):
    return all([cell != ' ' for row in board for cell in row])

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif is_tie(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = 'O'
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move[0]][move[1]] = ' '
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = 'X'
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move[0]][move[1]] = ' '
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for m in get_available_moves(board):
        board[m[0]][m[1]] = 'O'
        score = minimax(board, 0, False)
        board[m[0]][m[1]] = ' '
        if score > best_score:
            best_score = score
            move = m
    return move

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    
    while True:
        human_move = input("Enter your move (row and column): ").split()
        row, col = int(human_move[0]), int(human_move[1])
        if board[row][col] == ' ':
            board[row][col] = 'X'
        else:
            print("Invalid move! Try again.")
            continue

        print_board(board)

        if check_winner(board, 'X'):
            print("You win!")
            break

        if is_tie(board):
            print("It's a tie!")
            break

        ai_move = best_move(board)
        board[ai_move[0]][ai_move[1]] = 'O'
        print("AI plays:")
        print_board(board)

        if check_winner(board, 'O'):
            print("AI wins!")
            break

        if is_tie(board):
            print("It's a tie!")
            break

play_game()
