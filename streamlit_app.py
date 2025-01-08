import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.DrawPitchSetPieces import create_pitch_plotly

# Função para criar gráficos de ações no campo
def plot_actions(df, title, action_type, selected_game, key):
    st.title(title)
    filtered_df = df[(df['evento'] == action_type) & (df['jogo'] == selected_game)]
    pitch_figure = create_pitch_plotly(80, 60, 'yards', 'black', df=filtered_df)

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
    st.plotly_chart(pitch_figure, key=key)

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/teste_ic.csv')

# Título e descrição do app
st.title("Taxa de Interceptação de Cruzamentos - CIR")
st.subheader("Quantidade de cruzamentos que são feitos para a grande área, o quanto são interceptados e quantos geram finalização.")

# Selecionar jogo
selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())

# Gráfico 1: Cruzamentos na grande área
plot_actions(df, 'Cruzamentos na grande área', 'Cruzamento', selected_game, key="crossings")

# Gráfico 2: Finalizações e gols a partir de cruzamentos
st.title("Finalizações e gols a partir de cruzamentos")
df_shots = df[(df["evento"] == "Finalização") | (df["evento"] == "Gol")]
selected_action = st.selectbox('Selecione uma ação', df_shots.evento.unique())
plot_actions(df_shots, f'{selected_action}s a partir de cruzamentos', selected_action, selected_game, key="shots")

# Gráfico 3: Interceptações de cruzamentos
plot_actions(df, 'Interceptações dos cruzamentos', 'Interceptação', selected_game, key="interceptions")






