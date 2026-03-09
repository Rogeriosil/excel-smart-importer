// Atalho simples para pegar elementos por ID.
const $ = (id) => document.getElementById(id);

// Mostra mensagem de sucesso ou erro no topo do card.
function mostrarMensagem(texto, tipo = "ok") {
  const el = $("mensagem");
  el.textContent = texto;
  el.className = `alerta ${tipo}`;
  el.style.display = "block";
}

// Esconde a caixa de mensagem.
function esconderMensagem() {
  const el = $("mensagem");
  el.textContent = "";
  el.style.display = "none";
}

// Busca todas as importações salvas no backend.
async function listarImportacoes() {
  const tbody = $("tbodyImportacoes");
  tbody.innerHTML = "";
  $("vazioImportacoes").style.display = "none";

  const resp = await fetch("/api/importacoes");
  const dados = await resp.json();

  if (!Array.isArray(dados) || dados.length === 0) {
    $("vazioImportacoes").style.display = "block";
    return;
  }

  for (const item of dados) {
    const tr = document.createElement("tr");
    tr.className = "clicavel";
    tr.innerHTML = `
      <td>${item.id}</td>
      <td>${item.nome_arquivo}</td>
      <td>${item.total_linhas}</td>
      <td>${item.total_validas}</td>
      <td>${item.total_invalidas}</td>
      <td>${new Date(item.criado_em).toLocaleString("pt-BR")}</td>
    `;
    tr.addEventListener("click", () => carregarDetalhes(item.id));
    tbody.appendChild(tr);
  }
}

// Carrega os detalhes de uma importação específica.
async function carregarDetalhes(importacaoId) {
  const resp = await fetch(`/api/importacoes/${importacaoId}`);
  const dados = await resp.json();

  const tbodyValidos = $("tbodyValidos");
  const tbodyInvalidos = $("tbodyInvalidos");
  tbodyValidos.innerHTML = "";
  tbodyInvalidos.innerHTML = "";

  $("vazioValidos").style.display = dados.validos.length ? "none" : "block";
  $("vazioInvalidos").style.display = dados.invalidos.length ? "none" : "block";

  for (const item of dados.validos) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.linha_excel}</td>
      <td>${item.nome}</td>
      <td>${item.documento}</td>
      <td>${item.email || "-"}</td>
      <td>${item.telefone || "-"}</td>
    `;
    tbodyValidos.appendChild(tr);
  }

  for (const item of dados.invalidos) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.linha_excel}</td>
      <td>${item.nome || "-"}</td>
      <td>${item.documento || "-"}</td>
      <td>${item.motivo}</td>
    `;
    tbodyInvalidos.appendChild(tr);
  }
}

// Envia o Excel para o backend via FormData.
async function importarExcel() {
  esconderMensagem();

  const inputArquivo = $("arquivoExcel");
  const arquivo = inputArquivo.files[0];

  if (!arquivo) {
    mostrarMensagem("Selecione um arquivo Excel antes de importar.", "erro");
    return;
  }

  const formData = new FormData();
  formData.append("arquivo", arquivo);

  const resp = await fetch("/api/importar", {
    method: "POST",
    body: formData,
  });

  const dados = await resp.json();

  if (!resp.ok) {
    mostrarMensagem(dados.erro || "Erro ao importar arquivo.", "erro");
    return;
  }

  mostrarMensagem(dados.mensagem || "Importação concluída.", "ok");
  inputArquivo.value = "";
  await listarImportacoes();
}

// Liga eventos da interface.
$("btnImportar").addEventListener("click", importarExcel);
$("btnAtualizar").addEventListener("click", listarImportacoes);

// Carrega a lista inicial quando a página abre.
listarImportacoes();
