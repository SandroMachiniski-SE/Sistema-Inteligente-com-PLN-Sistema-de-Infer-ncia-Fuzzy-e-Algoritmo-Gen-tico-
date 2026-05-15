import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import numpy as np

rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

class VisualizadorResultados:
    def __init__(self, caminho_dataset_fuzzy, caminho_ranking):
        self.df_fuzzy = pd.read_csv(caminho_dataset_fuzzy)
        self.ranking = pd.read_csv(caminho_ranking, index_col='destino')

    def gerar_relatorio_geral(self):
        print("\n" + "="*70)
        print("RELATORIO GERAL - ANALISE DE DESTINOS TURISTICOS")
        print("="*70)

        print(f"\nTotal de avaliacoes analisadas: {len(self.df_fuzzy)}")
        print(f"Total de destinos: {self.df_fuzzy['destino'].nunique()}")

        print("\n" + "-"*70)
        print("ESTATISTICAS GERAIS")
        print("-"*70)

        print(f"\nScore Fuzzy Medio Geral: {self.df_fuzzy['score_fuzzy'].mean():.2f}")
        print(f"Score Fuzzy Maximo: {self.df_fuzzy['score_fuzzy'].max():.2f}")
        print(f"Score Fuzzy Minimo: {self.df_fuzzy['score_fuzzy'].min():.2f}")

        print(f"\nSentimento Positivo Medio: {self.df_fuzzy['prob_positivo'].mean():.2%}")
        print(f"Preco Medio: R$ {self.df_fuzzy['preco_medio'].mean():.2f}")
        print(f"Distancia Media: {self.df_fuzzy['distancia_km'].mean():.0f} km")

        print("\n" + "-"*70)
        print("TOP 3 DESTINOS RECOMENDADOS")
        print("-"*70)

        top3 = self.ranking.head(3)
        for idx, (destino, row) in enumerate(top3.iterrows(), 1):
            print(f"\n{idx}. {destino}")
            print(f"   Score Medio: {row['score_medio']:.2f}")
            print(f"   Sentimento Positivo: {row['sentimento_medio']:.2%}")
            print(f"   Preco Medio: R$ {row['preco_medio']:.2f}")
            print(f"   Distancia: {row['distancia_km']:.0f} km")
            print(f"   Numero de Avaliacoes: {int(row['num_avaliacoes'])}")

    def gerar_grafico_ranking(self):
        fig, ax = plt.subplots(figsize=(12, 6))

        cores = ['#2ecc71' if score > 50 else '#f39c12' if score > 30 else '#e74c3c' 
                 for score in self.ranking['score_medio']]

        self.ranking['score_medio'].plot(kind='barh', ax=ax, color=cores, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Score de Recomendacao (0-100)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Destino', fontsize=12, fontweight='bold')
        ax.set_title('Ranking de Destinos Turisticos\nBaseado em Sentimento, Preco e Distancia', 
                     fontsize=14, fontweight='bold', pad=20)

        for i, v in enumerate(self.ranking['score_medio']):
            ax.text(v + 1, i, f'{v:.2f}', va='center', fontweight='bold')

        ax.set_xlim(0, 100)
        plt.tight_layout()
        plt.savefig('01_ranking_destinos.png', dpi=300, bbox_inches='tight')
        print("Grafico salvo: 01_ranking_destinos.png")
        plt.close()

    def gerar_grafico_sentimento_vs_score(self):
        fig, ax = plt.subplots(figsize=(12, 7))

        destinos = self.df_fuzzy['destino'].unique()
        cores_destinos = plt.cm.Set3(np.linspace(0, 1, len(destinos)))

        for destino, cor in zip(destinos, cores_destinos):
            dados = self.df_fuzzy[self.df_fuzzy['destino'] == destino]
            ax.scatter(dados['prob_positivo'], dados['score_fuzzy'], 
                      label=destino, s=100, alpha=0.7, edgecolors='black', linewidth=1)

        ax.set_xlabel('Probabilidade de Sentimento Positivo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score Fuzzy', fontsize=12, fontweight='bold')
        ax.set_title('Relacao entre Sentimento Positivo e Score de Recomendacao', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('02_sentimento_vs_score.png', dpi=300, bbox_inches='tight')
        print("Grafico salvo: 02_sentimento_vs_score.png")
        plt.close()

    def gerar_grafico_preco_vs_distancia(self):
        fig, ax = plt.subplots(figsize=(12, 7))

        destinos = self.df_fuzzy['destino'].unique()
        cores_destinos = plt.cm.Set3(np.linspace(0, 1, len(destinos)))

        for destino, cor in zip(destinos, cores_destinos):
            dados = self.df_fuzzy[self.df_fuzzy['destino'] == destino]
            ax.scatter(dados['preco_medio'], dados['distancia_km'], 
                      s=dados['score_fuzzy']*5, alpha=0.6, label=destino, 
                      edgecolors='black', linewidth=1, color=cor)

        ax.set_xlabel('Preco Medio (R$)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Distancia (km)', fontsize=12, fontweight='bold')
        ax.set_title('Preco vs Distancia\n(Tamanho das bolhas = Score Fuzzy)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('03_preco_vs_distancia.png', dpi=300, bbox_inches='tight')
        print("Grafico salvo: 03_preco_vs_distancia.png")
        plt.close()

    def gerar_grafico_distribuicao_scores(self):
        fig, ax = plt.subplots(figsize=(12, 7))

        destinos = self.df_fuzzy['destino'].unique()

        for destino in destinos:
            dados = self.df_fuzzy[self.df_fuzzy['destino'] == destino]['score_fuzzy']
            ax.hist(dados, alpha=0.6, label=destino, bins=15, edgecolor='black')

        ax.set_xlabel('Score Fuzzy', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequencia', fontsize=12, fontweight='bold')
        ax.set_title('Distribuicao de Scores Fuzzy por Destino', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig('04_distribuicao_scores.png', dpi=300, bbox_inches='tight')
        print("Grafico salvo: 04_distribuicao_scores.png")
        plt.close()

    def gerar_tabela_resumida(self):
        tabela = self.ranking.copy()
        tabela = tabela.round(2)
        tabela['preco_medio'] = tabela['preco_medio'].apply(lambda x: f'R$ {x:.2f}')
        tabela['distancia_km'] = tabela['distancia_km'].apply(lambda x: f'{int(x)} km')
        tabela['sentimento_medio'] = tabela['sentimento_medio'].apply(lambda x: f'{x:.1%}')
        tabela['num_avaliacoes'] = tabela['num_avaliacoes'].astype(int)

        tabela.columns = ['Score', 'Preco Medio', 'Distancia', 'Sentimento Positivo', 'Avaliacoes']

        tabela.to_csv('tabela_resumida.csv', encoding='utf-8')
        print("Tabela salva: tabela_resumida.csv")

        html = tabela.to_html()
        with open('tabela_resumida.html', 'w', encoding='utf-8') as f:
            f.write(f"""
            <html>
            <head>
                <meta charset="utf-8">
                <title>Ranking de Destinos Turisticos</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #4CAF50; color: white; }}
                    tr:nth-child(even) {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>Ranking de Destinos Turisticos</h1>
                <p>Analise baseada em Sentimento, Preco e Distancia</p>
                {html}
            </body>
            </html>
            """)
        print("Tabela salva: tabela_resumida.html")

    def gerar_todos_graficos(self):
        print("\n" + "="*70)
        print("GERANDO VISUALIZACOES E RELATORIOS")
        print("="*70)

        self.gerar_relatorio_geral()

        print("\n" + "-"*70)
        print("GERANDO GRAFICOS")
        print("-"*70 + "\n")

        self.gerar_grafico_ranking()
        self.gerar_grafico_sentimento_vs_score()
        self.gerar_grafico_preco_vs_distancia()
        self.gerar_grafico_distribuicao_scores()
        self.gerar_tabela_resumida()

        print("\n" + "="*70)
        print("VISUALIZACOES CONCLUIDAS COM SUCESSO!")
        print("="*70)
        print("\nArquivos gerados:")
        print("  - 01_ranking_destinos.png")
        print("  - 02_sentimento_vs_score.png")
        print("  - 03_preco_vs_distancia.png")
        print("  - 04_distribuicao_scores.png")
        print("  - tabela_resumida.csv")
        print("  - tabela_resumida.html")
        print("="*70 + "\n")

if __name__ == "__main__":
    visualizador = VisualizadorResultados('dataset_com_fuzzy.csv', 'ranking_destinos.csv')
    visualizador.gerar_todos_graficos()
