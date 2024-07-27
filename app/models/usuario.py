from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero_bi = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('admin', 'funcionario', 'usuario', name='tipo_usuario'), default='usuario')
    criado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.senha = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.senha, password)