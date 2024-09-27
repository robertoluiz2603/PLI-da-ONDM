import os
import gurobipy as gp
from gurobipy import GRB

def optimize_lp_files(directory, time_limit=50):
    otimizou = 0
    otimizou_mno = 0
    nao_otimizou = 0
    # Percorre todos os arquivos no diretório
    for filename in os.listdir(directory):
        if filename.endswith(".lp"):  # Verifica se o arquivo tem a extensão .lp
            filepath = os.path.join(directory, filename)
            try:
                # Cria o modelo Gurobi a partir do arquivo .lp
                model = gp.read(filepath)
                
                # Define o TimeLimit
                model.setParam(GRB.Param.TimeLimit, time_limit)
                
                # Otimiza o modelo
                model.optimize()

                # Verifica se a otimização foi bem-sucedida ou se atingiu o limite de tempo
                if model.Status == GRB.OPTIMAL:
                    print(f"Solução ótima encontrada para o arquivo: {filename}")
                    otimizou += 1
                elif model.Status == GRB.TIME_LIMIT:
                    print(f"Tempo limite atingido para o arquivo: {filename}. Solução atual pode ser subótima.")
                    otimizou_mno += 1
                    if model.solCount > 0:
                        for v in model.getVars():
                            print(f"{v.VarName} = {v.X}")
                        print(f"Uma solução factível foi encontrada para o arquivo: {filename}.")
                    else:
                        print(f"Nenhuma solução factível foi encontrada para o arquivo: {filename}.")
                        nao_otimizou += 1
                else:
                    print(f"Erro ao otimizar o arquivo: {filename} - Status: {model.Status}")
            except gp.GurobiError as e:
                print(f"Erro Gurobi ao processar o arquivo: {filename} - {str(e)}")
            except Exception as e:
                print(f"Erro inesperado ao processar o arquivo: {filename} - {str(e)}")
    print("Resultados finais: \n")
    print("Número de arquivos que tiveram a solução ótima: " + str(otimizou))
    print("Número de arquivos que tiveram uma solução, porém não ótima: " + str(otimizou_mno))
    print("Número de arquivos que não foi possível encontrar uma solução: "+ str(nao_otimizou))
# Exemplo de uso:
directory_path = "arquivos_otimizacao"
optimize_lp_files(directory_path)
