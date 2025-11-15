# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entrada(db.Model):
    __tablename__ = 'entradas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    texto = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)

    categoria = db.relationship('Categoria', back_populates='entradas')

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "texto": self.texto,
            "categoria_id": self.categoria_id,
            "categoria_nombre": self.categoria.nombre if self.categoria else None
        }

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    entradas = db.relationship('Entrada', back_populates='categoria')

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}