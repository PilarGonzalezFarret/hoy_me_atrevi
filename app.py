import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'entries.json'

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return [
            {"date": "2024-10-04", "text": "Hoy me atreví a participar en un video"},
            {"date": "2024-10-05", "text": "Hoy me atreví a crear una app para la tarea"},
        ]

def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def format_date_for_display(date_str):
    """Convierte '2024-10-06' → 'Domingo 6 de octubre'"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        # Diccionario para días en español
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        dia_semana = dias[d.weekday()]
        dia = d.day
        mes = meses[d.month - 1]
        return f"{dia_semana} {dia} de {mes}"
    except:
        return date_str  # si falla, devuelve como está

entries = load_entries()

@app.route('/')
def index():
    # Formatear fechas para mostrar
    formatted_entries = []
    for e in entries:
        formatted_entries.append({
            "display_date": format_date_for_display(e["date"]),
            "text": e["text"],
            "raw_date": e["date"]
        })
    return render_template('index.html', entries=formatted_entries, title="Hoy me atreví")

@app.route('/add', methods=['POST'])
def add_entry():
    date = request.form.get('date')  # viene como "2024-10-06"
    text = request.form.get('text')
    if date and text:
        entries.insert(0, {"date": date, "text": text})
        save_entries(entries)
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_entry(index):
    if index < 0 or index >= len(entries):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        date = request.form.get('date')
        text = request.form.get('text')
        if date and text:
            entries[index] = {"date": date, "text": text}
            save_entries(entries)
        return redirect(url_for('index'))
    
    entry = entries[index]
    return render_template('edit.html', entry=entry, index=index)

@app.route('/delete/<int:index>')
def delete_entry(index):
    if 0 <= index < len(entries):
        entries.pop(index)
        save_entries(entries)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)