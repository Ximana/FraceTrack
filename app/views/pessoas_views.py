from flask import render_template
from . import pessoas_bp

@pessoas_bp.route('/listar')
def listar_pessoas():
    return render_template('pessoas/listar.html')

@pessoas_bp.route('/adicionar')
def adicionar_pessoa():
    return render_template('pessoas/adicionar.html')

@pessoas_bp.route('/editar')
def editar_pessoa():
    return render_template('pessoas/editar.html')

@pessoas_bp.route('/detalhes')
def detalhes_pessoa():
    return render_template('pessoas/detalhes.html')
