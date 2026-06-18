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
        "valor_compra": float(formatar_dinheiro(valor_compra)),
        "percentual_desconto": float(formatar_dinheiro(percentual_desconto)),
        "valor_final": float(formatar_dinheiro(valor_final)),
        "cliente_vip": cliente_vip,
        "cashback_base": float(formatar_dinheiro(cashback_base)),
        "bonus_vip": float(formatar_dinheiro(bonus_vip)),
        "cashback_total": float(formatar_dinheiro(cashback_total))
    }