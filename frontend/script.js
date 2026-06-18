const API_URL = 
  window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://nology-cashback-api.onrender.com";

const formCashback = document.getElementById("formCashback");
const tipoCliente = document.getElementById("tipoCliente");
const valorCompra = document.getElementById("valorCompra");
const percentualDesconto = document.getElementById("percentualDesconto");
const resultado = document.getElementById("resultado");
const historico = document.getElementById("historico");
const botaoCalcular = formCashback.querySelector("button");

function formatarMoeda(valor) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
  }).format(valor);
}

function mostrarErro(mensagem) {
  resultado.classList.remove("escondido");
  resultado.classList.add("erro");
  resultado.innerHTML = mensagem;
}

function limparErro() {
  resultado.classList.remove("erro");
}

async function calcularCashback(event) {
  event.preventDefault();

  limparErro();

  const dados = {
    valor_compra: Number(valorCompra.value),
    percentual_desconto: Number(percentualDesconto.value),
    cliente_vip: tipoCliente.value === "true"
  };

  botaoCalcular.disabled = true;
  botaoCalcular.textContent = "Calculando...";

  try {
    const resposta = await fetch(`${API_URL}/calcular-cashback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    if (!resposta.ok) {
      throw new Error("Erro ao calcular cashback. Verifique os valores informados.");
    }

    const calculo = await resposta.json();

    resultado.classList.remove("escondido");
    resultado.innerHTML = `
      <strong>Cashback final: ${formatarMoeda(calculo.cashback_total)}</strong>
      <p>Valor original: ${formatarMoeda(calculo.valor_compra)}</p>
      <p>Desconto aplicado: ${calculo.percentual_desconto}%</p>
      <p>Valor final da compra: ${formatarMoeda(calculo.valor_final)}</p>
      <p>Cashback base: ${formatarMoeda(calculo.cashback_base)}</p>
      <p>Bônus VIP: ${formatarMoeda(calculo.bonus_vip)}</p>
    `;

    valorCompra.value = "";
    percentualDesconto.value = "0";

    carregarHistorico();
  } catch (erro) {
    mostrarErro(erro.message);
  } finally {
    botaoCalcular.disabled = false;
    botaoCalcular.textContent = "Calcular cashback";
  }
}

async function carregarHistorico() {
  try {
    const resposta = await fetch(`${API_URL}/historico`);

    if (!resposta.ok) {
      throw new Error("Erro ao carregar histórico.");
    }

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
          <p>Valor original: ${formatarMoeda(consulta.valor_compra)}</p>
          <p>Desconto: ${consulta.percentual_desconto}%</p>
          <p>Valor final: ${formatarMoeda(consulta.valor_final)}</p>
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