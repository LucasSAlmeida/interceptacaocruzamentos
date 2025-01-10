import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from utils.DrawPitchSetPieces import create_pitch_plotly
import altair as alt

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/teste_ic.csv')

# Título e descrição
st.title("Cruzamentos na Grande Área - CiPA")
st.text("Quantidade de cruzamentos que são feitos para a grande área, o quanto são interceptados e quantos geram finalização.")



#Gráficos exploratórios
st.title("Resumo estatístico dos últimos 3 jogos")
df_defense = df[df['evento'] != "Cruzamento"]
df_defense_gb=df_defense.groupby(["evento","jogo"]).count()
df_defense_gb.reset_index(inplace=True)
df_defense_gb.drop(["x","y","x2","y2"],axis=1,inplace=True)
df_defense_gb['porcentagem']=df_defense_gb['time']/df_defense_gb['time'].sum() * 100
df_defense_gb['porcentagem_texto']=df_defense_gb['porcentagem'].round(1).astype('str') + '%'

source = df_defense_gb
chart = alt.Chart(source).mark_bar().encode(
    x=alt.X(
        'sum(time):Q',
        axis=alt.Axis(
            title="Total de ações pós-cruzamento",
            tickCount=10,
        ),
        scale=alt.Scale(
            domain=[0, 10]
        )
    ),
    y='evento:O',
    color='evento:N',
    row='jogo:N',
    tooltip=[  
        alt.Tooltip('sum(time):Q', title='Total de Ações'),  
        alt.Tooltip('evento:N', title='Tipo de Ação'),     
        alt.Tooltip('jogo:N', title='Jogo')                  
    ]
)
st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.title("Análise longitudinal")
porc=pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/refs/heads/main/porcentagens.csv')


source = porc
chart = alt.Chart(source).mark_line().encode(
        alt.X('jogo:O'),
        alt.Y('porcentagem:Q', axis=alt.Axis(format='%')),
        color='evento:N'
    )             


st.altair_chart(chart, theme="streamlit", use_container_width=True)

# Gráficos com noções de espaco
# Dropdowns para seleção
st.title("Visualização de ações em campo")
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










