from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# Onde os arquivos serão salvos
LINKS_FILE = "links.csv"

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para salvar o link
@app.route("/save-link", methods=["POST"])
def save_link():
    link = request.form.get("link")
    if link:
        # Verifica se o arquivo CSV já existe
        file_exists = os.path.isfile(LINKS_FILE)
        with open(LINKS_FILE, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(["Link"])  # Cabeçalho do CSV
            writer.writerow([link])
        return render_template("index.html", message="Link salvo com sucesso!")
    return render_template("index.html", error="Erro: Nenhum link foi enviado.")

@app.route("/view-links")
def view_links():
    links = []
    if os.path.isfile(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Pula o cabeçalho
            links = [row[0] for row in reader]
    return render_template("view_links.html", links=links)

if __name__ == '__main__':
    app.run(debug=True)