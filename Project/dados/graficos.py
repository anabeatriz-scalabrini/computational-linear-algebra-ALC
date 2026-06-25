import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Leitura dos dados
df = pd.read_csv('resultados_30inst.csv', sep=';', decimal=',')

# Remove as instâncias inviáveis (como a 6 e a 27) para os gráficos numéricos
df_plot = df.dropna(subset=['Média L2']).copy()
df_plot['ID Instância'] = df_plot['ID Instância'].astype(int).astype(str)

# Configurações visuais estilo artigo científico
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({'font.family': 'serif', 'font.size': 12})

# =====================================================================
# GRÁFICO 1: Tempo de Execução
# =====================================================================
plt.figure(figsize=(10, 5))
ax = sns.barplot(x='ID Instância', y='Tempo (s)', data=df, color='steelblue', edgecolor='black')
plt.axhline(y=300, color='red', linestyle='--', linewidth=1.5, label='Limite de Tempo (300s)')
plt.title('Tempo Computacional por Instância (Gurobi)', fontweight='bold')
plt.xlabel('ID da Instância')
plt.ylabel('Tempo de Execução (s)')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('figura1_tempo_execucao.png', dpi=300)
plt.close()

# =====================================================================
# GRÁFICO 2: Margem de Isolamento (L2 Média vs Mínima)
# =====================================================================
plt.figure(figsize=(10, 5))
plt.plot(df_plot['ID Instância'], df_plot['Média L2'], marker='o', label='Média L2 (Linha Reta)', color='navy', linewidth=2)
plt.plot(df_plot['ID Instância'], df_plot['Menor L2'], marker='s', label='Mínimo L2 Exigido', color='darkorange', linewidth=2)

plt.fill_between(df_plot['ID Instância'], df_plot['Menor L2'], df_plot['Média L2'], color='skyblue', alpha=0.3, label='Margem de Isolamento')

plt.title('Dispersão Euclidiana ($L_2$) de Alunos em Conflito', fontweight='bold')
plt.xlabel('ID da Instância (Apenas Factivéis)')
plt.ylabel('Distância (Unidades/Carteiras)')
plt.xticks(rotation=45, ha='right')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figura2_margem_isolamento.png', dpi=300)
plt.close()

# =====================================================================
# GRÁFICO 3: Boxplot das Três Normas Vetoriais
# =====================================================================
# Preparando os dados para o seaborn (formato longo)
df_melt = pd.melt(df_plot, 
                  value_vars=['Média L1', 'Média L2', 'Média L-inf'],
                  var_name='Norma Vetorial', 
                  value_name='Distância Média')

# Limpando os nomes para o gráfico
df_melt['Norma Vetorial'] = df_melt['Norma Vetorial'].replace({
    'Média L1': '$L_1$ (Manhattan)',
    'Média L2': '$L_2$ (Euclidiana)',
    'Média L-inf': '$L_\infty$ (Máximo)'
})

plt.figure(figsize=(8, 5))
sns.boxplot(x='Norma Vetorial', y='Distância Média', data=df_melt, palette='Set2', width=0.5)
plt.title('Distribuição Analítica das Normas Espaciais', fontweight='bold')
plt.ylabel('Distância Média')
plt.xlabel('')
plt.tight_layout()
plt.savefig('figura3_boxplot_normas.png', dpi=300)
plt.close()

print("Pronto! As três imagens (figura1_tempo_execucao.png, figura2_margem_isolamento.png, figura3_boxplot_normas.png) foram criadas na sua pasta.")