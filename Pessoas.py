import json
import os


class Pessoa:
    """dado de pessoa"""
    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome}

    @staticmethod
    def from_dict(d):
        return Pessoa(d["codigo"], d["nome"])


class Po:
    """Nó do índice: guarda o código e a posição do registro"""
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    """Índice em memória, da tabela Pessoas"""

    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Po(k, endereco)
        if self.raiz is None:
            self.raiz = novo
            return
        atual = self.raiz
        pai = None
        while atual is not None:
            pai = atual
            if k < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita
        if k < pai.codigo:
            pai.esquerda = novo
        else:
            pai.direita = novo

    def busca_na_arvore(self, k):
        atual = self.raiz
        while atual is not None:
            if k == atual.codigo:
                return atual.posicao
            elif k < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def listar_codigo(self):
        """Percurso em ordem -> devolve os códigos em ordem crescente"""
        codigos = []
        self._em_ordem(self.raiz, codigos)
        return codigos

    def _em_ordem(self, no, codigos):
        if no is not None:
            self._em_ordem(no.esquerda, codigos)
            codigos.append(no.codigo)
            self._em_ordem(no.direita, codigos)

    def limpar(self):
        self.raiz = None


class RepositorioPessoas:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "pessoas.jsonl")

    def __init__(self):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
        self.nomes = set()
        self._carregar_indice()

    @staticmethod
    def _normalizar(nome):
        return " ".join(nome.split()).casefold()

    def _carregar_indice(self):
        """Lê o arquivo uma vez e reconstrói a árvore e o conjunto de nomes"""
        os.makedirs(os.path.dirname(self.ARQUIVO), exist_ok=True)
        if not os.path.exists(self.ARQUIVO):
            return
        with open(self.ARQUIVO, "rb") as arq:
            while True:
                pos = arq.tell()
                linha = arq.readline()
                if linha == b"":
                    break
                if not linha.strip():
                    continue
                d = json.loads(linha.decode("utf-8"))
                self.arvore.inclusao(d["codigo"], pos)
                self.nomes.add(self._normalizar(d["nome"]))
                if d["codigo"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codigo"] + 1

    def incluir(self, nome):
        nome = " ".join(nome.split())          # limpa espaços extras
        if not nome:
            raise ValueError("O nome não pode ser vazio.")

        chave = self._normalizar(nome)
        if chave in self.nomes:
            raise ValueError()

        pessoa = Pessoa(self.proximo_codigo, nome)

        with open(self.ARQUIVO, "ab") as arq:
            pos = arq.tell()
            linha = json.dumps(pessoa.to_dict(), ensure_ascii=False) + "\n"
            arq.write(linha.encode("utf-8"))

        self.arvore.inclusao(pessoa.codigo, pos)
        self.nomes.add(chave)
        self.proximo_codigo += 1
        return pessoa

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "rb") as arq:
            arq.seek(pos)
            return Pessoa.from_dict(json.loads(arq.readline().decode("utf-8")))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigo()]