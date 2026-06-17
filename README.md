# Cashback Nology

Projeto desenvolvido para o desafio de Estagiário de Dev da Nology.

## Funcionalidades

- Cálculo de cashback para cliente comum e cliente VIP
- Cashback base de 5%
- Bônus VIP de 10% sobre o cashback base
- Cashback dobrado para compras acima de R$ 500
- API em Python com FastAPI
- Frontend estático em HTML, CSS e JavaScript
- Histórico de consultas por IP
- Persistência em banco de dados

## Regras de negócio

- O cashback base é de 5% sobre o valor final da compra.
- Clientes VIP recebem 10% de bônus sobre o cashback base.
- Compras acima de R$ 500 recebem o dobro de cashback.
- O histórico de consultas é salvo e exibido de acordo com o IP do usuário.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite local
- PostgreSQL para hospedagem
- HTML
- CSS
- JavaScript

## Como rodar localmente

Crie o ambiente virtual:

```bash
python3 -m venv venv 