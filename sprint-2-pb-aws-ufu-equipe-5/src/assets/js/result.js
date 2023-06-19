const form = document.getElementById('form');
const result = document.getElementById('result');

// Mostra o resultado na tela via POST
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch('/vision', {
        method: 'POST',
        body: formData,
    })

    const data = await response.text();

    // Imagem sem texto
    if(data == '{"error":{}}'){
        result.innerHTML = "Erro! a imagem não contém texto 😣.";
    } else{
        result.innerHTML = data;
    }

    console.log(data);
});
