import streamlit as st
import plotly.graph_objects as go

# Função que cria o campo
def create_pitch_plotly(length, width, unity, linecolor, df=None):

    # Criar a figura do campo
    fig = go.Figure()

    # Adiciona o campo de futebol
    fig.add_shape(type="rect", x0=0, y0=0, x1=length, y1=width, line=dict(color=linecolor))


    # Área de pênalti
    fig.add_shape(type="rect", x0=18, y0=0, x1=62, y1=18, line=dict(color=linecolor))


    # Área de 5 metros
    fig.add_shape(type="rect", x0=29, y0=0, x1=51, y1=7, line=dict(color=linecolor))


    # Círculo central e marca de pênalti
    fig.add_shape(type="circle", x0=(length / 2) - 9.15, y0=(width/2) +18, x1=(length / 2) + 9.15, y1=(width / 2) + 40, line=dict(color=linecolor))

    fig.add_shape(type="circle", x0=40 - 0.8, y0=(width / 2) - 20, x1=40 + 0.8, y1=(width / 2) - 18, fillcolor=linecolor)


    # Configurações do layout
    fig.update_layout(
        height=420,
        width=600,
        margin=dict(l=30, r=30, t=30, b=5),
        plot_bgcolor='white',
        dragmode=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    #Reverte os valores do eixo y
    fig.update_yaxes(autorange='reversed')

    # Adiciona os pontos no campo, se fornecidos
    if df is not None:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'], mode='markers',
            marker=dict(size=10, color='red'),
            showlegend=False
        ))

    return fig
