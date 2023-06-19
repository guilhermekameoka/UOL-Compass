const crypto = require('crypto');               // Gerção GUID aleatório

// Função para formatar a resposta JSON
function formatJSONResponse(data) {
    // Converte o objeto data em uma string JSON formatada
    const formattedJSON = JSON.stringify(data, null, 2).replace(/,"(?=.)/g, ',\n"');
    return formattedJSON;
}

// Faz as formatações necessárias no objeto data
function jokes(data) {
    
    let jokes_json = {
        "data_atualizacao": new Date(data.updated_at).toLocaleDateString('pt-BR'),        // campo “updated_at” da resposta da API original
        "data_criacao": new Date(data.created_at).toLocaleDateString('pt-BR'),            // campo “created_at” da resposta da API original
        "icone": data.icon_url,                                                           // campo “icon_url” da resposta da API original (mantido original)
        "id": crypto.randomUUID,                                                          // Gera um GUID aleatório
        "piada": data.value.replace(/Chuck Norris/g, 'Chuck Norris'.toUpperCase()),       // campo “value” da resposta da API original
        "referencia": data.url                                                            // campo “url” da resposta da API original (mantido original)
    }
    return jokes_json;
};

// Faz as formatações necessárias no objeto data
function activity(data) {

    let activity_json = {
        "id": crypto.randomUUID(),               // Gera um GUID aleatório
        "atividade": data.activity,              // campo “activity” da resposta da API original
        "tipo": data.type,                       // campo “type” da resposta da API original (mantido original)
        "participantes": data.participants,      // campo “participants” da resposta da API original. (mantido original)
        // Transforma em porcentagem
        "acessibilidade": `${(data.accessibility * 100).toFixed(0)}%`     // campo “accessibility” da resposta da API original
    }
    return activity_json;
};

// Exportando as funções
module.exports = {
    formatJSONResponse,
    activity,
    jokes
};
