# **Avaliação Sprint 4 - Programa de Bolsas Compass UOL / AWS e UFU**

Avaliação da quarta sprint do programa de bolsas Compass UOL para formação em machine learning para AWS.

## **Sobre o repositório**

Este repositório possui uma solução para a quarta avaliação do curso machine learning com AWS da Compass UOL. O objetivo é a implementação de uma API que consome outras 2 APIs, uma de piadas e outra de atividades. O sistema deve ser executado utilizando Node.JS e deve rodar em uma instância EC2 criada a partir da ferramenta Elastic Beanstalk. Foram abordadas as tecnologias Node.js, Express e AWS.

## **Execução do projeto Node.js**

Para executar o projeto criado com o Node.js, siga os passos abaixo:

1. Clone o repositório
2. Abra o terminal no diretório e realize o checkout para a branch `equipe-1`
3. Instale as dependências do Node utilizando o comando `npm install`
4. Execute o projeto node utilizando o comando `npm run start`.
5. Abra `http://localhost:8080/` para visualizar a aplicação.
6. Para a rota referente às piadas, digite `http://localhost:8080/api/piadas`
6. Para a rota referente às atividades, digite `http://localhost:8080/api/atividades`

## **Deploy do projeto no Elastic Beanstalk**

Para realizar o deploy do projeto no Elastic Beanstalk, deve-se:

- Escolher a opção 'Ambiente de servidor web'

- Informar o nome da aplicação (ex: sprint-4-grupo-1-deploy-3).

- Inserir etiquetas. No caso, a equipe inseriu a etiqueta 'Name' com o valor igual ao nome da aplicação.

- Nas informações do ambiente, deixar o nome default no nome do ambiente (sugestão da AWS).

- No item Plataforma, escolher a plataforma 'Node.JS'.

- Realizar o upload da aplicação criada com a tag de sua escolha. Deve-se lembrar de remover a pasta node_modules e o arquivo compactador deve ter extensão .zip.

- Em predefinições, deixar selecionado 'Instância única (qualificada para o nível gratuito)'.

- No tópico de Acesso ao serviço, deve-se inserir o par de chaves EC2 e o perfil de instância EC2 previamente criados.

- Em VPC, utilizar a opção disponível e na configuração de instâncias, deve-se selecionar ao menos 1 ou 2 subredes de instância.

- Não é necessário realizar nenhuma configuração referente a banco de dados e volume da raiz.

- No item 'Grupo de segurança do EC2', selecione a opção default.

- No item 'Capacidade', subitem 'Grupo de Auto Scaling', selecionar 'Instância sob demanda', arquitetura 'x86_64' e a instância do tipo t2.micro.

- No item 'Monitoramento', marcar a opção 'Aprimorado' e não mudar nenhuma configuração mostrada neste tópico.

- Desativar a opção de atualizações agendadas da plataforma e não é necessário inserir nenhum e-mail para notificação.

- No item 'Atualizações e implantações contínuas', deixar todas as opções default.

- No item 'Software de plataforma', a equipe optou pelo servidor de proxy do tipo 'Apache'.

- Na tela de review, basta confirmar todas as opções selecionadas anteriormente e aguardar a conclusão da configuração do ambiente.

Com o passo-a-passo descrito acima, a equipe conseguiu realizar o deploy da aplicação no Elastic Beanstalk.

#### Observações

Mais informações sobre o Elastic Beanstalk podem ser encontradas na [documentação da AWS](https://docs.aws.amazon.com/pt_br/elasticbeanstalk/latest/dg/Welcome.html)

## **Funcionamento**

A API criada funciona da seguinte forma:

### **Rota → Get /**

1. Nesta rota será efetuado um get na raiz do projeto.

2. O retorno desta API é um texto simples informando o grupo.

Exemplo:

```json
Este é o app do Grupo 1
```

3. O status code para sucesso da requisição é `200`

### **Rota → Get /api/piadas**

1. Nesta rota é efetuado um get em: [https://api.chucknorris.io/jokes/random](https://api.chucknorris.io/jokes/random)

2. O retorno da API é dado na seguinte formatação:

```json
{
  "data_atualizacao": "05-01-2020",
  "data_criacao": "05-01-2020",
  "icone": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
  "id": "b7585687-b14b-406d-a557-9cfeea4a8c16",
  "piada": "CHUCK NORRIS can slit your throat with his pinkie toenail.",
  "referencia": "https://api.chucknorris.io/jokes/2itjvbXZTcScUiuAMoOPLA"
}
```

3. O status code para sucesso da requisição é `200`

### **Rota → Get /api/atividades**

1. Nesta rota é efetuado um get em: [https://www.boredapi.com/api/activity](https://www.boredapi.com/api/activity)

2. O retorno da API é mostrado na seguinte formatação:

```json
{
  "id": "b7585687-b14b-406d-a557-9cfeea4a8c16",
  "atividade": "Wash your car",
  "tipo": "busywork",
  "participantes": 1,
  "acessibilidade": "15%"
}
```

3. Status code para sucesso da requisição é `200`

## **Desenvolvimento da atividade**

Inicialmente o repositório da sprint foi clonado e uma nova branch foi criada com o nome `equipe-1`. Após a etapa anterior, o trabalho desenvolvido nas sprint 2 e 3 foi reaproveitado e, em seguida, as modificações necessárias foram desenvolvidas. Iniciou-se a construção do código do projeto adotando o seguinte passo-a-passo:

- Criação das rotas para piadas e atividades

- Correção e testes de funcionamento para adequar às solicitações descritas no roteiro

- Deploy da aplicação no Elastic Beanstalk

## **Dificuldades**

A principal dificuldade encontrada pelo grupo foi o deploy da aplicação no Elastic Beanstalk. A configuração da ferramente se mostrou um desafio e diversas tentativas foram realizadas.

## **Membros da equipe**

- Chrystopher Pinter Oliveira Lacerda
- Guilherme Rimoldi Kameoka
- Manuela Oliveira Rocha e Souza
- Pedro Henrique Resende Ribeiro
