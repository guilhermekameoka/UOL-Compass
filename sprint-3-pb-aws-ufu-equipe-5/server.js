// Importação dos pacotes necessários
const express = require("express"); // Pacote para criar o servidor web
const path = require("path"); // Pacote para manipular caminhos de arquivo
const router = require('./public/routes/routes');// Recupera a rota da pasta rotas

const app = express(); // Criação de uma instância do servidor Express
const port = process.env.PORT || 3000; // Porta em que o servidor irá rodar (padrão: 3000)


app.use(router); // Executa a rota importada da pasta rotas

// Middleware para servir arquivos estáticos na pasta "public"
app.use(express.static(path.join(__dirname, "public")));

// Inicia o servidor
const server = app.listen(port, () => {
  console.log(`Servidor rodando na porta ${server.address().port}`); // Exibe uma mensagem quando o servidor estiver online
});