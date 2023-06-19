// Declaração dos módulos necessários
const express = require('express');             // npm install express
const routes = require('../routes/routes')   // Require nas rotas

// Inicializa a aplicação na rota 8080
const app = express();
const port = process.env.PORT || 8080;

// Utiliza as rotas definidas no arquivo routes.js
app.use(routes)

app.listen(port, function () {
    console.log('Aplicação rodando na porta: ' + port);
});