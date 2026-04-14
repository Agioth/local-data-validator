Dev Log: Do Código ao Produto (O Salto de Maturidade)
Data: 13 de Abril de 2026 | Por: Thiago (Agioth)

A sessão de hoje foi marcada pela palavra Robustez. Entendi que, para garantir uma vaga Home Office, não basta o código "funcionar na minha máquina"; ele precisa ser seguro, testável e fácil de ser movido para qualquer lugar.

O Pilar da Segurança e Arquitetura
A grande mudança estrutural foi a morte dos params espalhados pelo código.

Centralização: Criamos o database.py, um "porteiro" único para o banco de dados.

Blindagem de Credenciais: Implementei o uso de variáveis de ambiente com o .env. Agora, minhas senhas não ficam expostas no código.

O Escudo .gitignore: Configurei o Git para nunca "vazar" informações sensíveis. Isso é maturidade profissional básica que me diferencia de amadores.

Qualidade e Validação de Dados (Pydantic v2)
O projeto agora tem um "filtro de pureza". Com o models.py usando Pydantic, os dados brutos do PostgreSQL são transformados em objetos validados.

Cálculo Automático: O sistema limpa o telefone via Regex e calcula o Leads Quality Score no momento da criação do objeto.

Legenda Comercial: A exportação agora gera um relatório CSV que já vem com uma legenda explicativa, transformando dados técnicos em valor para o setor de vendas.

Mentalidade de Engenharia: "Menos é Mais"
Fizemos uma limpeza profunda no repositório. Deletei o analisador.py e scripts de rascunho. O projeto agora é enxuto, direto ao ponto e segue padrões de mercado. A introdução do test_projeto.py garante que qualquer alteração futura possa ser validada em segundos, evitando o medo de "cagar o código".

Roadmap para a Robustez Total (v2.0)
Definimos os quatro pilares que transformarão o Local-Data-Validator em um projeto nível Pleno:

Logs Profissionais: Implementar rastreabilidade de erros para operações remotas.

Dockerização: Criar containers para que o projeto rode em qualquer sistema sem atritos.

Pytest: Evoluir os testes simples para uma suíte de testes automatizados profissional.

Interface Streamlit: Criar a camada visual (Dashboard) para transformar os dados em gráficos inteligentes.

Frase do dia: "O código que eu escrevo hoje é o meu currículo de amanhã."