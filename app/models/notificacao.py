from app import db

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    deteccao_id = db.Column(db.Integer, db.ForeignKey('deteccoes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    enviado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp())
