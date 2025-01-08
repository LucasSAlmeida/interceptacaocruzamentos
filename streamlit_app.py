import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from utils.DrawPitchSetPieces import create_pitch_plotly

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/teste_ic.csv')

st.title("Taxa de Interceptação de Cruzamentos - CIR")
st.subheader("Quantidade de cruzamentos que são feitos para a grande área, o quanto são interceptados e quantos geram finalização.")
# Dropdowns
#selected_player = st.selectbox('Selecione um jogador', df.posicao.unique())


selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())
# 1. Gráfico de Ações em Campo

st.title('Cruzamentos na grande área')

df_filter_cross = df[df['evento'] == "Cruzamento"]
filtered_df = df_filter_cross[df_filter_cross['jogo'] == selected_game]
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
st.plotly_chart(pitch_figure)

st.title("Finalizações e gols a partir de cruzamentos")
df_shots=df[(df["evento"] == "Finalização") | (df["evento"] == "Gol")]
selected_action = st.selectbox('Selecione uma ação', df_shots.evento.unique())

filtered_df_shots=df_shots[(df_shots['evento'] == selected_action) & (df_shots['jogo'] == selected_game)]
pitch_figure_shots=create_pitch_plotly(80, 60, 'yards', 'black', df=filtered_df_shots)
st.plotly_chart(pitch_figure_shots)

st.title("Interceptações dos cruzamentos")
df_interceptions=df[df['evento']=='Interceptação']
filtered_df_interc=df_interceptions[df_interceptions['jogo'] == selected_game]
pitch_figure_interc = create_pitch_plotly(80,60,'yards','black',df=filtered_df_interc)
st.plotly_chart(pitch_figure_interc)








