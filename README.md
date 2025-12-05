# 💳 Carteira Digital — API de Gestão de Cripto e Moedas Fiat

Este repositório contém a implementação da API de Carteira Digital, que permite criação de carteiras, depósitos, saques, conversão de moedas e transferências entre carteiras.  
O projeto foi desenvolvido como parte de atividade acadêmica e segue rigorosamente os requisitos técnicos estabelecidos.

---

## 🧱 Funcionalidades Principais

✔️ Criar carteiras com chave pública e privada  
✔️ Hash da chave privada armazenada no banco  
✔️ Consultar saldos por moeda  
✔️ Realizar depósitos (sem taxa)  
✔️ Realizar saques com validação da chave privada  
✔️ Converter moedas utilizando API de cotação da Coinbase  
✔️ Transferir valores entre carteiras aplicando taxas  
✔️ Registrar histórico de todas as operações  

---

## 🗄️ Modelo de Dados

A API utiliza as seguintes entidades principais:

- **CARTEIRA**
- **MOEDA**
- **SALDO_CARTEIRA**
- **DEPOSITO_SAQUE**
- **CONVERSAO**
- **TRANSFERENCIA**

> O projeto suporta no mínimo 5 moedas:  
BTC, ETH, SOL, USD e BRL.

---

# 🚀 Guia de Instalação

Esta seção permite que qualquer usuário configure o ambiente, execute a API e realize testes completos das operações.

## ✔️ Pré-requisitos

Certifique-se de ter instalado:
- Python
- MySQL
- Git
- Cliente de requisições REST

---

## ⚙️ Instalação do Projeto

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Instalar dependências

```bash
pip install -r requirements.txt
```

## 🗄️ Configuração do Banco de Dados

Execute o script SQL abaixo no MySQL:

```bash
CREATE DATABASE wallet_homolog;

CREATE USER 'wallet_api_homolog'@'%' IDENTIFIED BY 'api123';

GRANT SELECT, INSERT, UPDATE, DELETE 
ON wallet_homolog.* 
TO 'wallet_api_homolog'@'%';

FLUSH PRIVILEGES;
```

## 📥 Popular tabela de moedas

```bash
INSERT INTO moeda (codigo, tipo) VALUES
('BTC', 'CRYPTO'),
('ETH', 'CRYPTO'),
('SOL', 'CRYPTO'),
('USD', 'FIAT'),
('BRL', 'FIAT');
```

## 🔒 Configurar variáveis de ambiente

Crie um arquivo .env baseado no exemplo:

```bash
DB_HOST=localhost
DB_PORT=3307
DB_USER=wallet_api_homolog
DB_PASSWORD=api123
DB_NAME=wallet_homolog

TAXA_SAQUE_PERCENTUAL=0.01
TAXA_CONVERSAO_PERCENTUAL=0.02
TAXA_TRANSFERENCIA_PERCENTUAL=0.01

PRIVATE_KEY_SIZE=32
PUBLIC_KEY_SIZE=16
```

## ▶️ Executanto o servidor

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```bash
http://localhost:8000
```

Se houver documentação interativa:

```bash
http://localhost:8000/docs
```
