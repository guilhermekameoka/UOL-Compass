const express = require('express');
const multer = require('multer');
const { ImageAnnotatorClient } = require('@google-cloud/vision');

const app = express();
const upload = multer();

app.use(express.static('.'));

// Método POST | Definindo rota '/vision'
app.post('/vision', upload.single('image'), async (req, res) => {
  try {
    const htmlImage = req.file.buffer;
    const showText = await executeGoogleVisionAPI(htmlImage);
    res.send(showText);
  } catch (error) {
    console.error(error);
    res.sendStatus(500);
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Servidor porta ${port}`);
});

// Função para executar API
async function executeGoogleVisionAPI(fileNames) {

  // Cria um cliente para Google Cloud Vision
  const client = new ImageAnnotatorClient({
    keyFilename: 'credential.json',
  });

  // Converte o buffer em uma string base64
  const fileContent = fileNames.toString('base64');

  // Prepara a requisição para enviar a imagem à API 
  const request = {
    image: {
      content: fileContent,
    },
    features: [
      { type: 'TEXT_DETECTION' }, // Detecção de texto
    ],
  };

  try {
    // Envia a requisição para a API do Google Cloud Vision
    const [result] = await client.annotateImage(request);
    const text = result.textAnnotations;

    console.log('\nTexto encontrado:');
    console.log(text[0].description);

    // Retorna valor do texto
    return text[0].description;
  } catch (error) {
    console.error('Erro:', error);
    return { error };
  }
}