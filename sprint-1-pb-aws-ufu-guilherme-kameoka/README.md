# Avaliação Sprint 1 - Programa de Bolsas Compass UOL / AWS e UFU

Avaliação da primeira sprint do programa de bolsas Compass UOL para formação em machine learning para AWS.

***

## Descrição

Foi desenvolvido uma aplicação em JavaScript que consiste na verificação de um código PIN no qual o usuário deverá tentar adivinhá-lo.
O programa irá dar dicas se o número escolhido pelo usuário está perto ou longe do acerto.
Mensagens como "Muito maior/menor", "Menor/Maior", "Um pouco maior/menor" será mostrada na tela para facilitar que o usuário acerte o PIN.


***
## Execução (Código Fonte)
    1. Será solicitado que o usuário digite um número positivo de quatro algarismos.
    2. O programa irá fazer a verificação do número digitado.
      - Caso o usuário entre com algum valor que não seja numérico, será mostrado uma mensagem de erro "ERRO: O valor digitado nao eh um numero!"
      - Caso o usuário entre com um número inválido, será mostrado uma mensagem de erro "O numero deve ter 4 algarismos!" e ele deverá escolher novamente.
    3. O valor digitado pelo usuário será armazenado na variável "num".
    4. Será feito o cálculo da diferença entre o PIN e o número digitado e o resultado é armazenado na variável "dif".
    5. O programa irá dar uma dica se o número é maior ou menor que o PIN.
        - Se a diferença entre o PIN e o número digitado for maior ou igual a 1000, então a dica será "Muito maior/menor".
        - Se a diferença for menor que 1000 e maior que 100, então a dica será "Maior/menor".
        - Se for menor ou igual a 100, então a dica será "Um pouquinho maior/menor".
    6. Isso se repetirá até que o usuário acerte o PIN.
    
***
## Autor

  Guilherme Rimoldi Kameoka

***
## Dificuldades encontradas

Tive dificuldades em tratar números com zeros à esquerda caso o usuário entre com o valor 0001, por exemplo.
