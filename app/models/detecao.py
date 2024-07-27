from app import db

class Deteccao(db.Model):
    __tablename__ = 'deteccoes'
    
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas_desaparecidas.id'), nullable=False)
    data_hora = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    localizacao = db.Column(db.String(255))
    imagem_capturada = db.Column(db.String(150))
    estado = db.Column(db.Enum('Desaparecido', 'Encontrado', name='estado_deteccao'), default='Desaparecido')
    notificacoes = db.relationship('Notificacao', backref='deteccao', lazy=True)
