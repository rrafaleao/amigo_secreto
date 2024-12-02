from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

# Lista inicial de nomes
nomes_restantes = []
nomes_sorteados = []

@app.route("/", methods=["GET"])
def index():
    # Renderiza a página inicial
    return render_template("index.html")

@app.route("/sortear", methods=["GET"])
def sortear():
    global nomes_restantes, nomes_sorteados
    
    # Verifica se ainda há nomes suficientes para sortear
    if len(nomes_restantes) < 2:
        return jsonify({"error": "Não há nomes suficientes para continuar o sorteio!"}), 400

    # Sorteia dois nomes sem repetição
    sorteados = random.sample(nomes_restantes, 2)
    
    # Remove os nomes sorteados da lista restante
    for nome in sorteados:
        nomes_restantes.remove(nome)
        nomes_sorteados.append(nome)

    return jsonify({
        "nome1": sorteados[0],
        "nome2": sorteados[1],
        "restantes": nomes_restantes
    })

@app.route("/resetar", methods=["POST"])
def resetar():
    global nomes_restantes, nomes_sorteados
    nomes_restantes = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Isabela", "João"]
    nomes_sorteados = []
    return jsonify({"message": "Sorteio resetado com sucesso!", "restantes": nomes_restantes})

@app.route("/adicionar", methods=["POST"])
def adicionar():
    global nomes_restantes
    # Obtém o nome do corpo da requisição
    novo_nome = request.json.get("nome", "").strip()
    
    if not novo_nome:
        return jsonify({"error": "O nome não pode ser vazio!"}), 400

    if novo_nome in nomes_restantes or novo_nome in nomes_sorteados:
        return jsonify({"error": "Este nome já foi adicionado ou sorteado!"}), 400

    # Adiciona o novo nome à lista de nomes restantes
    nomes_restantes.append(novo_nome)
    return jsonify({"message": f"Nome '{novo_nome}' adicionado com sucesso!", "restantes": nomes_restantes})

if __name__ == "__main__":
    app.run(debug=True)
