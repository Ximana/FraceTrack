from app import db

class PessoaDesaparecida(db.Model):
    __tablename__ = 'pessoas_desaparecidas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero_bi = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date, nullable=False)
    nome_pai = db.Column(db.String(100))
    nome_mae = db.Column(db.String(100))
    data_desaparecimento = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(100), default='person_icon.png')
    criado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deteccoes = db.relationship('Deteccao', backref='pessoa', lazy=True)

