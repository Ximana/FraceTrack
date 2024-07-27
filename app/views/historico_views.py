from flask import render_template
from . import historico_bp

@historico_bp.route('/listar')
def listar_historico():
    return render_template('historico/listar.html')

@historico_bp.route('/detalhes')
def detalhes_historico():
    return render_template('historico/detalhes.html')
