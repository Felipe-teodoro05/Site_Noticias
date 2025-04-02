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

@app.route("/clear-links", methods=["POST"])
def clear_links():
    if os.path.isfile(LINKS_FILE):
        # Limpa o conteúdo do arquivo CSV
        with open(LINKS_FILE, "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Link"])  # Reescreve apenas o cabeçalho
    return render_template("view_links.html", links=[], message="Todos os links foram excluídos com sucesso!")

@app.route("/delete-link/<int:link_index>", methods=["POST"])
def delete_link(link_index):
    links = []
    if os.path.isfile(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Pula o cabeçalho
            links = [row[0] for row in reader if row]

        # Remove o link pelo índice
        if 0 <= link_index < len(links):
            del links[link_index]

        # Reescreve o arquivo CSV com os links restantes
        with open(LINKS_FILE, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Link"])  # Reescreve o cabeçalho
            for link in links:
                writer.writerow([link])

    return render_template("view_links.html", links=links, message="O link foi excluído com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)