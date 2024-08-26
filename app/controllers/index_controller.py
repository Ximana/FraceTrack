
from flask import render_template, Blueprint

from app.decorador import login_obrigatorio # decorador para secao obrigatoria

index_bp = Blueprint('index', __name__, url_prefix='/')

@index_bp.route('/')
@login_obrigatorio
def index():
    return render_template('index.html')

@index_bp.route('/sobre')
def sobre():
    return render_template('sobre.html')


@index_bp.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')

