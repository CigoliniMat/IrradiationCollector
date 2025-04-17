from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def mostra_lista():
    oggetti = [
        {'nome': 'Mela', 'prezzo': 1.2},
        {'nome': 'Banana', 'prezzo': 0.8},
        {'nome': 'Arancia', 'prezzo': 1.0}
    ]
    return render_template('lista.html', oggetti=oggetti)

@app.route('/seleziona', methods=['POST'])
def seleziona_oggetti():
    selezionati = request.form.getlist('selezionati')
    return f"Hai selezionato: {', '.join(selezionati)}" if selezionati else "Non hai selezionato nulla."

if __name__ == '__main__':
    app.run(debug=True)

