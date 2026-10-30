import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, repo_bancos, repo_pessoas, repo_categorias, repo_contas, repo_transacoes):
        super().__init__()

        # repositórios recebidos do Main
        self.repo_bancos = repo_bancos
        self.repo_pessoas = repo_pessoas
        self.repo_categorias = repo_categorias
        self.repo_contas = repo_contas
        self.repo_transacoes = repo_transacoes

        self.title("Sistema de Gestão de Finanças Pessoais")
        self.geometry("900x600")

        # Divisão tela
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Parte lateral
        self.barra_lateral = ctk.CTkFrame(self, width=200)
        self.barra_lateral.grid(row=0, column=0, sticky="nsew")

        # Parte principal
        # command=ao_trocar_aba: toda vez que o usuário troca de aba, os menus são
        # atualizados com os dados mais recentes
        self.janela_abas = ctk.CTkTabview(self, width=400, command=self.ao_trocar_aba)
        self.janela_abas.grid(row=0, column=1, sticky="nsew", padx=10)

        self.janela_abas.add("Bancos")
        self.janela_abas.add("Pessoas")
        self.janela_abas.add("Categorias")
        self.janela_abas.add("Contas")
        self.janela_abas.add("Transações")
        self.janela_abas.add("Relatórios")

        # Chamadas
        # aba lateral
        self.construir_abaLateral()

        # aba Pessoa
        self.construir_abaPessoas()

        # aba Banco
        self.constrir_abaBanco()

        # aba Categoria
        self.construir_abaCategoria()

        # aba Conta
        self.construir_abaConta()

        # aba Transacao
        self.construir_abaTransacao()

        # aba Relatórios
        self.construir_abaRelatorios()

    def ao_trocar_aba(self):
        aba = self.janela_abas.get()
        if aba == "Contas":
            self.atualizar_menu_bancos()
            self.atualizar_menu_pessoas()
        elif aba == "Transações":
            self.atualizar_menu_categorias()
            self.atualizar_menu_contas()
            self.atualizar_menu_transacoes()
        elif aba == "Relatórios":
            self.atualizar_saldo_geral()


    def construir_abaLateral(self):
        self.titulo = ctk.CTkLabel(self.barra_lateral, text="Finanças", font=ctk.CTkFont(size=24, weight="bold"))
        self.titulo.pack(pady=(30, 10), padx=(60, 60))

        self.switch_mododark = ctk.CTkSwitch(self.barra_lateral, text="☀️​", command=self.alternar_tema)
        self.switch_mododark.pack(pady=(10, 25), side="bottom")

        # Altera a cor do tema (claro ou escuro)
    def alternar_tema(self):
        ctk.set_appearance_mode("Light" if self.switch_mododark.get() else "Dark")

    def constrir_abaBanco(self):
        aba_banco = self.janela_abas.tab("Bancos")

        self.campo_nomeBanco = ctk.CTkEntry(aba_banco, placeholder_text="Digite o Nome do Banco", width=300)
        self.campo_nomeBanco.pack(pady=(20, 20))

        self.botao_salvarBanco = ctk.CTkButton(aba_banco, text="Salvar Banco", hover_color="green",
                                                command=self.salvar_banco)
        self.botao_salvarBanco.pack(pady=(20, 20))

        self.label_erroBanco = ctk.CTkLabel(aba_banco, text="", text_color="red")
        self.label_erroBanco.pack(pady=(0, 10))

    def salvar_banco(self):
        nome = self.campo_nomeBanco.get().strip()
        if not nome:
            self.label_erroBanco.configure(text="Preencha o nome do banco.")
            return
        self.label_erroBanco.configure(text="")
        self.repo_bancos.incluir(nome)
        self.campo_nomeBanco.delete(0, "end")
        self.atualizar_menu_bancos()
        

    def construir_abaPessoas(self):
        aba_pessoa = self.janela_abas.tab("Pessoas")

        self.campo_nomepessoa = ctk.CTkEntry(aba_pessoa, placeholder_text="Digite o Seu Nome", width=300)
        self.campo_nomepessoa.pack(pady=(20, 20))

        self.botao_salvarPessoa = ctk.CTkButton(aba_pessoa, text="Salvar Pessoa", hover_color="green",
                                                 command=self.salvar_pessoa)
        self.botao_salvarPessoa.pack(pady=(20, 20))

        self.label_erroPessoa = ctk.CTkLabel(aba_pessoa, text="", text_color="red")
        self.label_erroPessoa.pack(pady=(0, 10))

    def salvar_pessoa(self):
        nome = self.campo_nomepessoa.get().strip()
        if not nome:
            self.label_erroPessoa.configure(text="Preencha o nome da Pessoa.")
            return
        self.label_erroPessoa.configure(text="")
        if not nome:
            self.repo_pessoas.incluir(nome)
        self.campo_nomepessoa.delete(0, "end")
        self.atualizar_menu_pessoas()

    def construir_abaCategoria(self):
        aba_categoria = self.janela_abas.tab("Categorias")

        self.campo_nomeCategoria = ctk.CTkEntry(aba_categoria, placeholder_text="Digite o Nome da Categoria", width=300)
        self.campo_nomeCategoria.pack(pady=(20, 20))

        self.botao_salvarCategoria = ctk.CTkButton(aba_categoria, text="Salvar Categoria", hover_color="green",
                                                     command=self.salvar_categoria)
        self.botao_salvarCategoria.pack(pady=(20, 20))

        self.label_erroCategoria = ctk.CTkLabel(aba_categoria, text="", text_color="red")
        self.label_erroCategoria.pack(pady=(0, 10))
    
    def salvar_categoria(self):
        nome = self.campo_nomeCategoria.get().strip()
        if not nome:
            self.label_erroCategoria.configure(text="Preencha a Categoria.")
            return
        self.label_erroCategoria.configure(text="")
        self.repo_categorias.incluir(nome)
        self.campo_nomeCategoria.delete(0, "end")
        self.atualizar_menu_categorias()

    def construir_abaConta(self):
        aba_conta = self.janela_abas.tab("Contas")

        self.campo_nomeConta = ctk.CTkEntry(aba_conta, placeholder_text="Digite o Nome da Conta", width=300)
        self.campo_nomeConta.pack(pady=(20, 5))

        self.aba_conta = self.janela_abas.tab("Contas")
        self.label_bancos = ctk.CTkLabel(self.aba_conta, text="Selecione o Banco")
        self.label_bancos.pack(pady=(5, 5))

        self.menu_bancos = ctk.CTkOptionMenu(self.aba_conta, values=["Cadastre um banco"])
        self.menu_bancos.pack(pady=(5, 10))

        self.aba_conta = self.janela_abas.tab("Contas")
        self.label_pessoas = ctk.CTkLabel(self.aba_conta, text="Selecione a Pessoa")
        self.label_pessoas.pack(pady=(5, 5))

        self.menu_pessoas = ctk.CTkOptionMenu(self.aba_conta, values=["Cadastre uma pessoa"])
        self.menu_pessoas.pack(pady=(5, 10))

        self.campo_saldoInicial = ctk.CTkEntry(aba_conta, placeholder_text="Digite o Saldo Inicial", width=300)
        self.campo_saldoInicial.pack(pady=(20, 5))

        self.botao_salvarConta = ctk.CTkButton(aba_conta, text="Salvar Conta", hover_color="green",
                                                command=self.salvar_conta)
        self.botao_salvarConta.pack(pady=(20, 20))

        self.label_erroConta = ctk.CTkLabel(aba_conta, text="", text_color="red")
        self.label_erroConta.pack(pady=(0, 10))

        self.atualizar_menu_bancos()
        self.atualizar_menu_pessoas()

    def atualizar_menu_bancos(self):
        # guarda a lista de objetos p/ recuperar o Banco escolhido pelo texto do menu
        self.bancos_disponiveis = self.repo_bancos.listar()
        valores = [b.descricao for b in self.bancos_disponiveis] or ["Cadastre um banco"]
        self.menu_bancos.configure(values=valores)
        self.menu_bancos.set(valores[0])

    def atualizar_menu_pessoas(self):
        self.pessoas_disponiveis = self.repo_pessoas.listar()
        valores = [p.nome for p in self.pessoas_disponiveis] or ["Cadastre uma pessoa"]
        self.menu_pessoas.configure(values=valores)
        self.menu_pessoas.set(valores[0])

    def salvar_conta(self):
        descricao = self.campo_nomeConta.get().strip()
        if not descricao or not self.bancos_disponiveis or not self.pessoas_disponiveis:
            self.label_erroConta.configure(text="Preencha todos os campos.")
            return
        try:
            saldo = float(self.campo_saldoInicial.get())
        except ValueError:
            self.label_erroConta.configure(text="Saldo inválido.")
            return
        if saldo < 0:
            self.label_erroConta.configure(text="O saldo não pode ser negativo.")
            return

        banco = next((b for b in self.bancos_disponiveis if b.descricao == self.menu_bancos.get()), None)
        pessoa = next((p for p in self.pessoas_disponiveis if p.nome == self.menu_pessoas.get()), None)
        if banco is None or pessoa is None:
            self.label_erroConta.configure(text="Selecione um banco e uma pessoa válidos.")
            return

        self.label_erroConta.configure(text="")
        self.repo_contas.incluir(banco.cod_banco, pessoa.codigo, descricao, saldo)
        self.campo_nomeConta.delete(0, "end")
        self.campo_saldoInicial.delete(0, "end")
        self.atualizar_menu_contas()
        self.atualizar_saldo_geral()

    def construir_abaTransacao(self):
        aba_transacao = self.janela_abas.tab("Transações")

        self.aba_transacao = self.janela_abas.tab("Transações")
        self.label_categoria = ctk.CTkLabel(self.aba_transacao, text="Selecione a Categoria")
        self.label_categoria.pack(pady=(5, 5))

        self.menu_categoria = ctk.CTkOptionMenu(self.aba_transacao, values=["Cadastre uma categoria"])
        self.menu_categoria.pack(pady=(5, 10))

        self.aba_transacao = self.janela_abas.tab("Transações")
        self.label_conta = ctk.CTkLabel(self.aba_transacao, text="Selecione a Conta")
        self.label_conta.pack(pady=(5, 5))

        self.menu_conta = ctk.CTkOptionMenu(self.aba_transacao, values=["Cadastre uma conta"])
        self.menu_conta.pack(pady=(5, 10))

        self.campo_dataTrasacao = ctk.CTkEntry(aba_transacao, placeholder_text="Digite a Data (AAAA-MM-DD)", width=300)
        self.campo_dataTrasacao.pack(pady=(20, 20))

        self.campo_valorTrasacao = ctk.CTkEntry(aba_transacao, placeholder_text="Digite o Valor", width=300)
        self.campo_valorTrasacao.pack(pady=(20, 5))

        self.aba_transacao = self.janela_abas.tab("Transações")
        self.label_tipo = ctk.CTkLabel(self.aba_transacao, text="Selecione o Tipo")
        self.label_tipo.pack(pady=(5, 5))

        self.menu_tipo = ctk.CTkOptionMenu(self.aba_transacao, values=["Debito", "Credito"])
        self.menu_tipo.pack(pady=(5, 10))

        self.botao_salvarTransacao = ctk.CTkButton(aba_transacao, text="Salvar Transação", hover_color="green",
                                                 command=self.salvar_transacao)
        self.botao_salvarTransacao.pack(pady=(20, 10))

        self.label_erroTransacao = ctk.CTkLabel(aba_transacao, text="", text_color="red")
        self.label_erroTransacao.pack(pady=(0, 10))

        # excluir uma transação lançada
        self.label_excluir = ctk.CTkLabel(aba_transacao, text="Excluir transação")
        self.label_excluir.pack(pady=(10, 5))

        self.menu_transacoes = ctk.CTkOptionMenu(aba_transacao, values=["Nenhuma transação"])
        self.menu_transacoes.pack(pady=(5, 10))

        self.botao_excluirTransacao = ctk.CTkButton(aba_transacao, text="Excluir Selecionada", hover_color="red",
                                                      command=self.excluir_transacao)
        self.botao_excluirTransacao.pack(pady=(0, 20))

        self.atualizar_menu_categorias()
        self.atualizar_menu_contas()
        self.atualizar_menu_transacoes()

    def atualizar_menu_transacoes(self):
        # guarda a lista para saber qual codTransacao corresponde ao texto escolhido
        self.transacoes_disponiveis = self.repo_transacoes.listar()
        textos = []
        for t in self.transacoes_disponiveis:
            categoria = self.repo_categorias.buscar(t.codCategoria)
            textos.append(f"#{t.codTransacao} | {t.data} | {categoria.descricao} | {t.DebitoCredito} | R$ {t.valor:.2f}")
        self.textos_transacoes = textos or ["Nenhuma transação"]
        self.menu_transacoes.configure(values=self.textos_transacoes)
        self.menu_transacoes.set(self.textos_transacoes[0])

    def excluir_transacao(self):
        if not self.transacoes_disponiveis:
            return
        indice = self.textos_transacoes.index(self.menu_transacoes.get())
        codigo = self.transacoes_disponiveis[indice].codTransacao
        self.repo_transacoes.excluir(codigo)
        self.atualizar_menu_transacoes()
        self.atualizar_saldo_geral()

    def atualizar_menu_categorias(self):
        self.categorias_disponiveis = self.repo_categorias.listar()
        valores = [c.descricao for c in self.categorias_disponiveis] or ["Cadastre uma categoria"]
        self.menu_categoria.configure(values=valores)
        self.menu_categoria.set(valores[0])

    def atualizar_menu_contas(self):
        self.contas_disponiveis = self.repo_contas.listar()
        valores = [c.descricao for c in self.contas_disponiveis] or ["Cadastre uma conta"]
        self.menu_conta.configure(values=valores)
        self.menu_conta.set(valores[0])

    def salvar_transacao(self):
        data = self.campo_dataTrasacao.get().strip()
        if not data or not self.categorias_disponiveis or not self.contas_disponiveis:
            self.label_erroTransacao.configure(text="Preencha todos os campos.")
            return
        try:
            valor = float(self.campo_valorTrasacao.get())
        except ValueError:
            self.label_erroTransacao.configure(text="Valor inválido.")
            return
        if valor < 0:
            self.label_erroTransacao.configure(text="O valor não pode ser negativo.")
            return

        categoria = next((c for c in self.categorias_disponiveis if c.descricao == self.menu_categoria.get()), None)
        conta = next((c for c in self.contas_disponiveis if c.descricao == self.menu_conta.get()), None)
        if categoria is None or conta is None:
            self.label_erroTransacao.configure(text="Selecione uma categoria e uma conta válidas.")
            return

        self.label_erroTransacao.configure(text="")
        tipo = "D" if self.menu_tipo.get() == "Debito" else "C"
        self.repo_transacoes.incluir(categoria.codigoCat, conta.codConta, data, valor, tipo)

        self.campo_dataTrasacao.delete(0, "end")
        self.campo_valorTrasacao.delete(0, "end")
        self.atualizar_menu_transacoes()
        self.atualizar_saldo_geral()

    def construir_abaRelatorios(self):
        aba_relatorios = self.janela_abas.tab("Relatórios")

        # extrato por período 
        self.label_extrato = ctk.CTkLabel(aba_relatorios, text="Extrato por período", font=ctk.CTkFont(weight="bold"))
        self.label_extrato.pack(pady=(15, 5))

        self.campo_dataInicial = ctk.CTkEntry(aba_relatorios, placeholder_text="Data inicial (AAAA-MM-DD)", width=300)
        self.campo_dataInicial.pack(pady=(5, 5))

        self.campo_dataFinal = ctk.CTkEntry(aba_relatorios, placeholder_text="Data final (AAAA-MM-DD)", width=300)
        self.campo_dataFinal.pack(pady=(5, 5))

        self.botao_buscarExtrato = ctk.CTkButton(aba_relatorios, text="Buscar", command=self.buscar_extrato)
        self.botao_buscarExtrato.pack(pady=(5, 10))

        self.texto_extrato = ctk.CTkTextbox(aba_relatorios, width=300, height=120)
        self.texto_extrato.pack(pady=(0, 5))
        self.texto_extrato.configure(state="disabled")

        self.label_saldoPeriodo = ctk.CTkLabel(aba_relatorios, text="Saldo do período: R$ 0.00")
        self.label_saldoPeriodo.pack(pady=(0, 20))

        # saldo de todas as contas + saldo geral
        self.label_saldos = ctk.CTkLabel(aba_relatorios, text="Saldo das contas", font=ctk.CTkFont(weight="bold"))
        self.label_saldos.pack(pady=(0, 5))

        self.texto_saldoGeral = ctk.CTkTextbox(aba_relatorios, width=300, height=100)
        self.texto_saldoGeral.pack(pady=(0, 5))
        self.texto_saldoGeral.configure(state="disabled")

        self.label_saldoGeral = ctk.CTkLabel(aba_relatorios, text="Saldo geral: R$ 0.00")
        self.label_saldoGeral.pack(pady=(0, 20))

        self.atualizar_saldo_geral()

    def buscar_extrato(self):
        data_ini = self.campo_dataInicial.get().strip()
        data_fim = self.campo_dataFinal.get().strip()
        transacoes, saldo_periodo = self.repo_transacoes.extrato_por_periodo(data_ini, data_fim)

        linhas = []
        for t in transacoes:
            categoria = self.repo_categorias.buscar(t.codCategoria)
            linhas.append(f"{t.data} | {categoria.descricao} | {t.DebitoCredito} | R$ {t.valor:.2f}")
        texto = "\n".join(linhas) if linhas else "Nenhuma transação no período."

        self.texto_extrato.configure(state="normal")
        self.texto_extrato.delete("1.0", "end")
        self.texto_extrato.insert("1.0", texto)
        self.texto_extrato.configure(state="disabled")

        self.label_saldoPeriodo.configure(text=f"Saldo do período: R$ {saldo_periodo:.2f}")

    def atualizar_saldo_geral(self):
        contas, total = self.repo_contas.saldo_geral()

        linhas = []
        for c in contas:
            banco = self.repo_bancos.buscar(c.codBanco)
            pessoa = self.repo_pessoas.buscar(c.codPessoa)
            linhas.append(f"{c.descricao} | {banco.descricao} | {pessoa.nome} | R$ {c.saldo:.2f}")
        texto = "\n".join(linhas) if linhas else "Nenhuma conta cadastrada."

        self.texto_saldoGeral.configure(state="normal")
        self.texto_saldoGeral.delete("1.0", "end")
        self.texto_saldoGeral.insert("1.0", texto)
        self.texto_saldoGeral.configure(state="disabled")

        self.label_saldoGeral.configure(text=f"Saldo geral: R$ {total:.2f}")
