import configparser
import os

#---------------------------------------------------------------------------
# MÓDULO DE GERENCIAMENTO DO ARQUIVO .INI
#---------------------------------------------------------------------------
# Esta parte do código é responsável por gerenciar as configurações da aplicação
# usando um arquivo .ini. Ele lê, salva e limpa as configurações armazenadas
# nesse arquivo. Assim, conseguimos manter e recuperar as preferências do usuário
# e outras configurações sem precisar mexer no código toda hora.
#---------------------------------------------------------------------------



class GerenciadorConfig:
    def __init__(self, nome_arquivo='configuracoes.ini'):
        self.config = configparser.ConfigParser()
        self.nome_arquivo = nome_arquivo
        self.carregar_config()

#---------------------------------------------------------------------------
# RETORA TODOS ITENS DO .INI
#---------------------------------------------------------------------------

    def carregar_config(self):
        if os.path.exists(self.nome_arquivo):
            self.config.read(self.nome_arquivo)
            return {section: dict(self.config.items(section)) for section in self.config.sections()}
        else:
            return {}
        

#---------------------------------------------------------------------------
# SALVAR NO .INI
#---------------------------------------------------------------------------

    def salvar_config(self, configuracoes):
        if not self.config.has_section('configuracoes'):
            self.config.add_section('configuracoes')
        self.config.remove_section('configuracoes')
        self.config.add_section('configuracoes')

        for chave, valor in configuracoes.items():
            self.config.set('configuracoes', chave, str(valor))
        with open(self.nome_arquivo, 'w') as arquivo:
            self.config.write(arquivo)


#---------------------------------------------------------------------------
# LIMPAR E REMOVER O .INI
#---------------------------------------------------------------------------

    def limpar_config(self):
        if os.path.exists(self.nome_arquivo):
            os.remove(self.nome_arquivo)
        self.carregar_config()

