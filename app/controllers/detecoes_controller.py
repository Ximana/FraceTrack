from flask import Blueprint, render_template

detecoes_bp = Blueprint('detecoes', __name__, url_prefix='/detecoes')

@detecoes_bp.route('/listar')
def listar_detecoes():
    return render_template('detecoes/listar.html')

@detecoes_bp.route('/detalhes')
def detalhes_detecao():
    return render_template('detecoes/detalhes.html')
