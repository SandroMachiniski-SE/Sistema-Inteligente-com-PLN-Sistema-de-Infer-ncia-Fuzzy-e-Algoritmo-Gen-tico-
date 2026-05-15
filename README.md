# 🌍 Sistema de Recomendação de Destinos Turísticos

Um sistema inteligente de análise e recomendação de destinos turísticos utilizando **Processamento de Linguagem Natural (PLN)**, **Lógica Fuzzy** e **Interface Web Interativa**.

## 📋 Visão Geral

Este projeto implementa um pipeline completo de análise de avaliações turísticas em 4 camadas:

1. **Camada I (PLN):** Classificação de sentimentos usando Naive Bayes
2. **Camada II (Lógica Fuzzy):** Sistema de inferência fuzzy para recomendação
3. **Camada III (Visualização):** Gráficos e relatórios estáticos
4. **Camada IV (Web):** Interface interativa com Flask e Plotly

## 🎯 Funcionalidades

- ✅ Análise de sentimento de avaliações textuais (positivo, negativo, neutro)
- ✅ Sistema fuzzy que combina sentimento, preço e distância
- ✅ Geração automática de ranking de destinos
- ✅ Visualizações interativas em tempo real
- ✅ Filtros dinâmicos por score, preço e nome do destino
- ✅ Relatórios detalhados em CSV e HTML
- ✅ Interface web responsiva e moderna

## 📊 Resultados

### Ranking de Destinos (Score 0-100)

| Posição | Destino | Score | Sentimento | Preço Médio | Distância |
|---------|---------|-------|-----------|-------------|-----------|
| 🥇 1º | Florianópolis | 57.10 | 35% | R$ 870.57 | 350 km |
| 🥈 2º | Foz do Iguaçu | 53.19 | 36% | R$ 1.116,93 | 800 km |
| 🥉 3º | Rio de Janeiro | 29.55 | 30% | R$ 1.453,30 | 1.150 km |
| 4º | Salvador | 27.38 | 28% | R$ 1.244,83 | 2.100 km |
| 5º | Manaus | 21.62 | 32% | R$ 1.957,13 | 3.500 km |

### Métricas de Desempenho

- **Acurácia do Naive Bayes:** 83.33%
- **Total de Avaliações Analisadas:** 150
- **Destinos Avaliados:** 5
- **Score Fuzzy Médio:** 37.77

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-recomendacao-destinos.git
cd sistema-recomendacao-destinos
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar o Sistema Completo

#### Passo 1: Gerar Dataset
```bash
python gerar_dataset.py
```
Cria o arquivo `dataset_destinos.csv` com avaliações de exemplo.

#### Passo 2: Executar Camada I (PLN)
```bash
python camada1_pln.py
```
Analisa sentimentos e gera `dataset_com_sentimentos.csv`.

**Saída esperada:**
- Acurácia: ~83%
- Arquivo: `dataset_com_sentimentos.csv`

#### Passo 3: Executar Camada II (Lógica Fuzzy)
```bash
python camada2_fuzzy.py
```
Aplica sistema fuzzy e gera ranking.

**Saída esperada:**
- Arquivo: `dataset_com_fuzzy.csv`
- Arquivo: `ranking_destinos.csv`

#### Passo 4: Executar Camada III (Visualização)
```bash
python camada3_visualizacao.py
```
Gera gráficos estáticos em PNG.

**Arquivos gerados:**
- `01_ranking_destinos.png`
- `02_sentimento_vs_score.png`
- `03_preco_vs_distancia.png`
- `04_distribuicao_scores.png`
- `tabela_resumida.csv`
- `tabela_resumida.html`

#### Passo 5: Executar Camada IV (Interface Web)
```bash
python camada4_web.py
```

Acesse em seu navegador: **http://localhost:5000**

## 📁 Estrutura do Projeto
sistema-recomendacao-destinos/ ├── gerar_dataset.py # Gera dados de exemplo ├── camada1_pln.py # Análise de sentimento (Naive Bayes) ├── camada2_fuzzy.py # Sistema de inferência fuzzy ├── camada3_visualizacao.py # Gráficos estáticos ├── camada4_web.py # Interface web interativa ├── requirements.txt # Dependências do projeto ├── README.md # Este arquivo └── dados/ ├── dataset_destinos.csv # Dataset original ├── dataset_com_sentimentos.csv ├── dataset_com_fuzzy.csv ├── ranking_destinos.csv └── [gráficos PNG e HTML]

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem principal
- **NLTK** - Processamento de linguagem natural
- **scikit-learn** - Machine Learning (Naive Bayes)
- **scikit-fuzzy** - Lógica fuzzy
- **pandas** - Manipulação de dados
- **Flask** - Framework web

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização responsiva
- **JavaScript** - Interatividade
- **Plotly.js** - Gráficos interativos

### Visualização
- **Matplotlib** - Gráficos estáticos
- **Seaborn** - Visualizações estatísticas

## 📚 Detalhes Técnicos

### Camada I: Processamento de Linguagem Natural

**Algoritmo:** Naive Bayes Multinomial

**Processo:**
1. Tokenização de textos
2. Remoção de stopwords
3. Vetorização TF-IDF
4. Treinamento do classificador
5. Predição de sentimentos

**Resultado:** Probabilidades para cada classe (positivo, negativo, neutro)

### Camada II: Lógica Fuzzy

**Variáveis de Entrada:**
- Sentimento Positivo (0-1)
- Preço (R$ 0-3000)
- Distância (0-4000 km)

**Variáveis de Saída:**
- Score de Recomendação (0-100)

**Conjuntos Fuzzy:**
- Sentimento: baixo, médio, alto
- Preço: barato, moderado, caro
- Distância: perto, médio, longe
- Score: muito_baixo, baixo, médio, alto, muito_alto

**Regras:** 27 regras fuzzy combinando as entradas

### Camada III: Visualizações

Gráficos gerados:
1. **Ranking de Destinos** - Barras horizontais com cores por score
2. **Sentimento vs Score** - Dispersão mostrando correlação
3. **Preço vs Distância** - Bolhas com tamanho proporcional ao score
4. **Distribuição de Scores** - Histograma por destino
5. **Métricas em Radar** - Análise multidimensional

### Camada IV: Interface Web

**Funcionalidades:**
- Dashboard com estatísticas gerais
- Ranking interativo com tabela
- Gráficos dinâmicos com Plotly
- Filtros em tempo real (destino, score, preço)
- Design responsivo (mobile-friendly)
- API REST para dados

## 📊 Exemplos de Uso

### Filtrar destinos com score > 50 e preço < R$ 1000
1. Acesse http://localhost:5000
2. Mova o slider de "Score Mínimo" para 50
3. Mova o slider de "Preço Máximo" para 1000
4. Clique em "Aplicar Filtros"

### Buscar destino específico
1. Digite o nome do destino no campo "Buscar Destino"
2. Clique em "Aplicar Filtros"

### Analisar gráficos
- Passe o mouse sobre os gráficos para ver valores exatos
- Use os botões de zoom e pan do Plotly
- Clique na legenda para mostrar/ocultar séries

## 🔧 Configuração

### Modificar Dados de Entrada

Edite `gerar_dataset.py` para adicionar novos destinos ou avaliações:

destinos = ['Seu Destino', ...]
avaliacoes_positivas = ['Sua avaliação positiva', ...]

### Ajustar Parâmetros Fuzzy

Em `camada2_fuzzy.py`, modifique os intervalos:


python

preco = ctrl.Antecedent(np.arange(0, 5000, 100), 'preco')  # Novo intervalo




### Mudar Porta da Web

Em `camada4_web.py`:


python

app.run(debug=True, port=8000)  # Mude para 8000




## 📈 Métricas e Avaliação

### Validação do Modelo

O Naive Bayes foi avaliado com:
- **Precision:** 0.84 (média ponderada)
- **Recall:** 0.83
- **F1-Score:** 0.83
- **Acurácia:** 83.33%

### Matriz de Confusão
          precision    recall  f1-score   support
negativo       0.80      0.73      0.76        11
  neutro       1.00      1.00      1.00        10
positivo       0.70      0.78      0.74         9
## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"

bash

pip install -r requirements.txt




### Erro: "Port 5000 already in use"

bash

python camada4_web.py --port 8000




### Gráficos não aparecem
- Certifique-se de que matplotlib está instalado
- Verifique se os arquivos CSV foram gerados corretamente

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## 👨‍💻 Autor

**Sandro**
- Projeto desenvolvido como trabalho acadêmico de Inteligência Artificial

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

## 🎓 Aprendizados

Este projeto demonstra:
- ✅ Processamento de Linguagem Natural com NLTK
- ✅ Machine Learning com scikit-learn
- ✅ Lógica Fuzzy e sistemas de inferência
- ✅ Desenvolvimento web com Flask
- ✅ Visualização de dados com Plotly e Matplotlib
- ✅ Análise e manipulação de dados com pandas
- ✅ Boas práticas de desenvolvimento Python

## 📚 Referências

- [NLTK Documentation](https://www.nltk.org/)
- [scikit-learn](https://scikit-learn.org/)
- [scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/)
- [Flask](https://flask.palletsprojects.com/)
- [Plotly](https://plotly.com/)

---

**Última atualização:** Maio de 2026
Agora crie o arquivo requirements.txt:

pandas==2.0.3
numpy==1.24.3
nltk==3.8.1
scikit-learn==1.3.0
scikit-fuzzy==0.5.0
matplotlib==3.7.1
seaborn==0.12.2
flask==2.3.2
plotly==5.14.0
networkx==3.1
Para gerar o arquivo requirements.txt automaticamente:

bash

pip freeze > requirements.txt
  
