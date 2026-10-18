# AI Support Intelligence v1.0

> Plataforma de auditoria inteligente de atendimentos, com regras de negócio explícitas, evidências rastreáveis e revisão humana.

**Status:** Planejamento e estruturação  
**Versão:** 1.0  
**Categoria:** Automação, integrações, IA aplicada e qualidade operacional

## 1. Visão geral

O AI Support Intelligence é uma plataforma demonstrativa que automatiza etapas da auditoria de conversas de atendimento ao cliente.

A solução combina integração de dados, processamento de texto, regras determinísticas e inteligência artificial para avaliar qualidade e conformidade, registrar evidências e disponibilizar resultados para revisão.

O projeto utilizará exclusivamente dados, empresas, agentes e procedimentos fictícios.

## 2. Problema de negócio

Auditorias manuais podem consumir muitas horas, cobrir apenas uma parcela dos atendimentos e gerar inconsistências na aplicação de critérios.

Além disso, identificar uma possível infração não basta: é necessário demonstrar a evidência, relacioná-la ao procedimento aplicável e permitir que o resultado seja revisado ou contestado.

## 3. Objetivos

- Automatizar a ingestão e o processamento de conversas.
- Padronizar avaliações de qualidade e conformidade.
- Identificar possíveis infrações com evidências verificáveis.
- Aplicar regras de pontuação consistentes.
- Reduzir falsos positivos e penalidades duplicadas.
- Permitir revisão humana e contestação.
- Produzir indicadores e relatórios operacionais.
- Registrar execuções, erros e custos de processamento.

## 4. Escopo funcional

### Ingestão e processamento

- Consumir conversas de uma API simulada.
- Implementar paginação, filtros e validação.
- Processar transcrições, metadados e avaliações.
- Distinguir atendimentos humanos e automatizados.
- Tratar indisponibilidade, respostas inválidas e registros duplicados.

### Auditoria de qualidade e conformidade

- Executar avaliações distintas para qualidade e conformidade.
- Classificar conversas em categorias de negócio.
- Consultar procedimentos internos fictícios.
- Exigir evidências textuais para sustentar possíveis infrações.
- Aplicar severidades e pontuações documentadas.
- Detectar possíveis falsos positivos.
- Evitar múltiplas penalidades pelo mesmo evento subjacente.

### Revisão e contestação

- Registrar a auditoria original e suas evidências.
- Permitir contestação de resultados.
- Reavaliar o caso considerando a contestação.
- Encaminhar casos incertos para revisão humana.
- Manter histórico das decisões e alterações.

### Relatórios e indicadores

- Apresentar resultados por agente, período e categoria.
- Exibir evidências, procedimento aplicável e recomendação de melhoria.
- Preservar a avaliação original do cliente.
- Diferenciar avaliações negativas justificadas por causas externas de falhas atribuíveis ao atendimento.
- Registrar custos, duração, falhas e volume processado.

## 5. Regras de negócio iniciais

A pontuação será definida em um documento específico de regras de negócio.

A proposta inicial prevê uma pontuação-base de 10 pontos e penalidades por severidade:

| Severidade | Penalidade proposta |
|---|---:|
| Baixa | 1 ponto |
| Média | 2 pontos |
| Grave | 3 pontos |
| Muito grave | 10 pontos |

Esses valores são uma especificação inicial a validar nos testes. O tratamento de limites, múltiplas infrações, exceções e casos sem evidência será documentado antes da implementação.

A IA não deverá determinar uma infração sem apresentar evidências verificáveis e referência ao critério utilizado. Resultados incertos poderão ser encaminhados para revisão humana.

## 6. Arquitetura prevista

- **FastAPI:** exposição dos endpoints e validação das requisições.
- **Python:** regras de negócio, processamento e serviços.
- **PostgreSQL:** conversas, auditorias, evidências, contestações e histórico.
- **n8n:** orquestração dos workflows.
- **Módulo de IA:** análise textual e classificação estruturada.
- **Dashboard:** visualização de auditorias e indicadores.
- **Docker Compose:** ambiente reproduzível.
- **Pytest:** testes automatizados.

## 7. Confiabilidade e segurança

- Validação de entradas e saídas.
- Logs estruturados com identificadores de execução.
- Retentativas limitadas e tratamento de erros.
- Idempotência no processamento quando aplicável.
- Separação de dados e credenciais por ambiente.
- Segredos fora do repositório.
- Evidências e histórico para auditoria.
- Revisão humana para decisões de maior impacto.

A confiança declarada pelo modelo não será tratada automaticamente como probabilidade calibrada. A qualidade das decisões deverá ser medida com casos rotulados e revisados.

## 8. Testes e critérios de aceitação

A primeira versão deverá demonstrar que é possível:

1. Obter conversas da API simulada.
2. Validar e processar transcrições.
3. Aplicar regras a casos conhecidos.
4. Gerar resultados estruturados com evidências.
5. Evitar penalidades duplicadas nos casos previstos.
6. Persistir auditorias e contestações.
7. Tratar erros de integração.
8. Executar testes automatizados.
9. Consultar os resultados pelo dashboard.

## 9. Dados

Os dados serão sintéticos e incluirão conversas normais, casos com possíveis infrações, avaliações negativas justificadas, ambiguidades e falhas de integração.

Cada cenário relevante terá um resultado esperado para permitir testes objetivos.

## 10. Status e próximos passos

**Status atual:** planejamento.

Próximas etapas:

1. Documentar regras de negócio e critérios de aceitação.
2. Definir o modelo de dados.
3. Criar transcrições sintéticas e casos de teste.
4. Implementar a API simulada.
5. Construir a API e a persistência.
6. Integrar n8n e módulo de IA.
7. Integrar o dashboard existente.
8. Preparar documentação de execução e demonstração.

## 11. Limitações

O projeto é demonstrativo e não está autorizado a tomar decisões reais sobre funcionários ou clientes. Resultados produzidos pela IA exigem validação, evidências e possibilidade de revisão.