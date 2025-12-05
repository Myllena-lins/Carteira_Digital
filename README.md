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
