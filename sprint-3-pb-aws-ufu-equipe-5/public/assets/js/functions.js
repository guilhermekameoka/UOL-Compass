// Aguarda o carregamento completo da arvore DOM
document.addEventListener('DOMContentLoaded', function () {
    
    // Quando o valor do campo de entrada de arquivo é alterado
    document.getElementById('file').onchange = function () {
        previewImage(); // Chama a função para visualizar a imagem selecionada
    };

    // Botão input
    const sendFile = document.getElementById('file');

    document.getElementById('file_selector').onclick = function () {
        sendFile.click();
    };

    // Quando o botão de enviar é clicado
    document.getElementById('color_detect').onclick = function () {
        output.innerHTML = ''; // Limpa o conteúdo de saída anterior
        const data = new FormData();
        data.append('file', document.getElementById('file').files[0]); // Obtém o arquivo selecionado
        axios.post('/color', data) // Envia uma solicitação POST para o servidor
            .then(function (result) {
                const properties = result.data[0].imagePropertiesAnnotation; // Obtém as propriedades da imagem analisada
                const colors = properties.dominantColors.colors; // Obtém as cores da imagem
                const sorted_colors = colors.sort((a, b) => b.pixelFraction - a.pixelFraction); // Ordena as cores com base na fração de pixels
                sorted_colors.forEach(color => output.appendChild(build_color_box(color))); // Cria caixas de cor para cada cor dominante
            })
            .catch(function (err) {
                console.log(err); // Exibe o erro no console, caso ocorra algum problema
            });
    };

    // Função para criar uma caixa de cor
    function build_color_box(color_data) {
        const new_div = document.createElement('div');
        new_div.style.backgroundColor = `rgba(${color_data.color.red},
             ${color_data.color.green},${color_data.color.blue},1)`; // Define a cor de fundo da caixa de acordo com os valores RGB
        new_div.className = 'colorBlock'; // Define a classe CSS para a caixa de cor
        new_div.innerText = `${color_data.pixelFraction.toFixed(2)} R${color_data.color.red} G${color_data.color.green} B${color_data.color.blue}`; // Define o texto dentro da caixa de cor
        return new_div;
    }

    // Função para visualizar a imagem selecionada
    function previewImage() {
        const input = document.getElementById('file'); // Obtém o elemento de entrada de arquivo do HTML
        if (input.files && input.files[0]) { // Verifica se um arquivo foi selecionado
            var reader = new FileReader(); // Cria uma instância do objeto FileReader

            // Define o evento de carregamento do leitor de arquivos
            reader.onload = function (e) {
                const img = document.createElement('img'); // Cria um elemento de imagem HTML
                img.src = e.target.result; // Define a origem da imagem como o resultado do carregamento do arquivo
                img.className = 'img-thumbnail'; // Define a classe CSS para a imagem
                const img_holder = document.getElementById('img-thumb');
                img_holder.innerHTML = ''; // Limpa qualquer conteúdo anterior no container
                img_holder.appendChild(img); // Adiciona a imagem ao container
            };

            reader.readAsDataURL(input.files[0]); // Lê o conteúdo do arquivo como URL de dados
            // A URL de dados representa o conteúdo do arquivo em base64 que pode ser usada diretamente como valor da propriedade "src" de da tag "img"
        }
    }
});