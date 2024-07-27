from flask import Blueprint, render_template

historico_bp = Blueprint('historico', __name__, url_prefix='/historico')



@historico_bp.route('/listar')
def listar_historico():
    return render_template('historico/listar.html')

@historico_bp.route('/detalhes')
def detalhes_historico():
    return render_template('historico/detalhes.html')
