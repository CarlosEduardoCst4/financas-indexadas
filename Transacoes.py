import json
import os


class Transacoes:
    def __init__(self, codTransacao, codCategoria, codConta, data, valor, DebitoCredito, excluida=False):
        self.codTransacao = codTransacao
        self.codCategoria = codCategoria
        self.codConta = codConta
        self.data = data
        self.valor = valor
        self.DebitoCredito = DebitoCredito
        self.excluida = excluida

    def to_dict(self):
        return {
            "codigoTrans": self.codTransacao,
            "codCategoria": self.codCategoria,
            "codConta": self.codConta,
            "data": self.data,
            "valor": self.valor,
            "debitoCredito": self.DebitoCredito,
            "excluida": self.excluida,
        }

    @staticmethod
    def from_dict(d):
        return Transacoes(
            d["codigoTrans"], d["codCategoria"], d["codConta"], d["data"], d["valor"],
            d["debitoCredito"], d.get("excluida", False),
        )


class Tr:
    """Nó do índice: código + posição"""
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    """Índice em memória, da tabela Transacoes"""

    def __init__(self):
        self.raiz = None

    def inclusao(self, k, endereco):
        novo = Tr(k, endereco)
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


class RepositorioTransacoes:
    ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "transacoes.jsonl")

    def __init__(self, repo_categorias, repo_contas):
        self.arvore = ArvoreBinaria()
        self.proximo_codigo = 1
        self.repo_categorias = repo_categorias
        self.repo_contas = repo_contas
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
                if not d.get("excluida", False):          # pula quem já está marcada como excluída
                    self.arvore.inclusao(d["codigoTrans"], pos)
                if d["codigoTrans"] >= self.proximo_codigo:
                    self.proximo_codigo = d["codigoTrans"] + 1

    def incluir(self, codCategoria, codConta, data, valor, debitoCredito):
        trans = Transacoes(self.proximo_codigo, codCategoria, codConta, data, valor, debitoCredito)
        with open(self.ARQUIVO, "a", encoding="utf-8") as arq:
            pos = arq.tell()
            arq.write(json.dumps(trans.to_dict()) + "\n")
        self.arvore.inclusao(trans.codTransacao, pos)
        self.proximo_codigo += 1

        conta = self.repo_contas.buscar(codConta)
        if debitoCredito == "C":
            novo_saldo = conta.saldo + valor
        else:
            novo_saldo = conta.saldo - valor
        self.repo_contas.atualizar_saldo(codConta, novo_saldo)
        return trans

    def buscar(self, codigo):
        pos = self.arvore.busca_na_arvore(codigo)
        if pos is None:
            return None
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            arq.seek(pos)
            return Transacoes.from_dict(json.loads(arq.readline()))

    def listar(self):
        return [self.buscar(c) for c in self.arvore.listar_codigos()]

    def listar_com_excluidas(self):
        """Lê o arquivo inteiro (fora da árvore), incluindo as marcadas como excluídas.
        Usado só internamente por excluir(), para poder regravar todo mundo."""
        todas = []
        if not os.path.exists(self.ARQUIVO):
            return todas
        with open(self.ARQUIVO, "r", encoding="utf-8") as arq:
            for linha in arq:
                todas.append(Transacoes.from_dict(json.loads(linha)))
        return todas

    def excluir(self, codigoTransacao):
        """exclusão lógica -> o registro continua no arquivo,
        só sai da árvore (marcado com excluida=True) e o saldo é estornado."""
        trans = self.buscar(codigoTransacao)
        if trans is None:
            return False

        conta = self.repo_contas.buscar(trans.codConta)
        if trans.DebitoCredito == "C":
            saldo_estornado = conta.saldo - trans.valor
        else:
            saldo_estornado = conta.saldo + trans.valor
        self.repo_contas.atualizar_saldo(trans.codConta, saldo_estornado)

        trans.excluida = True
        todas = self.listar_com_excluidas()
        todas = [t if t.codTransacao != codigoTransacao else trans for t in todas]
        self._regravar(todas)
        return True

    def _regravar(self, transacoes):
        self.arvore.limpar()
        with open(self.ARQUIVO, "w", encoding="utf-8") as arq:
            for t in transacoes:
                pos = arq.tell()
                arq.write(json.dumps(t.to_dict()) + "\n")
                if not t.excluida:                # só indexa quem não foi excluída
                    self.arvore.inclusao(t.codTransacao, pos)

    def extrato_por_periodo(self, data_ini, data_fim):
        """Datas em 'AAAA-MM-DD' podem ser comparadas como texto direto."""
        transacoes = [t for t in self.listar() if data_ini <= t.data <= data_fim]
        saldo_periodo = sum(t.valor if t.DebitoCredito == "C" else -t.valor for t in transacoes)
        return transacoes, saldo_periodo