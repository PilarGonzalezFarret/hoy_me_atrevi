# init_db.py
from app import db, Categoria, app

# Lista de categorías iniciales
categorias_iniciales = ["Estudio", "Trabajo", "Hobbies", "Salud", "Relaciones"]

with app.app_context():
    for nombre in categorias_iniciales:
        # Evita duplicados
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))
    
    db.session.commit()
    print("✅ Categorías creadas:", ", ".join(categorias_iniciales))