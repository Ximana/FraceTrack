from flask import render_template
from . import usuarios_bp

@usuarios_bp.route('/listar')
def listar_usuarios():
    return render_template('usuarios/listar.html')

@usuarios_bp.route('/adicionar')
def adicionar_usuario():
    return render_template('usuarios/adicionar.html')

@usuarios_bp.route('/editar')
def editar_usuario():
    return render_template('usuarios/editar.html')

@usuarios_bp.route('/detalhes')
def detalhes_usuario():
    return render_template('usuarios/detalhes.html')
