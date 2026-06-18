from decimal import Decimal, ROUND_HALF_UP


def formatar_dinheiro(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_cashback(valor_compra, percentual_desconto=0, cliente_vip=False):
    valor_compra = Decimal(str(valor_compra))
    percentual_desconto = Decimal(str(percentual_desconto))

    desconto = valor_compra * (percentual_desconto / Decimal("100"))
    valor_final = valor_compra - desconto

    cashback_base = valor_final * Decimal("0.05")

    bonus_vip = Decimal("0")
    if cliente_vip:
        bonus_vip = cashback_base * Decimal("0.10")

    cashback_total = cashback_base + bonus_vip

    if valor_final > Decimal("500"):
        cashback_total = cashback_total * Decimal("2")

    return {
        "valor_compra": formatar_dinheiro(valor_compra),
        "percentual_desconto": formatar_dinheiro(percentual_desconto),
        "valor_final": formatar_dinheiro(valor_final),
        "cliente_vip": cliente_vip,
        "cashback_base": formatar_dinheiro(cashback_base),
        "bonus_vip": formatar_dinheiro(bonus_vip),
        "cashback_total": formatar_dinheiro(cashback_total)
    }


def exibir_resultado(titulo, resultado):
    print(titulo)
    print(f"Valor original: R$ {resultado['valor_compra']}")
    print(f"Desconto aplicado: {resultado['percentual_desconto']}%")
    print(f"Valor final: R$ {resultado['valor_final']}")
    print(f"Cliente VIP: {resultado['cliente_vip']}")
    print(f"Cashback base: R$ {resultado['cashback_base']}")
    print(f"Bônus VIP: R$ {resultado['bonus_vip']}")
    print(f"Cashback total: R$ {resultado['cashback_total']}")
    print("-" * 40)


print("Questão 1 - Código Python de cálculo do cashback implementado.")
print("-" * 40)

caso_2 = calcular_cashback(
    valor_compra=600,
    percentual_desconto=20,
    cliente_vip=True
)

caso_3 = calcular_cashback(
    valor_compra=600,
    percentual_desconto=10,
    cliente_vip=False
)

caso_4 = calcular_cashback(
    valor_compra=600,
    percentual_desconto=15,
    cliente_vip=True
)

exibir_resultado("Questão 2 - VIP, R$600, 20% off:", caso_2)
exibir_resultado("Questão 3 - Cliente comum, R$600, 10% off:", caso_3)
exibir_resultado("Questão 4 - VIP, R$600, 15% off:", caso_4)