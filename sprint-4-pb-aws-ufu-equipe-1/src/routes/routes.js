// Declaração dos módulos necessários
const express = require('express')
const fetch = require('isomorphic-fetch');      // Requisições assíncronas
const routes = express.Router()                 // Módulo para trabalhar com rotas
const { formatJSONResponse, activity, jokes } = require('../js/functions');     // Importa as funções do arquivo functions.js

// Rota raiz
routes.get('/', function (req, res) {
    res.send('Este é o app do Grupo 1');
});


// Rota piadas
routes.get('/api/piadas', async function (req, res) {
    try {
        // Requisição assíncrona para a API
        const response = await fetch('https://api.chucknorris.io/jokes/random');
        // Se a resposta falhar, a mensagem de erro é mostrada no console
        if (!response.ok) throw new Error(response.statusText);
        // Se a resposta da promise não falhar, transforma o resultado em json
        const data = await response.json();

        // Faz com que a resposta seja interpretada como json
        res.setHeader('Content-Type', 'application/json');
        // Chama a função formatJSONResponse e retorna a resposta formatada
        res.send(formatJSONResponse(jokes(data)));

    } catch (error) {
        console.error(error);
        return;
    }
});


// Rota atividades
routes.get('/api/atividades', async function (req, res) {
    try {
        // Requisição assíncrona para a API
        const response = await fetch('https://www.boredapi.com/api/activity');
        // Se a resposta falhar, a mensagem de erro é mostrada no console
        if (!response.ok) throw new Error(response.statusText);
        // Se a resposta da promise não falhar, transforma o resultado em JSON
        const data = await response.json();

        // Faz com que a resposta seja interpretada como json
        res.setHeader('Content-Type', 'application/json');
        // Chama a função formatJSONResponse e retorna a resposta formatada
        res.send(formatJSONResponse(activity(data)));

    } catch (error) {
        console.error(error);
        return;
    }
});

// Caso entre com uma rota inexistente
routes.get('*', (req, res) => {
    res.send('Rota não existe!')
})

// Exportando as rotas
module.exports = routes;