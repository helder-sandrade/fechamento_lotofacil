#Criado por Programando o dIA
import os
import sys
from itertools import combinations

# Variaveis importantes
JOGO = []
RESULTADO = 'resultado.txt'
FECHAMENTO = 'fechamento.txt'
APOSTAS = 'lista_apostas.txt'

# Preparando o ambiente

PASTA_PROJETO = os.getcwd()
ARQUIVO_RESULTADO = os.path.join(PASTA_PROJETO, RESULTADO)
ARQUIVO_APOSTAS = os.path.join(PASTA_PROJETO, APOSTAS)
ARQUIVO_FECHAMENTO = os.path.join(PASTA_PROJETO, FECHAMENTO)

# Função para criação dos arquivos
def cria_arquivos() -> None:
    criado = False
    if not  os.path.isfile(ARQUIVO_RESULTADO):
        f = open(ARQUIVO_RESULTADO, 'w')
        f.close()
        criado = True
    if not  os.path.isfile(ARQUIVO_APOSTAS):
        f = open(ARQUIVO_APOSTAS, 'w')
        f.close()
        criado = True
    if not  os.path.isfile(ARQUIVO_FECHAMENTO):
        f = open(ARQUIVO_FECHAMENTO, 'w')
        f.close()
        criado = True
    if criado:
        print('Estrutura de arquivos criada')
        sair = input('Pressione enter para sair\r')
        sys.exit(1)

# Funções das apostas
# Função para criação das apostas
def cria_apostas() -> None:
    try:
        f = open(ARQUIVO_FECHAMENTO, 'r')
        fechamentos = f.read().splitlines()
        f.close()

        if len(fechamentos) == 0:
            raise ArquivoVazio
        for f in fechamentos:
            contador = 0
            if not ':' in f or not '-' in f:
                raise FormatoFechamentoErrado
            dezenas = f.split(':')[0].split('-')
            fixas = f.split(':')[1].split('-')

            if (len(dezenas) < 15 or len(dezenas) > 20) or (len(fixas) < 1 or len(fixas) > 14):
                raise FormatoFechamentoErrado
            todas_apostas = combinations(dezenas, 15)
            for aposta in todas_apostas:
                if check_fixos(fixas, aposta):
                    JOGO.append('-'.join(list(aposta)))
                    contador += 1
            print(f'Criado {contador} jogos, utilizando {len(fixas)} dezenas fixas')
        salva_apostas()
        sair = input('Pressione enter para sair\r')
    except ArquivoVazio:
        print('A arquivo de fechamento está vazio')
        sair = input('Pressione enter para sair\r')
        sys.exit(0)
    except FormatoFechamentoErrado:
        print('Formato do arquivo de fechamento está errado')
        sair = input('Pressione enter para sair\r')
        sys.exit(0)


# Função para verificar se todos os numeros fixos estão na aposta
def check_fixos(dezenas_fixas: list, jogo: list) -> bool:
    tamanho = len(dezenas_fixas)
    for df in dezenas_fixas:
        if df in jogo:
            tamanho -= 1
    if tamanho == 0:
        return True
    return False

# Função para salvar as apostas
def salva_apostas() -> None:
    f = open(ARQUIVO_APOSTAS, 'w')
    for jogo in JOGO:
        f.write(jogo)
        f.write('\n')
    f.close()

# Funções para o resultado
# Função para ler o resultado
def ler_resultado() -> list:
    try:
        lista = []
        f = open(ARQUIVO_RESULTADO, 'r')
        resultado = f.read()
        resultado = resultado.replace('\r', '')
        resultado = resultado.replace('\n', '')
        f.close()

        if len(resultado) == 0:
            return lista
        elif len(resultado) != 30:
            raise ErroNoArquivoResultado
        for i in range(2,31,2):
            lista.append(resultado[i-2:i])
        return lista
    except ErroNoArquivoResultado:
        print('Erro no arquivo de resultado')
        print('Copie e cole o resultado do site da caixa ou do google')
        sair = input('Pressione enter para sair\r')
        sys.exit(0)


# Função para ler as apostas
def ler_apostas() -> list:
    try:
        lista = []
        f = open(ARQUIVO_APOSTAS, 'r')
        apostas = f.read()
        if '\t' in apostas:
            print('Resultado ja conferido')
            sair = input('Pressione enter para sair\r')
            sys.exit(1)
        apostas = apostas.splitlines()
        f.close()
        for aposta in apostas:
            lista.append(aposta.split('-'))
        return lista
    except Exception as e:
        pass

# Função para contar os pontos feitos por uma aposta
def conta_pontos(resultado: list, aposta: list) -> str:
    contador = 0
    for r in resultado:
        if r in aposta:
            contador += 1
    return str(f'{contador:02}')

# Função para conferir os resultados
def confere_resultado() -> bool:
    try:
        apostas_verificadas = []
        resultado = ler_resultado()
        apostas = ler_apostas()
        if len(apostas) != 0 and len(resultado) >0:
            for aposta in apostas:
                apostas_verificadas.append('-'.join(aposta) + '\t' + conta_pontos(resultado, aposta))
            f = open(ARQUIVO_APOSTAS, 'w')
            for aposta in apostas_verificadas:
                f.write(aposta)
                f.write('\n')
            f.close()
            print('Jogos conferidos')
            sair = input('Pressione enter para sair\r')
            sys.exit(1)
        return False
    except Exception as e:
        pass


class Error(Exception):
    pass
class ArquivoVazio(Error):
    pass
class FormatoFechamentoErrado(Error):
    pass
class ErroNoArquivoResultado(Error):
    pass

# colocar o progtama para rodar

cria_arquivos()
if not confere_resultado():
    cria_apostas()
