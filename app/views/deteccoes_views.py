from flask import render_template
from . import deteccoes_bp

@deteccoes_bp.route('/listar')
def listar_deteccoes():
    return render_template('deteccoes/listar.html')

@deteccoes_bp.route('/detalhes')
def detalhes_deteccao():
    return render_template('deteccoes/detalhes.html')
