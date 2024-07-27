from flask import Blueprint

# Criação dos blueprints para as views
pessoas_bp = Blueprint('pessoas', __name__, url_prefix='/pessoas')
deteccoes_bp = Blueprint('deteccoes', __name__, url_prefix='/deteccoes')
notificacoes_bp = Blueprint('notificacoes', __name__, url_prefix='/notificacoes')
historico_bp = Blueprint('historico', __name__, url_prefix='/historico')
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

def init_app(app):
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(deteccoes_bp)
    app.register_blueprint(notificacoes_bp)
    app.register_blueprint(historico_bp)
    app.register_blueprint(usuarios_bp)
