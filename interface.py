import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gerenciador_config import GerenciadorConfig
from organizador_arquivos import organizar_arquivos
import ast 
import sys



class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Organizador de Arquivos')
        self.master.geometry("1280x920")
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, 'organize.ico')
        else:
            icon_path = 'organize.ico'

        self.master.iconbitmap(icon_path)
        self.config_manager = GerenciadorConfig()
        self.excecoes_nomes_arquivos = []
        self.lista_caminhos = []
        self.extensoes_disponiveis = [
                    '.exe', '.pdf', '.jpg', '.png', '.txt', '.docx', '.xlsx', '.pptx', '.zip', '.rar', '.tar', '.gz', 
                    '.mp4', '.mp3', '.wav', '.avi', '.mov', '.html', '.css', '.js', '.py', '.java', '.cpp', '.c', '.h', 
                    '.json', '.xml', '.csv', '.ppt', '.xls', '.svg', '.bmp', '.gif', '.tiff', '.psd', '.eps', '.ai', 
                    '.indd', '.flv', '.mkv', '.wmv', '.ogg', '.3gp', '.m4a', '.mid', '.midi', '.flac', '.aac', '.rtf', 
                    '.odt', '.ods', '.odp', '.odg', '.otp', '.ots', '.ott', '.pem', '.pfx', '.cer', '.der', '.p7b', 
                    '.p7c', '.ppk', '.pub', '.crt', '.key', '.log', '.bak', '.tmp', '.sh', '.bat', '.cmd', '.ps1', 
                    '.vbs', '.jse', '.wsf', '.icon'
                ]
        self.extensoes_adicionais = []  
        self.interface_grafica()
        self.carregar_configuracoes()

        #pyinstaller --onefile --windowed --icon=organize.ico --name=organize --add-data "organize.ico;." main.py

        #------------------------------------------------------------------------
        # LISTA E CAMINHOS
        #------------------------------------------------------------------------

    def interface_grafica(self):
        self.frame_config = tk.LabelFrame(self.master, text="Configurações Gerais", padx=10, pady=10)
        self.frame_config.pack(fill="both", expand="yes", padx=20, pady=30)

        #------------------------------------------------------------------------
        # LISTA E CAMINHOS
        #------------------------------------------------------------------------
        self.lbl_novo_caminho = tk.Label(self.frame_config, text="Novo Caminho:")
        self.lbl_novo_caminho.grid(row=0, column=0, sticky='w')
        self.entry_novo_caminho = tk.Entry(self.frame_config, width=170)
        self.entry_novo_caminho.grid(row=0, column=1, sticky='we')
        self.btn_adicionar_caminho = tk.Button(self.frame_config, text="Adicionar Caminho", command=self.adicionar_caminho)
        self.btn_adicionar_caminho.grid(row=0, column=3, sticky='we')
        
        self.frame_lista_caminhos = tk.Frame(self.frame_config)
        self.frame_lista_caminhos.grid(row=1, column=0, columnspan=3, sticky='we')

        self.scrollbar = tk.Scrollbar(self.frame_lista_caminhos, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lst_caminhos = tk.Listbox(self.frame_lista_caminhos, selectmode=tk.MULTIPLE, width=150, height=5, yscrollcommand=self.scrollbar.set)
        self.lst_caminhos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.lst_caminhos.yview)

        self.lst_caminhos.bind('<Delete>', self.remover_caminhos_selecionados)
       #------------------------------------------------------------------------
        # OPÇOES DE ORGANIZACAO 
        #------------------------------------------------------------------------
        self.frame_organizacao = tk.LabelFrame(self.master, text="Organizar Arquivos e agrupar por", padx=10, pady=10)
        self.frame_organizacao.pack(fill="both", expand="yes", padx=20, pady=10)

        self.frame_agrupar_extensoes = tk.LabelFrame(self.frame_organizacao, text="Agrupar por Extensões", padx=10, pady=10)
        self.frame_agrupar_extensoes.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        self.chk_agrupar_extensoes_var = tk.BooleanVar()
        self.chk_agrupar_extensoes = tk.Checkbutton(self.frame_agrupar_extensoes, text="Agrupar por Extensões", variable=self.chk_agrupar_extensoes_var)
        self.chk_agrupar_extensoes.grid(row=0, column=0, sticky='w')

        self.frame_excecoes = tk.Frame(self.frame_agrupar_extensoes)
        self.frame_excecoes.grid(row=1, column=0, padx=10, pady=10)


        #------------------------------------------------------------------------
        # EXCEÇOES EXTENÇOES
        #------------------------------------------------------------------------

        self.frame_organizacao_extensoes = tk.LabelFrame(self.frame_excecoes, text="Exceções de Extensões", padx=10, pady=10)
        self.frame_organizacao_extensoes.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        self.opcoes_extensoes = {}
        self.carregar_extensoes_disponiveis()


        #------------------------------------------------------------------------
        # novas EXCEÇOES EXTENÇOES
        #------------------------------------------------------------------------
        self.Novas_extensoes = tk.LabelFrame(self.master, text="Novas Extensões", padx=10, pady=10)
        self.Novas_extensoes.pack(fill="both", expand="yes", padx=20, pady=10)
        self.lbl_nova_extensao = tk.Label(self.Novas_extensoes, text="Nova Extensão:")
        self.lbl_nova_extensao.grid(row=2, column=0, sticky='w')
        self.entry_nova_extensao = tk.Entry(self.Novas_extensoes, width=18)
        self.entry_nova_extensao.grid(row=2, column=1, sticky='w')
        self.btn_adicionar_extensao = tk.Button(self.Novas_extensoes, text="Adicionar Extensão", command=self.adicionar_extensao)
        self.btn_adicionar_extensao.grid(row=2, column=2, sticky='w')

        #------------------------------------------------------------------------
        # EXCEÇOES NOMES DE ARQUIVOS
        #------------------------------------------------------------------------
        self.frame_organizacao_nomes = tk.LabelFrame(self.frame_excecoes, text="Exceções de Nomes de Arquivos", padx=10, pady=10)
        self.frame_organizacao_nomes.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        self.lbl_excecoes_nomes_arquivos = tk.Label(self.frame_organizacao_nomes, text="Exceções de nomes de arquivos:")
        self.lbl_excecoes_nomes_arquivos.grid(row=0, column=0, sticky='w')

        self.entry_excecoes_nomes_arquivos = tk.Entry(self.frame_organizacao_nomes, width=50)
        self.entry_excecoes_nomes_arquivos.grid(row=1, column=0, sticky='we')

        self.btn_adicionar_excecao = tk.Button(self.frame_organizacao_nomes, text="Adicionar Exceção", command=self.adicionar_excecao_nome_arquivo)
        self.btn_adicionar_excecao.grid(row=1, column=1, sticky='w')

        self.lista_excecoes_nomes_arquivos = tk.Listbox(self.frame_organizacao_nomes, selectmode=tk.MULTIPLE, width=50)
        self.lista_excecoes_nomes_arquivos.grid(row=2, column=0, columnspan=2, sticky='we')

        self.lista_excecoes_nomes_arquivos.bind('<Delete>', self.remover_nomes_arquivos_selecionados)
        #------------------------------------------------------------------------
        # RENOMEAR ARQUIVOS
        #------------------------------------------------------------------------
        self.frame_renomear_arquivos = tk.LabelFrame(self.frame_organizacao, text="Renomear Arquivos", padx=10, pady=10)
        self.frame_renomear_arquivos.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        self.renomear_var = tk.BooleanVar()
        self.chk_renomear = tk.Checkbutton(self.frame_renomear_arquivos, text="Habilitar Renomeação", variable=self.renomear_var)
        self.chk_renomear.grid(row=0, column=0, sticky='w')

        self.renomear_opcoes = tk.StringVar()
        self.radio_1_maiuscula = tk.Radiobutton(self.frame_renomear_arquivos, text="1 Maiúscula", variable=self.renomear_opcoes, value='1maiuscula')
        self.radio_1_maiuscula.grid(row=1, column=0, sticky='w')
        self.radio_todas_maiusculas = tk.Radiobutton(self.frame_renomear_arquivos, text="Todas Maiúsculas", variable=self.renomear_opcoes, value='todasmaiusculas')
        self.radio_todas_maiusculas.grid(row=2, column=0, sticky='w')
        self.radio_todas_minusculas = tk.Radiobutton(self.frame_renomear_arquivos, text="Todas Minúsculas", variable=self.renomear_opcoes, value='todasminusculas')
        self.radio_todas_minusculas.grid(row=3, column=0, sticky='w')
     

        #------------------------------------------------------------------------
        # check para escolher entre renomear ou orgnaizar 
        #------------------------------------------------------------------------

        self.chk_apenar_renomear_var = tk.BooleanVar()
        self.chk_apenar_renomear = tk.Checkbutton(self.frame_organizacao, text="Apenas padronizar Nomes", variable=self.chk_apenar_renomear_var)
        self.chk_apenar_renomear.grid(row=3, column=0, sticky='w')

        self.chk_apenas_organizar_var = tk.BooleanVar()
        self.chk_apenas_organizar = tk.Checkbutton(self.frame_organizacao, text="Apenas Agrupar em Pastas", variable=self.chk_apenas_organizar_var)
        self.chk_apenas_organizar.grid(row=4, column=0, sticky='w')
        

        #------------------------------------------------------------------------
        # CRIANDO FRAME PARA BOTOES E ACOES 
        #------------------------------------------------------------------------
        
        self.frame_acoes = tk.Frame(self.master, padx=10, pady=10)
        self.frame_acoes.pack(fill="both", expand="yes", padx=20, pady=10)

        #------------------------------------------------------------------------
        # BOTOTES SALVAR 
        #------------------------------------------------------------------------
        self.btn_salvar_config = tk.Button(self.frame_acoes, text="Salvar Configurações", command=self.salvar_configuracoes)
        self.btn_salvar_config.pack(side=tk.LEFT, padx=5)
        #------------------------------------------------------------------------
        # BOTAo ORGNANIZAR ARQUIVOS E RONOME
        #------------------------------------------------------------------------
        self.btn_organizar_arquivos = tk.Button(self.frame_acoes, text="Organizar Arquivos", command=self.executar_organizacao)
        self.btn_organizar_arquivos.pack(side=tk.LEFT, padx=5)
        #------------------------------------------------------------------------
        # BOTOTES LIMPAR CONFIG 
        #------------------------------------------------------------------------
        
        self.btn_limpar_interface = tk.Button(self.frame_acoes, text="Limpar Interface", command=self.limpar_interface)
        self.btn_limpar_interface.pack(side=tk.LEFT, padx=5)

   
    def carregar_extensoes_disponiveis(self):
            for idx, extensao in enumerate(self.extensoes_disponiveis + self.extensoes_adicionais):
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self.frame_organizacao_extensoes, text=extensao, variable=var)
                checkbutton.grid(row=1 + idx % 10, column=idx // 10, sticky='w')
                self.opcoes_extensoes[extensao] = var

    def adicionar_extensao(self):
            nova_extensao = self.entry_nova_extensao.get().strip()
            if nova_extensao and nova_extensao not in self.extensoes_disponiveis + self.extensoes_adicionais:
                self.extensoes_adicionais.append(nova_extensao)
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self.frame_organizacao_extensoes, text=nova_extensao, variable=var)
                checkbutton.grid(row=1 + len(self.extensoes_disponiveis) + len(self.extensoes_adicionais) % 10, column=(len(self.extensoes_disponiveis) + len(self.extensoes_adicionais)) // 10, sticky='w')
                self.opcoes_extensoes[nova_extensao] = var
                self.entry_nova_extensao.delete(0, tk.END)
#------------------------------------------------------------------------
# FUNCAO APRA CARREGAR AS CONFIGURACOES  QUANDO O APP ABRE
#------------------------------------------------------------------------
    def carregar_configuracoes(self):
        config = self.config_manager.carregar_config()
        config = config.get('configuracoes', {})

        self.chk_agrupar_extensoes_var.set(config.get('agrupar_por_extensoes', 'False') == 'True')
        self.renomear_var.set(config.get('renomear_arquivos', 'False') == 'True')
        self.renomear_opcoes.set('1maiuscula' if config.get('1maiuscula', 'False') == 'True' else 'todasmaiusculas' if config.get('todasmaiusculas', 'False') == 'True' else 'todasminusculas')

        self.chk_apenar_renomear_var.set(config.get('apenas_renomear', 'False') == 'True')
        self.chk_apenas_organizar_var.set(config.get('apenas_organizar', 'False') == 'True')

        if 'caminhos' in config and config['caminhos'] != '[]':
            caminhos = config['caminhos'].strip('[]').replace("'", "").split(', ')
            for path in caminhos:
                if path:
                    self.lista_caminhos.append(path)
                    self.lst_caminhos.insert(tk.END, path)

        if 'excecoes_extensoes' in config and config['excecoes_extensoes'] != '[]':
            excecoes = config['excecoes_extensoes'].strip('[]').replace("'", "").split(', ')
            for ext in excecoes:
                if ext in self.opcoes_extensoes:
                    self.opcoes_extensoes[ext].set(True)

        if 'excecoes_nomes_arquivos' in config and config['excecoes_nomes_arquivos'] != '[]':
            nomes = config['excecoes_nomes_arquivos'].strip('[]').replace("'", "").split(', ')
            self.excecoes_nomes_arquivos.extend(nomes)
            for nome in nomes:
                self.lista_excecoes_nomes_arquivos.insert(tk.END, nome)

        if 'extensoes_adicionais' in config and config['extensoes_adicionais'] != '[]':
            extensoes_adicionais = config['extensoes_adicionais'].strip('[]').replace("'", "").split(', ')
            self.extensoes_adicionais.extend(extensoes_adicionais)
            self.carregar_extensoes_disponiveis()

#---------------------------------------------------------------------------
# FUNCAO PARA  CARREGAR AS CONFIGURACOES  QUANDO O CLCIAR NO BOTAO ORGANIZAR
#---------------------------------------------------------------------------
    
    def carregar_configuracoes_organizacao(self):
        config = self.config_manager.carregar_config().get('configuracoes', {})
        print("Configurações carregadas:", config)
        caminhos_raw = config.get('caminhos', '[]')
        if caminhos_raw:
            self.lista_caminhos = ast.literal_eval(caminhos_raw)
            self.lista_caminhos = [caminho.strip() for caminho in self.lista_caminhos if caminho.strip()]

        excecoes_extensoes_raw = config.get('excecoes_extensoes', '[]')
        if excecoes_extensoes_raw:
            self.excecoes_extensoes = ast.literal_eval(excecoes_extensoes_raw)
            self.excecoes_extensoes = [ext.strip() for ext in self.excecoes_extensoes if ext.strip()]

        excecoes_nomes_arquivos_raw = config.get('excecoes_nomes_arquivos', '[]')
        if excecoes_nomes_arquivos_raw:
            self.excecoes_nomes_arquivos = ast.literal_eval(excecoes_nomes_arquivos_raw)
            self.excecoes_nomes_arquivos = [nome.strip() for nome in self.excecoes_nomes_arquivos if nome.strip()]

        self.renomear_var.set(config.get('renomear_arquivos', 'False') == 'True')
        esquema_renomeacao = '1maiuscula' if config.get('1maiuscula', 'False') == 'True' else 'todasmaiusculas' if config.get('todasmaiusculas', 'False') == 'True' else 'todasminusculas'

        self.chk_apenar_renomear_var.set(config.get('apenas_renomear', 'False') == 'True')
        self.chk_apenas_organizar_var.set(config.get('apenas_organizar', 'False') == 'True')

        self.renomear_opcoes.set(esquema_renomeacao)

        for caminho in self.lista_caminhos:
            if not os.path.exists(caminho):
                print(f"Caminho não encontrado: {caminho}")



#---------------------------------------------------------------------------
# AQUI  SALVO AS CONFIGURACOES ATUAIS E CHAMO O METODO DE ORGANIZACAO
#---------------------------------------------------------------------------

    def executar_organizacao(self):
        self.salvar_configuracoes()
        self.carregar_configuracoes_organizacao()  
        organizar_arquivos(
            caminhos=';'.join(self.lista_caminhos),
            usar_extensao=self.chk_agrupar_extensoes_var.get(),
            excecoes_extensoes=self.excecoes_extensoes,
            excecoes_nomes_arquivos=self.excecoes_nomes_arquivos,
            habilitar_renomear=self.renomear_var.get(),
            esquema_renomear=self.renomear_opcoes.get(),
            apenas_renomear =self.chk_apenar_renomear_var.get(),
            apenas_organizar =self.chk_apenas_organizar_var.get()
        )
        messagebox.showinfo("Organização Completa", "Os arquivos foram organizados com sucesso!")




#---------------------------------------------------------------------------
# FUNCAO PARA ADICIONAR OS O NOMES NA LITA DE EXCECOES 
#---------------------------------------------------------------------------

    def adicionar_excecao_nome_arquivo(self):
        nome_arquivo = self.entry_excecoes_nomes_arquivos.get()
        if nome_arquivo:
            self.excecoes_nomes_arquivos.append(nome_arquivo)
            self.lista_excecoes_nomes_arquivos.insert(tk.END, nome_arquivo)
            #messagebox.showinfo("Adicionado", f"O arquivo '{nome_arquivo}' foi adicionado à lista de exceções.")
            self.entry_excecoes_nomes_arquivos.delete(0, tk.END)


#---------------------------------------------------------------------------
# SALVAR AS CONFIG  NO ARUQIVO .INI
#---------------------------------------------------------------------------

    def salvar_configuracoes(self):
        lista_caminhos = self.lista_caminhos
        excecoes_extensoes = [ext for ext, var in self.opcoes_extensoes.items() if var.get()]
        excecoes_nomes_arquivos = self.excecoes_nomes_arquivos

        configuracoes = {
            'caminhos': lista_caminhos,
            'agrupar_por_extensoes': self.chk_agrupar_extensoes_var.get(),
            'excecoes_extensoes': excecoes_extensoes,
            'excecoes_nomes_arquivos': excecoes_nomes_arquivos,
            'renomear_arquivos': self.renomear_var.get(),
            '1maiuscula': self.renomear_opcoes.get() == '1maiuscula',
            'todasmaiusculas': self.renomear_opcoes.get() == 'todasmaiusculas',
            'todasminusculas': self.renomear_opcoes.get() == 'todasminusculas',
            'apenas_renomear': self.chk_apenar_renomear_var.get(),
            'apenas_organizar': self.chk_apenas_organizar_var.get(),
            'extensoes_adicionais': self.extensoes_adicionais
        }

        self.config_manager.salvar_config(configuracoes)
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")


#---------------------------------------------------------------------------
# FUNCAO PARA ADICIONARO OS CAMINHOS NA LISTA DE CAMINHOS
#---------------------------------------------------------------------------

    def adicionar_caminho(self):
        path = filedialog.askdirectory()
        if path:
            self.lista_caminhos.append(path) 
            self.lst_caminhos.insert(tk.END, path)


#---------------------------------------------------------------------------
# BOTAO LIMPAR TUDO E ZERAR O .INI
#---------------------------------------------------------------------------
    def limpar_interface(self):
    
        self.chk_agrupar_extensoes_var.set(False)
        self.renomear_var.set(False)
        self.chk_apenar_renomear_var.set(False)
        self.chk_apenas_organizar_var.set(False)
        self.renomear_opcoes.set('')

        # Limpar listas e entradas
        self.lista_caminhos.clear()
        self.lst_caminhos.delete(0, tk.END)
        self.excecoes_nomes_arquivos.clear()
        self.lista_excecoes_nomes_arquivos.delete(0, tk.END)
        self.entry_excecoes_nomes_arquivos.delete(0, tk.END)
        self.config_manager.limpar_config()
        
        for var in self.opcoes_extensoes.values():
            var.set(False)

        messagebox.showinfo("Limpeza", "Interface limpa com sucesso!")

    

#---------------------------------------------------------------------------
# FUNCAO APRA CHAMAR ATRAVES DO DELETA O ITENS SELECIONAS
#---------------------------------------------------------------------------

    def remover_caminhos_selecionados(self, event):
        indices_selecionados = self.lst_caminhos.curselection()
        for i in reversed(indices_selecionados):
            self.lista_caminhos.pop(i)
            self.lst_caminhos.delete(i)

    def remover_nomes_arquivos_selecionados(self, event):
        indices_selecionados = self.lista_excecoes_nomes_arquivos.curselection()
        indices_a_remover = list(indices_selecionados)
        for i in reversed(indices_a_remover):
            self.excecoes_nomes_arquivos.pop(i)
            self.lista_excecoes_nomes_arquivos.delete(i)



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()