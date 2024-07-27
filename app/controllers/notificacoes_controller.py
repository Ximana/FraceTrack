from flask import Blueprint, render_template, jsonify, session
from app import db
from app.models.notificacao import Notificacao

notificacoes_bp = Blueprint('notificacoes', __name__, url_prefix='/notificacoes')

@notificacoes_bp.route('/listar')
def listar_notificacoes():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login'))

    notificacoes = Notificacao.query.filter_by(usuario_id=user_id).order_by(Notificacao.enviado_em.desc()).all()
    return render_template('notificacoes/listar.html', notificacoes=notificacoes)

@notificacoes_bp.route('/detalhes')
def detalhes_notificacao():
    return render_template('notificacoes/detalhes.html')
