// Input
const inputFile = document.querySelector('#input__file');
const inputButton = document.querySelector('#input__button'); // Botão nativo

//DIV
const pictureImage = document.querySelector('.picture'); // Preview de imagem
const pictureImageTxt = 'Selecione uma Imagem 🖼️'; // Texto padrão
pictureImage.innerHTML = pictureImageTxt;

// Seleciona arquivo
pictureImage.addEventListener("click", (e) => { 
    inputFile.click();
});

// Botões
const resetButton = document.querySelector('#button-1');
const sendButton = document.querySelector('#button-2');

// Botão enviar
sendButton.addEventListener("click", (e) =>{
    inputButton.click();
});

// Botão resetar
function resetImage() {
    resetButton.addEventListener('click', function () {

        //Limpa o último Estado
        pictureImage.innerHTML = 'Tente outra imagem 🖼️';
    });
}

// Inserir Imagem
inputFile.addEventListener('change', function (e) {

    const inputTarget = e.target;
    const file = inputTarget.files[0];

    //Exibe o preview da Imagem caso seja um arquivo válido.
    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function (e) {
            const readerTarget = e.target;

            // Cria o documento do tipo imagem por meio do JS
            const img = document.createElement('img');
            img.src = readerTarget.result;
            img.classList.add('picture');

            //Limpa o último Estado
            pictureImage.innerHTML = '';

            // Adiciona o Preview da Imagem a tela.
            pictureImage.appendChild(img);

            // Botões
            resetImage();
            sendImage(); // Mostra URL
        });

        reader.readAsDataURL(file);

    } else {
        pictureImage.innerHTML = pictureImageTxt;
    }
});