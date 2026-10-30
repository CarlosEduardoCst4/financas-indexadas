# Sistema de Gestão de Finanças Pessoais

Trabalho prático de **Estruturas de Arquivos Indexados** (ADS) — sistema de gerenciamento de finanças pessoais em Python, com interface gráfica em **CustomTkinter**.

## Ideia central: arquivo indexado

| Parte | Onde fica | Como é implementada |
|---|---|---|
| **Área de índices** | Memória (RAM) | Uma **Árvore Binária** por tabela (código → posição no arquivo) |
| **Área de dados** | Disco | Um arquivo **JSON Lines** (`.jsonl`) por tabela, na pasta `dados/` |

Ao abrir o programa, cada tabela lê seu arquivo uma vez e reconstrói sua árvore. Para buscar um registro, a árvore informa a posição em bytes e o arquivo é acessado direto com `seek()`, sem varrer tudo. Os dados continuam salvos mesmo desligando o computador.

## Tabelas

| Arquivo | Tabela | Campos |
|---|---|---|
| `Pessoas.py` | Pessoas | Codigo, Nome |
| `CategoriaGastos.py` | Categoria_Gastos | Codigo_Cat, Descricao |
| `Bancos.py` | Bancos | Cod_Banco, Descricao |
| `ContasBancarias.py` | Contas_Bancarias | Cod_Conta, Cod_Banco, Cod_Pessoa, Descricao, Saldo |
| `Transacoes.py` | Transacoes | Codigo_Trans, Cod_Cat, Cod_Conta, Data, Valor, Debito_Credito |

Além delas: `Interface.py` (telas em CustomTkinter) e `Main.py` (ponto de entrada).

## Funcionalidades

- Inclusão de dados em todas as tabelas
- Ao cadastrar uma conta, escolha do banco e da pessoa pelo nome
- Lançamento de transações com categoria e conta; **Crédito soma** e **Débito subtrai** do saldo da conta
- Extrato de transações por período, com o saldo do período
- Saldo de todas as contas e saldo geral
- Exclusão de transações (**exclusão lógica**: o registro continua no `.jsonl` marcado com `"excluida": true`, mas sai da árvore e o saldo da conta é estornado)
- Validação de campos vazios e bloqueio de valores negativos

## Como executar

Requisitos: Python 3.8+ e CustomTkinter.

```bash
pip install -r requirements.txt
python Main.py
```

A pasta `dados/` é criada automaticamente no primeiro cadastro. Este repositório inclui uma pasta `dados/` de exemplo, útil para demonstração.

## Estrutura do projeto

```
.
├── Main.py
├── Interface.py
├── Pessoas.py
├── CategoriaGastos.py
├── Bancos.py
├── ContasBancarias.py
├── Transacoes.py
├── requirements.txt
└── dados/            # arquivos .jsonl (uma linha JSON por registro)
```

## Formato dos dados

Exemplo de linha em `dados/transacoes.jsonl`:

```json
{"codigoTrans": 1, "codCategoria": 1, "codConta": 1, "data": "2026-09-01", "valor": 378.53, "debitoCredito": "D", "excluida": false}
```

As datas usam o formato `AAAA-MM-DD`.
