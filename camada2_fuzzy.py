import pandas as pd
import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz

# ============================================
# CAMADA II: LÓGICA FUZZY
# ============================================

class SistemaFuzzyTurismo:
    """
    Sistema de Inferência Fuzzy para recomendação de destinos turísticos.
    Combina sentimento (Naive Bayes), preço e distância para gerar score.
    """

    def __init__(self):
        self.sistema = None
        self.simulacao = None

    def criar_sistema_fuzzy(self):
        """
        Cria o sistema de inferência fuzzy com:
        - Entradas: sentimento_positivo, preco, distancia
        - Saída: score_recomendacao (0-100)
        """
        print("Criando sistema Fuzzy...")

        # ============================================
        # DEFINIR VARIÁVEIS DE ENTRADA
        # ============================================

        # 1. Sentimento Positivo (0-1, vem do Naive Bayes)
        sentimento = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'sentimento')
        sentimento['baixo'] = fuzz.trimf(sentimento.universe, [0, 0, 0.33])
        sentimento['medio'] = fuzz.trimf(sentimento.universe, [0.25, 0.5, 0.75])
        sentimento['alto'] = fuzz.trimf(sentimento.universe, [0.67, 1, 1])

        # 2. Preço (em reais, 0-3000)
        preco = ctrl.Antecedent(np.arange(0, 3001, 100), 'preco')
        preco['barato'] = fuzz.trimf(preco.universe, [0, 0, 1000])
        preco['moderado'] = fuzz.trimf(preco.universe, [800, 1500, 2200])
        preco['caro'] = fuzz.trimf(preco.universe, [2000, 3000, 3000])

        # 3. Distância (em km, 0-4000)
        distancia = ctrl.Antecedent(np.arange(0, 4001, 100), 'distancia')
        distancia['perto'] = fuzz.trimf(distancia.universe, [0, 0, 1000])
        distancia['medio'] = fuzz.trimf(distancia.universe, [800, 2000, 3200])
        distancia['longe'] = fuzz.trimf(distancia.universe, [3000, 4000, 4000])

        # ============================================
        # DEFINIR VARIÁVEL DE SAÍDA
        # ============================================

        # Score de Recomendação (0-100)
        score = ctrl.Consequent(np.arange(0, 101, 1), 'score')
        score['muito_baixo'] = fuzz.trimf(score.universe, [0, 0, 25])
        score['baixo'] = fuzz.trimf(score.universe, [15, 30, 45])
        score['medio'] = fuzz.trimf(score.universe, [40, 50, 60])
        score['alto'] = fuzz.trimf(score.universe, [55, 70, 85])
        score['muito_alto'] = fuzz.trimf(score.universe, [75, 100, 100])

        # ============================================
        # DEFINIR REGRAS FUZZY
        # ============================================

        regras = [
            # Sentimento alto é o mais importante
            ctrl.Rule(sentimento['alto'] & preco['barato'] & distancia['perto'], score['muito_alto']),
            ctrl.Rule(sentimento['alto'] & preco['barato'] & distancia['medio'], score['muito_alto']),
            ctrl.Rule(sentimento['alto'] & preco['barato'] & distancia['longe'], score['alto']),
            ctrl.Rule(sentimento['alto'] & preco['moderado'] & distancia['perto'], score['muito_alto']),
            ctrl.Rule(sentimento['alto'] & preco['moderado'] & distancia['medio'], score['alto']),
            ctrl.Rule(sentimento['alto'] & preco['moderado'] & distancia['longe'], score['medio']),
            ctrl.Rule(sentimento['alto'] & preco['caro'] & distancia['perto'], score['alto']),
            ctrl.Rule(sentimento['alto'] & preco['caro'] & distancia['medio'], score['medio']),
            ctrl.Rule(sentimento['alto'] & preco['caro'] & distancia['longe'], score['baixo']),

            # Sentimento médio
            ctrl.Rule(sentimento['medio'] & preco['barato'] & distancia['perto'], score['alto']),
            ctrl.Rule(sentimento['medio'] & preco['barato'] & distancia['medio'], score['alto']),
            ctrl.Rule(sentimento['medio'] & preco['barato'] & distancia['longe'], score['medio']),
            ctrl.Rule(sentimento['medio'] & preco['moderado'] & distancia['perto'], score['alto']),
            ctrl.Rule(sentimento['medio'] & preco['moderado'] & distancia['medio'], score['medio']),
            ctrl.Rule(sentimento['medio'] & preco['moderado'] & distancia['longe'], score['baixo']),
            ctrl.Rule(sentimento['medio'] & preco['caro'] & distancia['perto'], score['medio']),
            ctrl.Rule(sentimento['medio'] & preco['caro'] & distancia['medio'], score['baixo']),
            ctrl.Rule(sentimento['medio'] & preco['caro'] & distancia['longe'], score['muito_baixo']),

            # Sentimento baixo
            ctrl.Rule(sentimento['baixo'] & preco['barato'] & distancia['perto'], score['medio']),
            ctrl.Rule(sentimento['baixo'] & preco['barato'] & distancia['medio'], score['baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['barato'] & distancia['longe'], score['baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['moderado'] & distancia['perto'], score['baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['moderado'] & distancia['medio'], score['muito_baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['moderado'] & distancia['longe'], score['muito_baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['caro'] & distancia['perto'], score['muito_baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['caro'] & distancia['medio'], score['muito_baixo']),
            ctrl.Rule(sentimento['baixo'] & preco['caro'] & distancia['longe'], score['muito_baixo']),
        ]

        # Criar sistema de controle
        sistema_ctrl = ctrl.ControlSystem(regras)
        self.sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

        print("Sistema Fuzzy criado com sucesso!")
        return self.sistema

    def avaliar_destino(self, sentimento_positivo, preco, distancia):
        """
        Avalia um destino usando o sistema fuzzy.
        """
        if self.sistema is None:
            raise Exception("Sistema não foi criado. Execute criar_sistema_fuzzy() primeiro.")

        self.sistema.input['sentimento'] = sentimento_positivo
        self.sistema.input['preco'] = preco
        self.sistema.input['distancia'] = distancia

        self.sistema.compute()

        return self.sistema.output['score']

    def processar_dataset(self, caminho_csv):
        """
        Processa o dataset completo e adiciona scores fuzzy.
        """
        print("\nCarregando dataset com sentimentos...")
        df = pd.read_csv(caminho_csv)

        print("Calculando scores Fuzzy para cada avaliação...")
        scores = []

        for idx, row in df.iterrows():
            sentimento = row['prob_positivo']
            preco = row['preco_medio']
            distancia = row['distancia_km']

            score = self.avaliar_destino(sentimento, preco, distancia)
            scores.append(score)

        df['score_fuzzy'] = scores

        return df

    def gerar_ranking_destinos(self, df):
        """
        Gera ranking de destinos baseado no score fuzzy.
        """
        ranking = df.groupby('destino').agg({
            'score_fuzzy': 'mean',
            'preco_medio': 'mean',
            'distancia_km': 'first',
            'prob_positivo': 'mean',
            'avaliacao': 'count'
        }).round(2)

        ranking.columns = ['score_medio', 'preco_medio', 'distancia_km', 'sentimento_medio', 'num_avaliacoes']
        ranking = ranking.sort_values('score_medio', ascending=False)

        return ranking


if __name__ == "__main__":
    fuzzy_sistema = SistemaFuzzyTurismo()

    fuzzy_sistema.criar_sistema_fuzzy()

    df_fuzzy = fuzzy_sistema.processar_dataset('dataset_com_sentimentos.csv')

    df_fuzzy.to_csv('dataset_com_fuzzy.csv', index=False, encoding='utf-8')
    print("\nDataset com scores Fuzzy salvo como: dataset_com_fuzzy.csv")

    ranking = fuzzy_sistema.gerar_ranking_destinos(df_fuzzy)

    print("\n=== RANKING DE DESTINOS ===")
    print(ranking)

    ranking.to_csv('ranking_destinos.csv', encoding='utf-8')
    print("\nRanking salvo como: ranking_destinos.csv")

    print("\n=== EXEMPLOS DE AVALIAÇÕES COM SCORES FUZZY ===")
    exemplos = df_fuzzy.head(15)[['destino', 'avaliacao', 'prob_positivo', 'preco_medio', 'distancia_km', 'score_fuzzy']]
    print(exemplos.to_string())
