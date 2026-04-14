# 🚀 Local-Data-Validator (SEO Audit Tool)

Ferramenta de engenharia de dados para auditoria de SEO local. O sistema extrai dados, valida informações via banco PostgreSQL e gera um dashboard de priorização de leads.

## ✨ Destaques Técnicos
- **Dashboard Dinâmico:** Construído com Dash/Plotly para visualização de scores.
- **Arquitetura Robusta:** Containerização completa com Docker e Docker Compose.
- **Tratamento de Dados:** Uso de Pandas para análise e limpeza.
- **Logs de Auditoria:** Rastreamento completo de conexões e erros.

## 🛠️ Como Rodar
1. Configure o `.env` com suas credenciais.
2. Suba o ambiente:
   ```bash
   docker-compose up --build