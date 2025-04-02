from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# Onde os arquivos serão salvos
file = "links.csv"

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para salvar o link
@app.route('/save_link', methods=['POST'])
def save_link():
    link = request.form['link']
    if link:
        # Verifica se o arquivo já existe
        file_exists = os.path.isfile(file)
        
        # Abre o arquivo em modo append e escreve o link
        with open(file, mode='a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Link']) # Cabeçalho do CSV
            
            writer.writerow([link])
        
        return render_template("index.html", message="Link salvo com sucesso!")
    return render_template("index.html", message="Erro, nenhum  link foi enviado.")

if __name__ == '__main__':
    app.run(debug=True)