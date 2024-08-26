from flask import Blueprint, render_template

from app.decorador import login_obrigatorio # decorador para secao obrigatoria


detecoes_bp = Blueprint('detecoes', __name__, url_prefix='/detecoes')

@detecoes_bp.route('/listar')
@login_obrigatorio
def listar_detecoes():
    return render_template('detecoes/listar.html')

@detecoes_bp.route('/detalhes')
@login_obrigatorio
def detalhes_detecao():
    return render_template('detecoes/detalhes.html')

def adicionar_detecao():
    return 
