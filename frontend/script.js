const API_URL = "http://127.0.0.1:8000";

const formCashback = document.getElementById("formCashback");
const tipoCliente = document.getElementById("tipoCliente");
const valorCompra = document.getElementById("valorCompra");
const resultado = document.getElementById("resultado");
const historico = document.getElementById("historico");

function formatarMoeda(valor) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
  }).format(valor);
}

async function calcularCashback(event) {
  event.preventDefault();

  const dados = {
    valor_compra: Number(valorCompra.value),
    cliente_vip: tipoCliente.value === "true"
  };

  try {
    const resposta = await fetch(`${API_URL}/calcular-cashback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    const calculo = await resposta.json();

    resultado.classList.remove("escondido");
    resultado.innerHTML = `
      <strong>Cashback final: ${formatarMoeda(calculo.cashback_total)}</strong>
      <p>Cashback base: ${formatarMoeda(calculo.cashback_base)}</p>
      <p>Bônus VIP: ${formatarMoeda(calculo.bonus_vip)}</p>
    `;

    valorCompra.value = "";

    carregarHistorico();
  } catch (erro) {
    resultado.classList.remove("escondido");
    resultado.classList.add("erro");
    resultado.innerHTML = "Erro ao calcular cashback. Verifique se a API está ligada.";
  }
}

async function carregarHistorico() {
  try {
    const resposta = await fetch(`${API_URL}/historico`);
    const consultas = await resposta.json();

    if (consultas.length === 0) {
      historico.innerHTML = "<p>Nenhuma consulta feita ainda.</p>";
      return;
    }

    historico.innerHTML = consultas.map((consulta) => {
      const tipo = consulta.cliente_vip ? "Cliente VIP" : "Cliente comum";

      return `
        <div class="item-historico">
          <strong>${tipo}</strong>
          <p>Valor da compra: ${formatarMoeda(consulta.valor_compra)}</p>
          <p>Cashback final: ${formatarMoeda(consulta.cashback_total)}</p>
          <p>Data: ${new Date(consulta.criado_em).toLocaleString("pt-BR")}</p>
        </div>
      `;
    }).join("");
  } catch (erro) {
    historico.innerHTML = "<p>Não foi possível carregar o histórico.</p>";
  }
}

formCashback.addEventListener("submit", calcularCashback);

carregarHistorico();