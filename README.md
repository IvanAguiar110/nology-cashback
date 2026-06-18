# Cashback Nology

Projeto desenvolvido para o desafio de Estagiário de Dev da Nology.

## Funcionalidades

- Cálculo de cashback para cliente comum e cliente VIP
- Aplicação de percentual de desconto sobre o valor da compra
- Cashback base de 5% sobre o valor final da compra
- Bônus VIP de 10% sobre o cashback base
- Cashback dobrado para compras acima de R$ 500
- API em Python com FastAPI
- Frontend estático em HTML, CSS e JavaScript
- Histórico de consultas por IP
- Persistência em banco de dados PostgreSQL em produção
- SQLite utilizado como fallback local para testes

## Regras de negócio

- Primeiro é aplicado o percentual de desconto sobre o valor original da compra.
- O cashback é calculado sobre o valor final da compra, após o desconto.
- O cashback base é de 5%.
- Clientes VIP recebem bônus de 10% sobre o cashback base.
- Compras acima de R$ 500 recebem o dobro de cashback.
- O histórico de consultas é salvo e exibido de acordo com o IP do usuário.

## Exemplo de cálculo

Cliente VIP compra um produto de R$ 600 com 15% de desconto.

Valor final da compra:

```text
600 - 15% = 510