import pandas as pd
import joblib
import os 
from sklearn import model_selection, preprocessing, pipeline, linear_model, metrics

# carregar dados

def carregar_dados(caminho_arquivo = "historicoAcademico.csv"):

    try:
        if os.path.exists(caminho_arquivo):

            df = pd.read_csv(caminho_arquivo, encoding="latin1", sep=",")

            print("O arquivo foi carregado com sucesso!")

            return df
        
        else:

            print("O arquivo não foi encontrado dentro da pasta!")

            return None
        
    except Exception as e:

        print("Erro inesperado ao carregar o arquivo: ", e)

        return None


dados = carregar_dados()


#------ etapa 2, preparação e divisao dos dados
# definição de x (features )e y (target), 

if dados is not None:

    print(f"\nTotal de registros carregados: {len(dados)}")
    print("iniciando o pipeline de treinamento...")

    target_columm = "Status_Final" 

    try:
        x = dados.drop(target_columm, axis=1)
        y = dados[target_columm]

        print(f"features (x definidas: {list(x.columns)})")
        print(f"target (y) definida: {target_columm}")

    except KeyError:
        print("---------ERRO CRITICO---------")
        print(f"\n a coluna {target_columm} não foi encontrada no csv.")
        print(f"Colunas disponiveis: {list(dados.columns)}")
        print(f"Por favor, ajuste a variavel 'target_columm' e tente novamente!.")
        # se o alvo não for encontrado, encerra o programa
        exit()


    print("\n----------Dividindo os dados em treino e teste...----------")
    x_treino, x_teste, y_treino, y_teste = model_selection.train_test_split(
        x, y, 
        test_size=0.2,  #20% para teste                                                                    
        random_state=42,# garante a reprodutibilidade dos resultados
        stratify = y    # garante que a distribuição das classes seja mantida
    )
    print(f"Registros de treino: {len(x_treino)} | Registros de teste: {len(x_teste)}")
    
    #------ etapa 3, criação do pipeline de treinamento

    print("\n----------Criando o pipeline de treinamento...----------")
    pipeline_modelo = pipeline.Pipeline([
        ('scaler', preprocessing.StandardScaler()),#normalização dos dados
        ('model', linear_model.LogisticRegression(random_state=42))# aplica o modelo de regração logistica
    ])

    #------ etapa 4, treinamento e avaliação dos dados
    print("\n----------Treinamento do modelo...---------------------")

    pipeline_modelo.fit(x_treino, y_treino)

    print("Modelo treinado, avaliando com os dados de teste...")

    y_pred = pipeline_modelo.predict(x_teste)

    
    #avaliação de desempenho
    accuracy = metrics.accuracy_score(y_teste, y_pred)
    report = metrics.classification_report(y_teste, y_pred)
    print("------------Relatorio de avaliação geral-----------------")
    print(f"Acurácia: {accuracy * 100:.2f}%\n")
    print("Relatório de Classificação Detalhado:\n", report)


    #------ etapa 5, salvando o modelo

    model_filename = "modelo_treinado.joblib"

    print(f"\n Salvando o modelo criado em... {model_filename}")
    joblib.dump(pipeline_modelo, model_filename)

    print("processo concluído com sucesso!")
    print(f"O arquivo {model_filename} esta pronto para ser utilizado.")

else:
    print("O processo de treinamento foi interrompido devido a falha no carregamento dos dados.")