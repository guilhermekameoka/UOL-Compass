## API do Google Cloud Vision
Este é um código em JavaScript que utiliza a API Cloud Vision da Google para fazer a detecção de texto em uma imagem. Ele é executado em um servidor NodeJS, utilizando o framework Express.

## Integrantes
- Carlos Livius da Silva
- Fabio Romero de Souza Junior
- Guilherme Rimoldi Kameoka
- Paulo Eduardo Ferreira da Silva

## Instalação
Para utilizar este código, é necessário instalar o Node.js (https://nodejs.org) e os seguintes pacotes:

- express: npm install express
- multer: npm install multer
- nodemon: npm install nodemon
- @google-cloud/vision: npm install @google-cloud/vision

Também é necessário criar um arquivo credential.json com as suas credenciais do Google Cloud Vision. Para mais informações sobre como criar este arquivo, consulte a documentação da API do Google Cloud Vision (https://cloud.google.com/vision/docs/before-you-begin?hl=pt-br)

## Utilização
1. Inicialize um repositório com o comando npm init.
2. Instale as dependências do express, multer e da Cloud Vision API.
3. Coloque as credenciais da chave JSON gerada pelo Google Cloud no arquivo credential.json do projeto.
4. Execute o comando cd scr no terminal para acessar o diretório "./src".
5. Execute o código em um servidor Node.js com o comando "node server.js".
6. O código será executado na porta 3000 e para fazer uma requisição para a API basta clicar em "selecionar imagem". Após isso, irá abrir o explorador de arquivos solicitando que o usuário escolha uma imagem.
7. Selecionado uma imagem válida, a API irá retornar o texto encontrado no campo "resultado".
8. Uma mensagem de erro será exibida se a imagem não conter um texto.

## Funcionamento
O código utiliza o pacote Multer para fazer o upload da imagem. Em seguida, ele faz a chamada da API Cloud Vision através da função executeGoogleVisionAPI para fazer a detecção do texto na imagem que será retornado como resposta para a requisição.

## Dificuldades encontradas
Durante a execução do projeto, enfrentamos algumas dificuldades em relação ao tempo disponível, especialmente em relação ao desenvolvimento do código para consumir a API e em fazer a conexão entre o backend e o frontend da aplicação. Essas dificuldades acabaram impactando o progresso do projeto e exigiram mais esforços para serem superadas.