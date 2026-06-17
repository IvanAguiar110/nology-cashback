from decimal import Decimal, ROUND_HALF_UP


def formatar_dinheiro(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_cashback(valor_compra, cliente_vip=False):
    valor_compra = Decimal(str(valor_compra))

    cashback_base = valor_compra * Decimal("0.05")

    bonus_vip = Decimal("0")
    if cliente_vip:
        bonus_vip = cashback_base * Decimal("0.10")

    cashback_total = cashback_base + bonus_vip

    if valor_compra > Decimal("500"):
        cashback_total = cashback_total * Decimal("2")

    return {
        "valor_compra": float(formatar_dinheiro(valor_compra)),
        "cliente_vip": cliente_vip,
        "cashback_base": float(formatar_dinheiro(cashback_base)),
        "bonus_vip": float(formatar_dinheiro(bonus_vip)),
        "cashback_total": float(formatar_dinheiro(cashback_total))
    }