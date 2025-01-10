import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from utils.DrawPitchSetPieces import create_pitch_plotly

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/teste_ic.csv')
#df_filter_cross = df[df['evento'] == "Cruzamento"]
#df_other=df[df['evento'] != "Cruzamento"]

st.title("Taxa de Interceptação de Cruzamentos - CIR")
st.text("Quantidade de cruzamentos que são feitos para a grande área, o quanto são interceptados e quantos geram finalização.")


# Dropdowns
selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())
selected_action = st.selectbox('Selecione uma ação', df_shots.evento.unique())
# 1. Gráfico de Ações em Campo

st.title('Gráficos')

filtered_df= df[(df['jogo'] == selected_game) & (df['evento'] == selected_action)]
pitch_figure = create_pitch_plotly(80, 60, 'yards', 'black', df=filtered_df)
if selected_action in ['Cruzamento']:
    filtered_df_cross=filtered_df[filtered_df['evento'] == selected_action]
    if not filtered_df.empty:
        pitch_figure=create_pitch_plotly(80,60,"yards","black",df=filtered_df_cross)
        
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
        st.write(f"Não foram encontrados dados sobre '{selected_action}' para o jogador {selected_player} no jogo {selected_game}.")
else:
    filtered_action_df = filtered_df[(filtered_df['evento'] == selected_action)]
    pitch_figure = create_pitch_plotly(120, 80, 'yards', 'black', filtered_action_df)
    st.plotly_chart(pitch_figure)

st.title("Finalizações e gols a partir de cruzamentos")








