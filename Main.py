from Pessoas import RepositorioPessoas
from Bancos import RepositorioBancos
from CategoriaGastos import RepositorioCategoriaGasto
from ContasBancarias import RepositorioContasBancarias
from Transacoes import RepositorioTransacoes
from Interface import App


def main():
    repo_pessoas = RepositorioPessoas()
    repo_bancos = RepositorioBancos()
    repo_categoriaGastos = RepositorioCategoriaGasto()
    repo_contaBancaria = RepositorioContasBancarias(repo_bancos, repo_pessoas)
    repo_transacoes = RepositorioTransacoes(repo_categoriaGastos, repo_contaBancaria)

    # Chama a janela da interface
    janela = App(repo_bancos, repo_pessoas, repo_categoriaGastos, repo_contaBancaria, repo_transacoes)
    janela.mainloop()


if __name__ == "__main__":
    main()
