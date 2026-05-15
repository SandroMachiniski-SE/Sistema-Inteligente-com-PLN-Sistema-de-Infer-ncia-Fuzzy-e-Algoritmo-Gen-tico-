import pandas as pd
import random

# Definir seed para reprodutibilidade
random.seed(42)

# Dados dos destinos
destinos_info = {
    'Rio de Janeiro': {'preco': 1500, 'distancia': 1150, 'tipo': 'praia'},
    'Salvador': {'preco': 1200, 'distancia': 2100, 'tipo': 'praia'},
    'Florianópolis': {'preco': 900, 'distancia': 350, 'tipo': 'praia'},
    'Manaus': {'preco': 2000, 'distancia': 3500, 'tipo': 'natureza'},
    'Foz do Iguaçu': {'preco': 1100, 'distancia': 800, 'tipo': 'natureza'}
}

# Avaliações positivas
avaliacoes_positivas = [
    "Destino incrível! Superou minhas expectativas. Voltaria com certeza!",
    "Maravilhoso! Paisagens de tirar o fôlego e pessoas muito simpáticas.",
    "Experiência fantástica! Recomendo para todos os amigos.",
    "Perfeito! Tudo bem organizado e muito bonito.",
    "Adorei! Voltaria mil vezes se pudesse.",
    "Sensacional! Melhor viagem da minha vida.",
    "Excelente custo-benefício! Muito bom mesmo.",
    "Que lugar lindo! Ficamos apaixonados.",
    "Simplesmente perfeito! Tudo funcionou muito bem.",
    "Recomendo demais! Vale muito a pena visitar."
]

# Avaliações negativas
avaliacoes_negativas = [
    "Muito caro e decepcionante. Não recomendo.",
    "Péssimo! Não vale o preço cobrado.",
    "Horrível! Tudo muito sujo e desorganizado.",
    "Não gostei. Esperava muito mais.",
    "Decepção total. Não volto mais.",
    "Muito ruim! Atendimento péssimo.",
    "Não recomendo. Muito caro pelo que oferece.",
    "Terrível experiência. Dinheiro jogado fora.",
    "Muito decepcionante. Não vale a pena.",
    "Horrível! Pior viagem que já fiz."
]

# Avaliações neutras
avaliacoes_neutras = [
    "Lugar ok. Nada de especial, mas também não é ruim.",
    "Normal. Tem seus pontos bons e ruins.",
    "Mediano. Esperava mais, mas não foi ruim.",
    "Aceitável. Poderia ser melhor.",
    "Razoável. Alguns pontos bons, outros nem tanto.",
    "Nem bom nem ruim. Apenas ok.",
    "Lugar comum. Nada excepcional.",
    "Pode ir, mas não é imprescindível.",
    "Regular. Tem coisas legais e outras não.",
    "Aceitável, mas poderia melhorar bastante."
]

# Criar dataset
dados = []

for destino, info in destinos_info.items():
    # 30 avaliações por destino (total 150)
    for i in range(30):
        # Distribuir: 10 positivas, 10 negativas, 10 neutras
        if i < 10:
            avaliacao = random.choice(avaliacoes_positivas)
            rating = random.randint(4, 5)
            sentimento = 'positivo'
        elif i < 20:
            avaliacao = random.choice(avaliacoes_negativas)
            rating = random.randint(1, 2)
            sentimento = 'negativo'
        else:
            avaliacao = random.choice(avaliacoes_neutras)
            rating = 3
            sentimento = 'neutro'

        # Adicionar variação ao preço (±20%)
        preco_variado = info['preco'] + random.randint(-int(info['preco']*0.2), int(info['preco']*0.2))

        dados.append({
            'avaliacao': avaliacao,
            'rating': rating,
            'destino': destino,
            'preco_medio': preco_variado,
            'distancia_km': info['distancia'],
            'tipo': info['tipo'],
            'sentimento_real': sentimento
        })

# Criar DataFrame
df = pd.DataFrame(dados)

# Salvar como CSV
df.to_csv('dataset_destinos.csv', index=False, encoding='utf-8')

print("Dataset criado com sucesso!")
print(f"Total de avaliações: {len(df)}")
print("\nPrimeiras 5 linhas:")
print(df.head())
print("\nArquivo salvo como: dataset_destinos.csv")