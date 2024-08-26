from flask import Blueprint, render_template

from app.decorador import login_obrigatorio # decorador para secao obrigatoria


historico_bp = Blueprint('historico', __name__, url_prefix='/historico')



@historico_bp.route('/listar')
@login_obrigatorio
def listar_historico():
    return render_template('historico/listar.html')

@historico_bp.route('/detalhes')
@login_obrigatorio
def detalhes_historico():
    return render_template('historico/detalhes.html')
