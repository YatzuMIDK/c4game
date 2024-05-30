from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Tablero inicial vacío (6 filas x 7 columnas)
board = [["" for _ in range(7)] for _ in range(6)]
current_player = "R"  # Comienza el jugador rojo

def check_winner(board):
    # Comprobaciones para encontrar un ganador
    for row in range(6):
        for col in range(7):
            if board[row][col] != "":
                # Comprobación horizontal
                if col <= 3 and all(board[row][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Comprobación vertical
                if row <= 2 and all(board[row + i][col] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Comprobación diagonal descendente
                if row <= 2 and col <= 3 and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Comprobación diagonal ascendente
                if row >= 3 and col <= 3 and all(board[row - i][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]
    return None

@app.route('/move', methods=['POST'])
def make_move():
    global current_player
    data = request.json
    column = data.get("column")

    if column is None or not (0 <= column < 7):
        return jsonify({"error": "Columna inválida"}), 400

    # Encontrar la fila vacía más baja en la columna especificada
    for row in reversed(range(6)):
        if board[row][column] == "":
            board[row][column] = current_player
            winner = check_winner(board)
            if winner:
                response = jsonify({"board": board, "winner": winner})
                return response
            # Cambiar el turno al otro jugador
            current_player = "Y" if current_player == "R" else "R"
            return jsonify({"board": board, "current_player": current_player})

    return jsonify({"error": "Columna llena"}), 400

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({"board": board, "current_player": current_player})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
