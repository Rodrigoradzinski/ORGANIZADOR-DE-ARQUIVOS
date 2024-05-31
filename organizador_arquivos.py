import os
import shutil

def organizar_arquivos(caminhos,
                        usar_extensao,
                        excecoes_extensoes,
                        excecoes_nomes_arquivos,
                        habilitar_renomear,
                        esquema_renomear,
                        apenas_renomear,
                        apenas_organizar
                        ):
    #print('apenas_renomear',apenas_renomear)
    #print('apenas_organizar',apenas_organizar)
    for caminho in caminhos.split(';'):
        if not os.path.exists(caminho):
            print(f"Caminho não encontrado: {caminho}")
            continue
        for arquivo in os.listdir(caminho):
            arquivo_completo = os.path.join(caminho, arquivo)
            if not os.path.isfile(arquivo_completo):
                continue

            nome, extensao = os.path.splitext(arquivo)

            if nome.lower() in [n.lower() for n in excecoes_nomes_arquivos] or extensao in excecoes_extensoes:
                print(f"Ignorando arquivo: {arquivo}")
                continue
        
            
            novo_nome = nome
            if habilitar_renomear and (apenas_renomear or not apenas_organizar):
                # Aplicar renomeação
                if esquema_renomear == '1maiuscula':
                    novo_nome = nome.capitalize()
                elif esquema_renomear == 'todasmaiusculas':
                    novo_nome = nome.upper()
                elif esquema_renomear == 'todasminusculas':
                    novo_nome = nome.lower()
            novo_nome += extensao

            if usar_extensao and (apenas_organizar or not apenas_renomear):
                destino_final = os.path.join(caminho, extensao.lstrip('.').lower(), novo_nome)
                os.makedirs(os.path.join(caminho, extensao.lstrip('.').lower()), exist_ok=True)
            else:
                destino_final = os.path.join(caminho, novo_nome)

            if arquivo_completo != destino_final:
                shutil.move(arquivo_completo, destino_final)
                print(f"Arquivo {arquivo} movido para {destino_final}")
