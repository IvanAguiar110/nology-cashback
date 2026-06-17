from decimal import Decimal, ROUND_HALF_UP


def formatar_dinheiro(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_cashback(valor_produto, percentual_desconto=0, cliente_vip=False):
    valor_produto = Decimal(str(valor_produto))
    percentual_desconto = Decimal(str(percentual_desconto))

    desconto = valor_produto * (percentual_desconto / Decimal("100"))
    valor_final = valor_produto - desconto

    cashback_base = valor_final * Decimal("0.05")

    bonus_vip = Decimal("0")
    if cliente_vip:
        bonus_vip = cashback_base * Decimal("0.10")

    cashback_total = cashback_base + bonus_vip

    if valor_final > Decimal("500"):
        cashback_total = cashback_total * Decimal("2")

    return {
        "valor_produto": formatar_dinheiro(valor_produto),
        "percentual_desconto": percentual_desconto,
        "valor_final": formatar_dinheiro(valor_final),
        "cashback_base": formatar_dinheiro(cashback_base),
        "bonus_vip": formatar_dinheiro(bonus_vip),
        "cashback_total": formatar_dinheiro(cashback_total)
    }


# Testes pedidos no desafio

caso_2 = calcular_cashback(600, 20, True)
caso_3 = calcular_cashback(600, 10, False)
caso_4 = calcular_cashback(600, 15, True)

print("Caso 2 - VIP, R$600, 20% off:")
print(f"Valor final: R$ {caso_2['valor_final']}")
print(f"Cashback base: R$ {caso_2['cashback_base']}")
print(f"Bônus VIP: R$ {caso_2['bonus_vip']}")
print(f"Cashback total: R$ {caso_2['cashback_total']}")

print("\nCaso 3 - Cliente comum, R$600, 10% off:")
print(f"Valor final: R$ {caso_3['valor_final']}")
print(f"Cashback base: R$ {caso_3['cashback_base']}")
print(f"Bônus VIP: R$ {caso_3['bonus_vip']}")
print(f"Cashback total: R$ {caso_3['cashback_total']}")

print("\nCaso 4 - VIP, R$600, 15% off:")
print(f"Valor final: R$ {caso_4['valor_final']}")
print(f"Cashback base: R$ {caso_4['cashback_base']}")
print(f"Bônus VIP: R$ {caso_4['bonus_vip']}")
print(f"Cashback total: R$ {caso_4['cashback_total']}")