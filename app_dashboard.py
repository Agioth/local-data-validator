from dash import Dash, html, dcc, dash_table
import pandas as pd
import plotly.express as px
from database import get_connection, logger

app = Dash(__name__)

def carregar_dados():
    conn = get_connection()
    if conn:
        try:
            # Usando o nome real da tabela: auditoria_seo
            query = "SELECT * FROM auditoria_seo" 
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    fig = px.bar(
        df, 
        x="nivel_prioridade", 
        y="score_prioridade",
        title="Análise de Leads por Nível de Prioridade", 
        color="nivel_prioridade",
        color_discrete_map={
            'CRÍTICA': '#e74c3c', 
            'MÉDIA': '#f39c12',   
            'BAIXA': '#3498db'    
        },
        hover_data=["nome_empresa", "telefone"],
        labels={'nivel_prioridade': 'Nível de Prioridade', 'score_prioridade': 'Pontuação'}
    )
else:
    fig = px.bar(title="Nenhum dado encontrado no banco")

app.layout = html.Div(style={'fontFamily': 'Segoe UI, Arial', 'padding': '30px', 'backgroundColor': '#f9f9f9'}, children=[
    html.H1('Local Data Validator - Dashboard Profissional', style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P('Relatório consolidado de auditoria de SEO local.', style={'textAlign': 'center', 'color': '#7f8c8d'}),

    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='grafico-leads', figure=fig),
    ]),

    html.Br(),
    html.H2('Tabela Detalhada de Leads', style={'color': '#2c3e50'}),
    
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'}, children=[
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i.replace('_', ' ').title(), "id": i} for i in df.columns],
            page_size=15,
            sort_action="native",
            filter_action="native",
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
        )
    ])
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)