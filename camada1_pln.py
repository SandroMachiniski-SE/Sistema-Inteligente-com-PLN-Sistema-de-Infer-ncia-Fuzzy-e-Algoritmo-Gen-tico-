import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import re

# Baixar recursos necessários do NLTK (execute uma única vez)
nltk.download('stopwords')
nltk.download('punkt')

# ============================================
# CAMADA I: PLN + NAIVE BAYES
# ============================================

class AnalisadorSentimentoTurismo:
    """
    Classificador de sentimentos para avaliações de destinos turísticos
    usando PLN e Naive Bayes
    """

    def __init__(self):
        self.modelo = None
        self.vetorizador = None
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))

    def preprocessar_texto(self, texto):
        """
        Pré-processamento do texto:
        1. Converter para minúsculas
        2. Remover pontuação e caracteres especiais
        3. Tokenização
        4. Remover stop words
        5. Stemming
        """
        # Converter para minúsculas
        texto = texto.lower()

        # Remover pontuação e caracteres especiais
        texto = re.sub(r'[^a-záéíóúãõç\s]', '', texto)

        # Tokenização
        tokens = word_tokenize(texto)

        # Remover stop words e aplicar stemming
        tokens_processados = [
            self.stemmer.stem(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]

        return ' '.join(tokens_processados)

    def carregar_e_preparar_dados(self, caminho_csv):
        """
        Carrega o dataset e prepara os dados para treinamento
        """
        print("Carregando dataset...")
        df = pd.read_csv(caminho_csv)

        print("Pré-processando textos...")
        # Aplicar pré-processamento em todas as avaliações
        df['avaliacao_processada'] = df['avaliacao'].apply(self.preprocessar_texto)

        # Usar a coluna 'sentimento_real' como rótulo (já vem no dataset)
        X = df['avaliacao_processada']
        y = df['sentimento_real']

        return X, y, df

    def treinar_modelo(self, X, y):
        """
        Treina o modelo Naive Bayes com os dados
        """
        print("\nTreinando modelo...")

        # Dividir dados em treino (80%) e teste (20%)
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Vetorizar textos usando TF-IDF
        self.vetorizador = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        X_treino_vetorizado = self.vetorizador.fit_transform(X_treino)
        X_teste_vetorizado = self.vetorizador.transform(X_teste)

        # Treinar Naive Bayes
        self.modelo = MultinomialNB()
        self.modelo.fit(X_treino_vetorizado, y_treino)

        # Avaliar modelo
        y_pred = self.modelo.predict(X_teste_vetorizado)

        print("\n=== RESULTADOS DO TREINAMENTO ===")
        print(f"\nAcurácia: {self.modelo.score(X_teste_vetorizado, y_teste):.2%}")
        print("\nRelatório de Classificação:")
        print(classification_report(y_teste, y_pred, zero_division=0))

        return X_treino_vetorizado, X_teste_vetorizado, y_treino, y_teste

    def classificar_sentimento(self, texto):
        """
        Classifica o sentimento de um novo texto
        Retorna: (sentimento, probabilidades)
        """
        if self.modelo is None:
            raise Exception("Modelo não foi treinado. Execute treinar_modelo() primeiro.")

        # Pré-processar texto
        texto_processado = self.preprocessar_texto(texto)

        # Vetorizar
        texto_vetorizado = self.vetorizador.transform([texto_processado])

        # Predizer
        sentimento = self.modelo.predict(texto_vetorizado)[0]
        probabilidades = self.modelo.predict_proba(texto_vetorizado)[0]

        # Mapear probabilidades para cada classe
        classes = self.modelo.classes_
        prob_dict = {classe: prob for classe, prob in zip(classes, probabilidades)}

        return sentimento, prob_dict

    def processar_dataset_completo(self, df):
        """
        Processa todas as avaliações do dataset e retorna
        um dataframe com as classificações e probabilidades
        """
        print("\nClassificando todas as avaliações...")

        sentimentos = []
        probs_positivo = []
        probs_negativo = []
        probs_neutro = []

        for avaliacao in df['avaliacao']:
            sentimento, probs = self.classificar_sentimento(avaliacao)
            sentimentos.append(sentimento)
            probs_positivo.append(probs.get('positivo', 0))
            probs_negativo.append(probs.get('negativo', 0))
            probs_neutro.append(probs.get('neutro', 0))

        # Adicionar resultados ao dataframe
        df['sentimento_previsto'] = sentimentos
        df['prob_positivo'] = probs_positivo
        df['prob_negativo'] = probs_negativo
        df['prob_neutro'] = probs_neutro

        return df


# ============================================
# EXECUTAR CAMADA I
# ============================================

if __name__ == "__main__":
    # Criar instância do analisador
    analisador = AnalisadorSentimentoTurismo()

    # Carregar e preparar dados
    X, y, df = analisador.carregar_e_preparar_dados('dataset_destinos.csv')

    # Treinar modelo
    analisador.treinar_modelo(X, y)

    # Processar dataset completo
    df_resultado = analisador.processar_dataset_completo(df)

    # Salvar resultado
    df_resultado.to_csv('dataset_com_sentimentos.csv', index=False, encoding='utf-8')
    print("\nDataset com sentimentos salvo como: dataset_com_sentimentos.csv")

    # Mostrar exemplos
    print("\n=== EXEMPLOS DE CLASSIFICAÇÃO ===")
    exemplos = df_resultado.head(10)[['avaliacao', 'sentimento_real', 'sentimento_previsto', 'prob_positivo', 'prob_negativo', 'prob_neutro']]
    print(exemplos.to_string())

    # Testar com uma avaliação nova
    print("\n=== TESTE COM AVALIAÇÃO NOVA ===")
    teste_texto = "Lugar maravilhoso! Voltaria com certeza, mas foi um pouco caro."
    sentimento, probs = analisador.classificar_sentimento(teste_texto)
    print(f"Texto: {teste_texto}")
    print(f"Sentimento: {sentimento}")
    print(f"Probabilidades: {probs}")