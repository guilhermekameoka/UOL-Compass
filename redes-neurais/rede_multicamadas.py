# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 11:44:00 2023

@author: grkam
"""

#importacao da biblioteca numpy
import numpy as np


#calcula a ativacao a partir da soma
def sigmoid(soma):
    return 1/(1+np.exp(-soma))

#calcula a derivada da ativacao
def sigmoidDerivada(sig):
    return sig*(1-sig)


entradas = np.array ([[0,0],
                      [0,1],
                      [1,0],
                      [1,1]])

saidas = np.array ([[0],[1],[1],[0]])

#pesos0 = np.array([[-0.424, -0.740, -0.961],
#                  [0.358, -0.577, -0.469]])

#pesos1 = np.array([[-0.017], [-0.893], [0.148]])

pesos0 = 2* np.random.random((2,3)) - 1
pesos1 = 2* np.random.random((3,1)) -1

epocas = 100
taxaAprendizagem = 0.6
momento = 1

for j in range(epocas):
    camadaEntrada = entradas
    
    somaSinapse0 = np.dot(camadaEntrada, pesos0)
    camadaOculta = sigmoid(somaSinapse0)
    
    somaSinapse1 = np.dot(camadaOculta, pesos1)
    camadaSaida = sigmoid(somaSinapse1)
    
    erroCamadaSaida = saidas - camadaSaida
    mediaAbsoluta = np.mean(np.abs(erroCamadaSaida))
    print("Erro: " +str(mediaAbsoluta))
    
    derivadaSaida = sigmoidDerivada(camadaSaida)
    
    deltaSaida = erroCamadaSaida * derivadaSaida
    
    #transformando a matriz de pesos1 em matriz transposta
    pesos1Transposta = pesos1.T
    #multiplica o deltaSaida pelo pesos1
    deltaSaidaXPeso = deltaSaida.dot(pesos1Transposta)
    #calcula o deltaCamadaOculta
    deltaCamadaOculta = deltaSaidaXPeso * sigmoidDerivada(camadaOculta)
    
    # Mudança dos pesos da camada oculta para a camada de saida
    camadaOcultaTransporta = camadaOculta.T
    pesosNovo1 = camadaOcultaTransporta.dot(deltaSaida)
    # Formula: Peso n+1 = (peso(n) * momento) + (entrada * delta * taxaAprendizagem)
    pesos1 = (pesos1 * momento) + (pesosNovo1 * taxaAprendizagem)
    
    camadaEntradaTransposta = camadaEntrada.T
    pesosNovo0 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momento) + (pesosNovo0 * taxaAprendizagem)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    