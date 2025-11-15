# app.py (actualizado)
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from models import db, Entrada, Categoria

app = Flask(__name__)

# Configuración de la base de datos
# Para desarrollo local: usa SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoy_me_atrevi.db'

# Para producción (Render): usa PostgreSQL desde la variable de entorno
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

def format_date_for_display(date_str):
    """Convierte '2024-10-06' → 'Domingo 6 de octubre'"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
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
        return date_str

@app.route('/')
def index():
    # Obtener todas las entradas, ordenadas por fecha (más reciente primero)
    entries = Entrada.query.order_by(Entrada.fecha.desc()).all()
    
    formatted_entries = []
    for e in entries:
        formatted_entries.append({
            "display_date": format_date_for_display(e.fecha.isoformat()),
            "text": e.texto,
            "raw_date": e.fecha.isoformat(),
            "id": e.id,
            "categoria": e.categoria.nombre if e.categoria else "Sin categoría"
        })
    categorias = Categoria.query.all()
    return render_template('index.html', entries=formatted_entries, title="Hoy me atreví", categorias=categorias)

@app.route('/add', methods=['POST'])
def add_entry():
    date_str = request.form.get('date')
    text = request.form.get('text')
    categoria_id = request.form.get('categoria_id', type=int)  # opcional
    
    if date_str and text:
        try:
            fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
            nueva_entrada = Entrada(fecha=fecha, texto=text, categoria_id=categoria_id)
            db.session.add(nueva_entrada)
            db.session.commit()
        except Exception as e:
            print(f"Error al guardar: {e}")
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entrada = Entrada.query.get(entry_id)
    if not entrada:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        text = request.form.get('text')
        categoria_id = request.form.get('categoria_id', type=int)
        
        if date_str and text:
            try:
                entrada.fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
                entrada.texto = text
                entrada.categoria_id = categoria_id
                db.session.commit()
            except Exception as e:
                print(f"Error al editar: {e}")
        return redirect(url_for('index'))
    
    categorias = Categoria.query.all()
    return render_template('edit.html', entry=entrada, categorias=categorias)

@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    entrada = Entrada.query.get(entry_id)
    if entrada:
        db.session.delete(entrada)
        db.session.commit()
    return redirect(url_for('index'))

# NUEVO: Endpoint para stats
@app.route('/stats')
def stats():
    total = Entrada.query.count()
    hoy = datetime.now().date()
    hoy_count = Entrada.query.filter(Entrada.fecha == hoy).count()
    promedio = total / 7 if total > 0 else 0  # promedio semanal
    
    # Conteo por categoría
    categorias_stats = {}
    for cat in Categoria.query.all():
        count = Entrada.query.filter_by(categoria_id=cat.id).count()
        categorias_stats[cat.nombre] = count
    
    return render_template('stats.html', 
        total=total, 
        hoy=hoy_count, 
        promedio=promedio, 
        categorias_stats=categorias_stats)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)