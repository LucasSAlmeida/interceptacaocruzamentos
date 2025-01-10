import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
from utils.DrawPitchSetPieces import create_pitch_plotly

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/teste_ic.csv')

# Título e descrição
st.title("Taxa de Interceptação de Cruzamentos - CIR")
st.text("Quantidade de cruzamentos que são feitos para a grande área, o quanto são interceptados e quantos geram finalização.")

# Dropdowns para seleção
selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())
selected_action = st.selectbox('Selecione uma ação', df.evento.unique())

# Filtrar os dados com base nas seleções
filtered_df = df[(df['jogo'] == selected_game) & (df['evento'] == selected_action)]

# Verificar se há dados para a ação selecionada
if filtered_df.empty:
    st.write(f"Não foram encontrados dados sobre '{selected_action}' no jogo '{selected_game}'.")
else:
    # Criar o gráfico do campo
    pitch_figure = create_pitch_plotly(80, 60, 'yards', 'black', df=filtered_df)
    
    if selected_action == 'Cruzamento':
        # Adicionar traços e anotações no gráfico para cruzamentos
        for _, row in filtered_df.iterrows():
            pitch_figure.add_trace(
                go.Scatter(
                    x=[row['x']],
                    y=[row['y']],
                    mode='lines+markers',
                    line=dict(color='black', width=2),
                    marker=dict(color='red', size=6),
                    showlegend=False,
                    hoverinfo='none',
                )
            )
            pitch_figure.add_annotation(
                x=row['x2'], 
                y=row['y2'], 
                ax=row['x'], 
                ay=row['y'],
                xref="x", 
                yref="y",
                axref="x", 
                ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='black'
            )
        st.plotly_chart(pitch_figure)
    else:
        # Plotar diretamente o campo para outras ações
        st.plotly_chart(pitch_figure)










