from flask import Flask, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

#importar outos arquivos
from app.decorador import login_obrigatorio


db = SQLAlchemy()
migrate = Migrate()

# Importar os modelos
from app.models import usuario, pessoa_desaparecida, detecao, notificacao

# Importar os controladores
from .controllers.index_controller import index_bp
from .controllers.login_controller import login_bp
from app.controllers.pessoas_controller import pessoas_bp
from .controllers.detecoes_controller import detecoes_bp
from .controllers.historico_controller import historico_bp
from .controllers.notificacoes_controller import notificacoes_bp
from .controllers.usuarios_controller import usuarios_bp
from app.controllers.cameras_controller import cameras_bp, init_reconhecimento_facial

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(pessoas_bp)    
    app.register_blueprint(detecoes_bp)
    app.register_blueprint(historico_bp)
    app.register_blueprint(notificacoes_bp)    
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(cameras_bp)
    
    @app.context_processor
    def inject_notifications():
        user_id = session.get('user_id')
        if user_id:
            from app.models.notificacao import Notificacao  # Importar o modelo dentro da função
            # Limitar a 10 notificações mais recentes
            notificacoes = Notificacao.query.filter_by(usuario_id=user_id).order_by(Notificacao.enviado_em.desc()).limit(10).all()
            return dict(notificacoes=notificacoes)
        return dict(notificacoes=[])

    with app.app_context():
        init_reconhecimento_facial()

    return app
