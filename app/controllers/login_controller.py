from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import db
from app.models.usuario import Usuario

login_bp = Blueprint('login', __name__, url_prefix='/')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nomeusuario = request.form['nomeusuario']
        password = request.form['password']
        
        # Busca o usuário pelo nome
        usuario = Usuario.query.filter_by(email=nomeusuario).first()
        
        if usuario and check_password_hash(usuario.senha, password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nome
            session['user_type'] = usuario.tipo
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index.index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_type', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login.login'))
