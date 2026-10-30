import json
import os


class CategoriaGasto:
    """dado da categoria de gasto"""
    def __init__(self, codigoCat, descricao):
        self.codigoCat = codigoCat
        self.descricao = descricao

    def to_dict(self):
        return {"codigoCat": self.codigoCat, "descricao": self.descricao}

    @staticmethod
    def from_dict(d):
        return CategoriaGasto(d["codigoCat"], d["descricao"])


class Cg:
    """Nó do índice: código + posição do registro"""
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    """Índice em memória, da tabela Categoria_Gastos"""

    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Cg(k, endereco)
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

    def listar_codigos(self):
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


class RepositorioCategoriaGasto:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "categorias.jsonl")

    def __init__(self):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
        self._carregar_indice()

    def _carregar_indice(self):
        os.makedirs(os.path.dirname(self.ARQUIVO), exist_ok=True)
        if not os.path.exists(self.ARQUIVO):
            return
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            while True:
                pos = arq.tell()
                linha = arq.readline()
                if linha == "":
                    break
                d = json.loads(linha)
                self.arvore.inclusao(d["codigoCat"], pos)
                if d["codigoCat"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codigoCat"] + 1

    def incluir(self, descricao):
        cat = CategoriaGasto(self.proximo_codigo, descricao)
        with open(self.ARQUIVO, "a", encoding="utf-8") as arq:
            pos = arq.tell()
            arq.write(json.dumps(cat.to_dict()) + "\n")
        self.arvore.inclusao(cat.codigoCat, pos)
        self.proximo_codigo += 1
        return cat

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            arq.seek(pos)
            return CategoriaGasto.from_dict(json.loads(arq.readline()))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigos()]
