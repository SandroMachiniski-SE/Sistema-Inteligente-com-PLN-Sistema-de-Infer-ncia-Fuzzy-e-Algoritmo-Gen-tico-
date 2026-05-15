from flask import Flask, render_template_string, jsonify, request
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# ============================================
# CAMADA IV: INTERFACE WEB INTERATIVA
# ============================================

app = Flask(__name__)

# Carregar dados
df_fuzzy = pd.read_csv('dataset_com_fuzzy.csv')
ranking = pd.read_csv('ranking_destinos.csv', index_col='destino')

# ============================================
# TEMPLATE HTML
# ============================================

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Recomendação de Destinos Turísticos</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 50px;
        }

        .section h2 {
            color: #333;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .stat-card .value {
            font-size: 2.2em;
            font-weight: bold;
        }

        .chart-container {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }

        .ranking-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .ranking-table th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        .ranking-table td {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }

        .ranking-table tr:hover {
            background: #f8f9fa;
        }

        .ranking-table tr:nth-child(even) {
            background: #f8f9fa;
        }

        .badge {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .badge-gold {
            background: #ffd700;
            color: #333;
        }

        .badge-silver {
            background: #c0c0c0;
            color: #333;
        }

        .badge-bronze {
            background: #cd7f32;
            color: white;
        }

        .filter-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .filter-section label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }

        .filter-section input, .filter-section select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            margin-bottom: 15px;
        }

        .filter-section button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }

        .filter-section button:hover {
            background: #764ba2;
        }

        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }

        .destino-card {
            background: white;
            border: 2px solid #667eea;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }

        .destino-card:hover {
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
            transform: translateY(-5px);
        }

        .destino-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .destino-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }

        .destino-info-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }

        .destino-info-item strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Sistema de Recomendação de Destinos Turísticos</h1>
            <p>Análise inteligente baseada em Processamento de Linguagem Natural e Lógica Fuzzy</p>
        </div>

        <div class="content">
            <!-- SEÇÃO DE ESTATÍSTICAS -->
            <div class="section">
                <h2>📊 Estatísticas Gerais</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total de Avaliações</h3>
                        <div class="value" id="total-avaliacoes">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Destinos Analisados</h3>
                        <div class="value" id="total-destinos">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Score Médio</h3>
                        <div class="value" id="score-medio">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Sentimento Positivo Médio</h3>
                        <div class="value" id="sentimento-medio">0%</div>
                    </div>
                </div>
            </div>

            <!-- SEÇÃO DE RANKING -->
            <div class="section">
                <h2>🏆 Ranking de Destinos</h2>
                <div class="chart-container">
                    <div id="ranking-chart"></div>
                </div>

                <table class="ranking-table">
                    <thead>
                        <tr>
                            <th>Posição</th>
                            <th>Destino</th>
                            <th>Score</th>
                            <th>Sentimento</th>
                            <th>Preço Médio</th>
                            <th>Distância</th>
                            <th>Avaliações</th>
                        </tr>
                    </thead>
                    <tbody id="ranking-tbody">
                    </tbody>
                </table>
            </div>

            <!-- SEÇÃO DE GRÁFICOS -->
            <div class="section">
                <h2>📈 Análise Detalhada</h2>

                <h3 style="color: #667eea; margin-top: 30px; margin-bottom: 15px;">Sentimento vs Score Fuzzy</h3>
                <div class="chart-container">
                    <div id="sentimento-score-chart"></div>
                </div>

                <h3 style="color: #667eea; margin-top: 30px; margin-bottom: 15px;">Preço vs Distância</h3>
                <div class="chart-container">
                    <div id="preco-distancia-chart"></div>
                </div>

                <h3 style="color: #667eea; margin-top: 30px; margin-bottom: 15px;">Distribuição de Scores</h3>
                <div class="chart-container">
                    <div id="distribuicao-chart"></div>
                </div>
            </div>

            <!-- SEÇÃO DE FILTROS E BUSCA -->
            <div class="section">
                <h2>🔍 Filtrar Destinos</h2>
                <div class="filter-section">
                    <label for="filtro-destino">Buscar Destino:</label>
                    <input type="text" id="filtro-destino" placeholder="Digite o nome do destino...">

                    <label for="filtro-score">Score Mínimo:</label>
                    <input type="range" id="filtro-score" min="0" max="100" value="0">
                    <span id="score-valor">0</span>

                    <label for="filtro-preco">Preço Máximo (R$):</label>
                    <input type="range" id="filtro-preco" min="0" max="3000" value="3000" step="100">
                    <span id="preco-valor">R$ 3000</span>

                    <button onclick="aplicarFiltros()">Aplicar Filtros</button>
                </div>

                <div id="destinos-filtrados"></div>
            </div>
        </div>

        <div class="footer">
            <p>Sistema desenvolvido com Python, Flask, Plotly e Lógica Fuzzy</p>
            <p>© 2026 - Inteligência Artificial | Análise de Destinos Turísticos</p>
        </div>
    </div>

    <script>
        // Carregar dados
        fetch('/api/dados')
            .then(response => response.json())
            .then(data => {
                carregarEstatisticas(data);
                carregarRanking(data);
                carregarGraficos(data);
            });

        function carregarEstatisticas(data) {
            document.getElementById('total-avaliacoes').textContent = data.total_avaliacoes;
            document.getElementById('total-destinos').textContent = data.total_destinos;
            document.getElementById('score-medio').textContent = data.score_medio.toFixed(2);
            document.getElementById('sentimento-medio').textContent = (data.sentimento_medio * 100).toFixed(1) + '%';
        }

        function carregarRanking(data) {
            const tbody = document.getElementById('ranking-tbody');
            const ranking = data.ranking;

            ranking.forEach((item, index) => {
                const badges = ['badge-gold', 'badge-silver', 'badge-bronze'];
                const badge = index < 3 ? `<span class="badge ${badges[index]}">${index + 1}º</span>` : `<span>${index + 1}º</span>`;

                const row = `
                    <tr>
                        <td>${badge}</td>
                        <td><strong>${item.destino}</strong></td>
                        <td>${item.score_medio.toFixed(2)}</td>
                        <td>${(item.sentimento_medio * 100).toFixed(1)}%</td>
                        <td>R$ ${item.preco_medio.toFixed(2)}</td>
                        <td>${item.distancia_km.toFixed(0)} km</td>
                        <td>${item.num_avaliacoes}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }

        function carregarGraficos(data) {
            // Gráfico de Ranking
            const ranking = data.ranking;
            const destinos = ranking.map(r => r.destino);
            const scores = ranking.map(r => r.score_medio);

            const traceRanking = {
                x: scores,
                y: destinos,
                type: 'bar',
                orientation: 'h',
                marker: {
                    color: scores.map(s => s > 50 ? '#2ecc71' : s > 30 ? '#f39c12' : '#e74c3c')
                }
            };

            Plotly.newPlot('ranking-chart', [traceRanking], {
                title: 'Score de Recomendação por Destino',
                xaxis: { title: 'Score (0-100)' },
                margin: { l: 150 }
            });

            // Gráfico Sentimento vs Score
            const destinos_unicos = [...new Set(data.avaliacoes.map(a => a.destino))];
            const traces_sentimento = destinos_unicos.map(destino => {
                const dados = data.avaliacoes.filter(a => a.destino === destino);
                return {
                    x: dados.map(d => d.prob_positivo),
                    y: dados.map(d => d.score_fuzzy),
                    mode: 'markers',
                    name: destino,
                    marker: { size: 8 }
                };
            });

            Plotly.newPlot('sentimento-score-chart', traces_sentimento, {
                title: 'Sentimento Positivo vs Score Fuzzy',
                xaxis: { title: 'Probabilidade de Sentimento Positivo' },
                yaxis: { title: 'Score Fuzzy' }
            });

            // Gráfico Preço vs Distância
            const traces_preco = destinos_unicos.map(destino => {
                const dados = data.avaliacoes.filter(a => a.destino === destino);
                return {
                    x: dados.map(d => d.preco_medio),
                    y: dados.map(d => d.distancia_km),
                    mode: 'markers',
                    name: destino,
                    marker: { 
                        size: dados.map(d => d.score_fuzzy / 10),
                        opacity: 0.7
                    }
                };
            });

            Plotly.newPlot('preco-distancia-chart', traces_preco, {
                title: 'Preço vs Distância (tamanho = Score)',
                xaxis: { title: 'Preço Médio (R$)' },
                yaxis: { title: 'Distância (km)' }
            });

            // Gráfico Distribuição
            const traces_dist = destinos_unicos.map(destino => {
                const dados = data.avaliacoes.filter(a => a.destino === destino);
                return {
                    x: dados.map(d => d.score_fuzzy),
                    name: destino,
                    type: 'histogram',
                    nbinsx: 15,
                    opacity: 0.7
                };
            });

            Plotly.newPlot('distribuicao-chart', traces_dist, {
                title: 'Distribuição de Scores Fuzzy',
                xaxis: { title: 'Score Fuzzy' },
                yaxis: { title: 'Frequência' },
                barmode: 'overlay'
            });
        }

        // Filtros
        document.getElementById('filtro-score').addEventListener('input', function() {
            document.getElementById('score-valor').textContent = this.value;
        });

        document.getElementById('filtro-preco').addEventListener('input', function() {
            document.getElementById('preco-valor').textContent = 'R$ ' + this.value;
        });

        function aplicarFiltros() {
            const destino = document.getElementById('filtro-destino').value.toLowerCase();
            const scoreMin = parseFloat(document.getElementById('filtro-score').value);
            const precoMax = parseFloat(document.getElementById('filtro-preco').value);

            fetch('/api/filtrar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ destino, scoreMin, precoMax })
            })
            .then(response => response.json())
            .then(data => exibirDestinosFiltrados(data));
        }

        function exibirDestinosFiltrados(destinos) {
            const container = document.getElementById('destinos-filtrados');
            container.innerHTML = '';

            if (destinos.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999;">Nenhum destino encontrado com os filtros aplicados.</p>';
                return;
            }

            destinos.forEach(d => {
                const card = `
                    <div class="destino-card">
                        <h3>${d.destino}</h3>
                        <div class="destino-info">
                            <div class="destino-info-item">
                                <strong>Score:</strong> ${d.score_medio.toFixed(2)}
                            </div>
                            <div class="destino-info-item">
                                <strong>Sentimento:</strong> ${(d.sentimento_medio * 100).toFixed(1)}%
                            </div>
                            <div class="destino-info-item">
                                <strong>Preço:</strong> R$ ${d.preco_medio.toFixed(2)}
                            </div>
                            <div class="destino-info-item">
                                <strong>Distância:</strong> ${d.distancia_km.toFixed(0)} km
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML += card;
            });
        }
    </script>
</body>
</html>
"""

# ============================================
# ROTAS DA API
# ============================================

@app.route('/')
def index():
    return render_template_string(TEMPLATE_HTML)

@app.route('/api/dados')
def api_dados():
    """Retorna dados gerais para a interface."""
    ranking_dict = ranking.reset_index().to_dict('records')

    return jsonify({
        'total_avaliacoes': len(df_fuzzy),
        'total_destinos': df_fuzzy['destino'].nunique(),
        'score_medio': df_fuzzy['score_fuzzy'].mean(),
        'sentimento_medio': df_fuzzy['prob_positivo'].mean(),
        'ranking': ranking_dict,
        'avaliacoes': df_fuzzy.to_dict('records')
    })

@app.route('/api/filtrar', methods=['POST'])
def api_filtrar():
    """Filtra destinos baseado nos critérios."""
    data = request.json
    destino = data.get('destino', '').lower()
    score_min = data.get('scoreMin', 0)
    preco_max = data.get('precoMax', 10000)

    # Filtrar dados
    filtrado = ranking.reset_index()

    if destino:
        filtrado = filtrado[filtrado['destino'].str.lower().str.contains(destino)]

    filtrado = filtrado[filtrado['score_medio'] >= score_min]
    filtrado = filtrado[filtrado['preco_medio'] <= preco_max]

    return jsonify(filtrado.to_dict('records'))

# ============================================
# EXECUTAR APLICAÇÃO
# ============================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CAMADA IV - INTERFACE WEB INTERATIVA")
    print("="*70)
    print("\n✓ Servidor iniciado com sucesso!")
    print("\n📍 Acesse a aplicação em: http://localhost:5000")
    print("\nPressione CTRL+C para parar o servidor\n")
    print("="*70 + "\n")

    app.run(debug=True, port=5000)