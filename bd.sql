CREATE DATABASE reconhecimento_facial;

-- Usar o banco de dados
USE facetrack;

-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    numero_bi VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'funcionario', 'usuario') DEFAULT 'usuario',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Pessoas Desaparecidas
CREATE TABLE pessoas_desaparecidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    numero_bi VARCHAR(100),
    data_nascimento DATE NOT NULL,
    data_desaparecimento DATE NOT NULL,
    descricao TEXT,
    imagem VARCHAR(100) DEFAULT 'person_icon.png',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Detecções
CREATE TABLE deteccoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    localizacao VARCHAR(255),
    imagem_capturada VARCHAR(150),
    estado ENUM('Desaparecido', 'Emcontrado') DEFAULT 'Desaparecido',
    FOREIGN KEY (pessoa_id) REFERENCES pessoas_desaparecidas(id) ON DELETE CASCADE
);

-- Tabela de Notificações
CREATE TABLE notificacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deteccao_id INT,
    usuario_id INT,
    mensagem TEXT,
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deteccao_id) REFERENCES deteccoes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


