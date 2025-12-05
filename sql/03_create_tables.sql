USE wallet_homolog;

CREATE TABLE IF NOT EXISTS CARTEIRA (
    endereco_carteira VARCHAR(255) PRIMARY KEY,
    hash_chave_privada VARCHAR(255) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ATIVA'
);

CREATE TABLE IF NOT EXISTS MOEDA (
    id_moeda SMALLINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS SALDO_CARTEIRA (
    endereco_carteira VARCHAR(255),
    id_moeda SMALLINT,
    saldo DECIMAL(19,2) DEFAULT 0,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (endereco_carteira, id_moeda),
    FOREIGN KEY (endereco_carteira) REFERENCES CARTEIRA(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES MOEDA(id_moeda)
);

CREATE TABLE IF NOT EXISTS DEPOSITO_SAQUE (
    id_movimento BIGINT PRIMARY KEY AUTO_INCREMENT,
    endereco_carteira VARCHAR(255),
    id_moeda SMALLINT,
    tipo VARCHAR(20) NOT NULL, 
    valor DECIMAL(19,2) NOT NULL,
    taxa_valor DECIMAL(19,2),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_carteira) REFERENCES CARTEIRA(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES MOEDA(id_moeda)
);

CREATE TABLE IF NOT EXISTS CONVERSAO (
    id_conversao BIGINT PRIMARY KEY AUTO_INCREMENT,
    endereco_carteira VARCHAR(255),
    id_moeda_origem SMALLINT,
    id_moeda_destino SMALLINT,
    valor_origem DECIMAL(19,2) NOT NULL,
    valor_destino DECIMAL(19,2) NOT NULL,
    taxa_percentual DECIMAL(10,4),
    taxa_valor DECIMAL(19,2),
    cotacao_utilizada DECIMAL(19,6),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_carteira) REFERENCES CARTEIRA(endereco_carteira),
    FOREIGN KEY (id_moeda_origem) REFERENCES MOEDA(id_moeda),
    FOREIGN KEY (id_moeda_destino) REFERENCES MOEDA(id_moeda)
);

CREATE TABLE IF NOT EXISTS TRANSFERENCIA (
    id_transferencia BIGINT PRIMARY KEY AUTO_INCREMENT,
    endereco_origem VARCHAR(255),
    endereco_destino VARCHAR(255),
    id_moeda SMALLINT,
    valor DECIMAL(19,2) NOT NULL,
    taxa_valor DECIMAL(19,2),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_origem) REFERENCES CARTEIRA(endereco_carteira),
    FOREIGN KEY (endereco_destino) REFERENCES CARTEIRA(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES MOEDA(id_moeda)
);
