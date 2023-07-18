# Avaliação Sprint 6- grupo 2 - Programa de Bolsas Compass UOL / AWS e UFU

Avaliação da sexta sprint do programa de bolsas Compass UOL para formação em machine learning para AWS. No qual, foi
nos requisitado a resolução de uma aplicação que realizava a conversão de texto em audio, por meio de uma página HTML,
AWS Polly e que fosse salvo no DynamoDB e no S3;

***
## Execução
- Passo 1: Instale o framework serverless em seu computador.
  
```
npm install -g serverless
```
- Passo 2: Gere suas credenciais (AWS Acess Key e AWS Secret) na console AWS pelo IAM.
- Passo 3: Em seguida insira as credenciais e execute o comando conforme exemplo:
```json
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Também é possivel configurar via [aws-cli]
```json
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: ENTER
  ```
- Passo 4: Para efetuar o deploy da solução na sua conta aws execute (acesse a pasta `api-tts`):
 ```
serverless deploy
```
Depois de efetuar o deploy, vocẽ terá um retorno parecido com isso:

```bash
Deploying api-tts to stage dev (us-east-1)

Service deployed to stack api-tts-dev (85s)

endpoints:
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2
functions:
  health: api-tts-dev-health (2.1 kB)
  v1Description: api-tts-dev-v1Description (2.1 kB)
  v2Description: api-tts-dev-v2Description (2.1 kB)
```
- Passo 5: Abrir o arquivo index.html, conforme a imagem a seguir: 
  
  <img src = https://github.com/Compass-pb-aws-2023-UFU/sprint-6-pb-aws-ufu/assets/123610986/167ba1c1-3dd8-4801-a13a-e6f0fab5a412 width = "400px">
- Passo 6: Adicionar o o texto a ser convertido na rota de sua preferência:
  ```
  Lembrando:
  Rota 4: Apenas converte o texto em aúdio e salva no S3;
  Rota 5: Ela além de transformar o texto em aúdio, salva no S3 e no DynamoDB;
  Rota 6: Ela confere pelo ID se o texto não foi inserido, se já foi ele retorna os parâmetros da primeira inserção,
  caso contrário ela insere como a rota 5.
  ```
- Passo 7: Clicar em enviar e aproveitar o aúdio recém convertido;
- 
***
## Estrutura de rotas 
Nossas rotas para a aplicação são as:

``` Bash
GET /
GET /v1
GET /v2
GET /v3
POST /v1/tts
POST /v2/tts
POST /v3/tts
```
Retorno da rota `GET /`:

``` JSON
{
  "message": "Go Serverless v3.0! Your function executed successfully!",
  "input": { "... data ..." }
}
```

Retorno da rota `GET /v1`:

``` JSON
{
  "message": "TTS api version 1."
}
```

Retorno da rota `GET /v2`:

``` JSON
{
  "message": "TTS api version 2."
}
```

Retorno da rota `GET /v3`:

``` JSON
{
  "message": "TTS api version 3."
}
```
Retorno da rota `POST /v1/tts`:

``` JSON
{
    "received_phrase": "Teste grupo-2 v1",
    "url_to_audio": "https://sprint6-polly/f50c5db78e60fe17ad53bd1c1d6f6721f8049b3eaa3ae321e81864ac78005541.mp3",
    "created_audio": "03-07-2023 20:29:01"
}
```
Retorno da rota `POST /v2/tts`:

``` JSON
{
    "received_phrase": "Teste grupo-2 v2",
    "url_to_audio": "https://sprint6-polly/2a71a47e1771171979feb226756a1510c7ac21233f8c5d01031f5dde0576e6e0.mp3",
    "created_audio": "03-07-2023 20:30:37",
    "unique_id": "2a71a47e1771171979feb226756a1510c7ac21233f8c5d01031f5dde0576e6e0"
}
```

Retorno da rota `POST /v3/tts` caso não exista a chave no DynamoDB:

``` JSON
{
    "received_phrase": "Teste grupo-2 v3",
    "url_to_audio": "https://sprint6-polly/a2436b58e8b925c3333ba6a8f9dcabbe743cd864d53199ae11058e12ec6f3add.mp3",
    "created_audio": "03-07-2023 20:31:08",
    "unique_id": "a2436b58e8b925c3333ba6a8f9dcabbe743cd864d53199ae11058e12ec6f3add"
}
```
Retorno da rota `POST /v3/tts` caso exista a chave no DynamoDB:

``` JSON
{
  "received_phrase": "Teste grupo-2 v3",
    "url_to_audio": "https://sprint6-polly/a2436b58e8b925c3333ba6a8f9dcabbe743cd864d53199ae11058e12ec6f3add.mp3",
    "created_audio": "03-07-2023 20:31:08",
    "unique_id": "a2436b58e8b925c3333ba6a8f9dcabbe743cd864d53199ae11058e12ec6f3add"
}
```


***
## Arquitetura do projeto

### Rota 4:

<img src = "https://github.com/Compass-pb-aws-2023-UFU/sprint-6-pb-aws-ufu/assets/123610986/7ed894cb-72c4-4820-b591-663fcf6ff9b2" width = 500px>


### Rota 5:

<img src = "https://github.com/Compass-pb-aws-2023-UFU/sprint-6-pb-aws-ufu/assets/123610986/78417b35-3dda-4516-8b83-44fc731b3d29" width = 500px>


### Rota 6:

<img src = "https://github.com/Compass-pb-aws-2023-UFU/sprint-6-pb-aws-ufu/assets/123610986/78cc716a-034d-4f10-8e3f-a2119371781e" width = 500px>


***
## Tecnologias utilizadas:

- AWS Polly
- Bucket S3
- DynamoDB
- HTML
- JS
- Python
- Serveless
- Lambda
***
## Dificuldades encontradas:
Primeiramente, nosso grupo não teve nenhuma dificuldade que pudesse causar o impedimento total do grupo, porém tivemos algumas
que demandaram mais tempo para resolução como:
- Liberar permissõs do serveless
- Trabalhar com o framework serveless
- Fazer inserção no DynamoDB
***
## Integrantes
- Guilherme Rimoldi Kameoka
- Gustavo Guimaraes Reis 
- Vitor Pereira Thomé
***

