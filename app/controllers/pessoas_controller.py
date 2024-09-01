from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.pessoa_desaparecida import PessoaDesaparecida
import os
from werkzeug.utils import secure_filename
import uuid
from flask_paginate import Pagination, get_page_parameter
from app.models.reconhecimento_facial import ReconhecimentoFacial

from app.decorador import login_obrigatorio # decorador para secao obrigatoria

pessoas_bp = Blueprint('pessoas', __name__, url_prefix='/pessoas')

UPLOAD_FOLDER = 'app/static/img/pessoasDesaparecidas'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pessoas_bp.route('/listar')
@login_obrigatorio
def listar_pessoas():
    # Obtendo o número da página atual (padrão é 1)
    page = request.args.get('page', 1, type=int)
    
    # Consultar as pessoas e paginar resultados (10 pessoas por página)
    pessoas = PessoaDesaparecida.query.paginate(page=page, per_page=10)
    
    return render_template('pessoas/listar.html', pessoas=pessoas)

@pessoas_bp.route('/adicionar', methods=['GET', 'POST'])
@login_obrigatorio
def adicionar_pessoa():
    if request.method == 'POST':
        nome = request.form['nome']
        numero_bi = request.form['numeroBI']
        data_nascimento = request.form['dataNascimento']
        nome_pai = request.form['nomePai']
        nome_mae = request.form['nomeMae']
        data_desaparecimento = request.form['dataDesaparecimento']
        descricao = request.form['descricao']

        # Processar o upload da imagem
        file = request.files['fileImg']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        else:
            unique_filename = 'person_icon.png'  # Imagem padrão caso nenhuma imagem seja enviada

        nova_pessoa = PessoaDesaparecida(
            nome=nome,
            numero_bi=numero_bi,
            data_nascimento=data_nascimento,
            nome_pai=nome_pai,
            nome_mae=nome_mae,
            data_desaparecimento=data_desaparecimento,
            descricao=descricao,
            imagem=unique_filename
        )

        try:
            db.session.add(nova_pessoa)
            db.session.commit()

            flash('Pessoa desaparecida adicionada com sucesso!', 'success')
            return redirect(url_for('pessoas.listar_pessoas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar pessoa desaparecida: {str(e)}', 'danger')

    return redirect(url_for('pessoas.listar_pessoas'))

@pessoas_bp.route('/detalhes/<int:id>')
@login_obrigatorio
def detalhes_pessoa(id):
    pessoa = PessoaDesaparecida.query.get_or_404(id)
    return render_template('pessoas/detalhes.html', pessoa=pessoa)

@pessoas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_obrigatorio
def editar_pessoa(id):
    pessoa = PessoaDesaparecida.query.get_or_404(id)

    if request.method == 'POST':
        pessoa.nome = request.form.get('nome')
        pessoa.numero_bi = request.form.get('numeroBI')
        pessoa.data_nascimento = request.form.get('dataNascimento')
        pessoa.data_desaparecimento = request.form.get('dataDesaparecimento')
        pessoa.nome_pai = request.form.get('nomePai')
        pessoa.nome_mae = request.form.get('nomeMae')
        pessoa.descricao = request.form.get('descricao')

        # Processar o upload da imagem
        if 'fileImg' in request.files:
            file = request.files['fileImg']
            if file and allowed_file(file.filename):
                # Gerar nome único para o arquivo
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{ext}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                pessoa.imagem = unique_filename
            else:
                pessoa.imagem = 'person_icon.png'  # Imagem padrão caso nenhuma imagem seja enviada

        try:
            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar pessoa: {e}', 'danger')
        
        return redirect(url_for('pessoas.detalhes_pessoa', id=id))

    return render_template('pessoas/editar.html', pessoa=pessoa)

@pessoas_bp.route('/remover/<int:id>', methods=['POST'])
@login_obrigatorio
def remover_pessoa(id):
    pessoa = PessoaDesaparecida.query.get_or_404(id)
    
    try:
        # Remover a imagem do diretório, se não for a imagem padrão
        if pessoa.imagem != 'person_icon.png':
            image_path = os.path.join(UPLOAD_FOLDER, pessoa.imagem)
            if os.path.exists(image_path):
                os.remove(image_path)

        # Remover a pessoa do banco de dados
        db.session.delete(pessoa)
        db.session.commit()

        flash('Pessoa removida com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover pessoa: {str(e)}', 'danger')

    return redirect(url_for('pessoas.listar_pessoas'))
