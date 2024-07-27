from flask import render_template
from . import notificacoes_bp

@notificacoes_bp.route('/listar')
def listar_notificacoes():
    return render_template('notificacoes/listar.html')

@notificacoes_bp.route('/detalhes')
def detalhes_notificacao():
    return render_template('notificacoes/detalhes.html')
