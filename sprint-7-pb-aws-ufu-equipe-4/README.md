# Avaliação Sprint 7 - Programa de Bolsas Compass UOL / AWS e UFU

Avaliação da sétima sprint do programa de bolsas Compass UOL para formação em machine learning para AWS.

***

## **Tabela de conteúdo**
  - [**Sobre este repositório**](#sobre)
  - [**Execução**](#execucao)
  - [**Funcionalidades**](#funcionalidades)
  - [**Desenvolvimento da atividade**](#desenvolvimento)
  - [**Dificuldades**](#dificuldades)
  - [**Integrantes da equipe**](#integrantes)

***

<div id="sobre"/>
  
## Sobre este repositório
Este repositório possui um chatbot (MedBot) desenvolvido com o objetivo de proporcionar auxílio aos usuários na busca por uma melhor qualidade de vida. Com foco na área de saúde, o MedBot oferece dicas e orientações personalizadas para ajudar as pessoas a adotarem hábitos saudáveis.

Além disso, o MedBot também oferece suporte em situações de emergência. Ele fornece instruções sobre primeiros socorros, orientando os usuários sobre como agir em casos de parada cardíaca, engasgamento, queimaduras, cortes e outras emergências comuns.

O bot também é capaz de disponibilizar os contatos de emergência essenciais, como SAMU, Corpo de Bombeiros e CVV (Centro de Valorização da Vida). Isso permite que os usuários obtenham ajuda rápida e apropriada em situações de emergência, garantindo que possam entrar em contato com os serviços adequados conforme necessário.

Veja todas as funcionalidades [aqui](#funcionalidades).

***
<div id="execucao"/>
  
## Execução
1. Abra o browser de sua preferência e acesse [aqui](https://join.slack.com/t/novoworkspace-h0s4728/shared_invite/zt-1zkl9cgs0-D2sgemjLLprmqTnj6FUHaQ).
2. Para logar, será necessário criar uma conta na plataforma (Slack). Conseguindo realizar o login, vá até a pagina inicial do Workspace Dev ChatSaude.
3. No side-bar esquerdo, na parte inferior, localiza-se o APP MedBot. Selecionando o bot, o chat irá abrir para a execução do serviço.
4. No campo de inserção de texto, digite "Olá" para invocar a execução.
5. O Chatbot é composto por perguntas dispostas em cards, as respostas estão dispostas em botões.
6. Para avançar no seu fluxo, será necessário clicar nos botões de sua preferência dentro dos cards. 
***
<div id="funcionalidades"/>
  
## Funcionalidades do MedBot
O chatbot possui 15 intents no total, sendo 4 principais. E é feito a captura de 3 slots:
  - Orientações personalizadas [Intent]
    - {faixaEtariaSlot} [Slot]
    - {fazExercicioSlot} [Slot]
    - {frequenciaSlot} [Slot]
  - Primeiro Socorros [Intent]
    - Parada respiratória [Intent]
    - Engasgamento [Intent]
    - Ferimentos e sangramentos [Intent]
    - Queimaduras [Intent]
    - Convulsões [Intent]
  - Dicas de saúde [Intent]
    - Hábitos alimentáres [Intent]
    - Atividades físicas [Intent]
    - Gerenciamento do sono [Intent]
  - Contatos de emergência [Intent]
    - SAMU [Intent]
    - Corpo de bombeiros [Intent]
    - Centro de valorização da vida (CVV) [Intent]
  
***
<div id="desenvolvimento"/>
  
## Desenvolvimento da atividade
A atividade foi desenvolvida por uma equipe de 3 integrantes, que por meio de reuniões e conversas foram alinhando o andamento da atividade e divisão de responsabilidades.


Para o desenvolvimento foi utilizado basicamente duas ferramentas sendo o Amazon Lex, para o desenvolvimento de fato do bot e também o Slack para criar uma integração com o Lex e disponibilizar o acesso externo à aplicação.


Além disso, o tema também foi escolhido em conjunto de forma que ele suprisse os requisitos impostos pela atividade.


Então, foram criadas ao todo 15 intents, algumas cumprindo o papel apenas de ser o próximo passo conversa com base nas opções selecionadas nas intents anteriores. Portanto, para algumas intents não foi necessário a criação de slots, mas o número mínimo definido como pré requisito foi alcançado.


Outro recurso muito utilizado foi o "Conditional Branch", para guiar o usuário dentro do fluxo de conversa com base nas opções selecionadas pelo mesmo.

***
<div id="dificuldades"/>
  
## Dificuldades encontradas
Não foi pré-requisitado, mas a inserção de Funções Lambda para a execução de uma intent foi um dos nossos impedimentos.
<br>A familiaridade com o próprio serviço Amazon Lex também, pois os contéudos distribuídos nos cursos estavam relacionados à outros tópicos.

***
<div id="integrantes"/>
  
## Integrantes da equipe
- Carlos Livius da Silva
- Guilherme Rimoldi Kameoka  
- Leandro Rodrigues de Ávila
