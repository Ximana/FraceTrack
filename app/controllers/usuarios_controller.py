from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models.usuario import Usuario

from app.decorador import login_obrigatorio # decorador para secao obrigatoria


usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/listar', defaults={'page': 1})
@usuarios_bp.route('/listar/<int:page>')
@login_obrigatorio
def listar_usuarios(page):
    per_page = 10
    usuarios_paginados = Usuario.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('usuarios/listar.html', usuarios_paginados=usuarios_paginados)

@usuarios_bp.route('/adicionar', methods=['GET', 'POST'])
@login_obrigatorio
def adicionar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        numero_bi = request.form.get('numero_bi')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo_usuario = request.form.get('tipo_usuario')

        # Criptografar a senha
        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome=nome,
            numero_bi=numero_bi,
            email=email,
            senha=senha_hash,
            tipo=tipo_usuario
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário adicionado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar usuário: {e}', 'danger')
        
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('usuarios/adicionar.html')

@usuarios_bp.route('/editar')
@login_obrigatorio
def editar_usuario():
    return render_template('usuarios/editar.html')

@usuarios_bp.route('/detalhes')
@login_obrigatorio
def detalhes_usuario():
    return render_template('usuarios/detalhes.html')



@usuarios_bp.route('/excluir/<int:id>', methods=['POST'])
@login_obrigatorio
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir usuário: {e}', 'danger')
    
    return redirect(url_for('usuarios.listar_usuarios'))