# AI Support Intelligence

### AI-powered Support Quality, Compliance & Operational Intelligence

Plataforma de auditoria inteligente de atendimentos que combina classificação determinística, automação de processos, inteligência artificial, análise de evidências e revisão de decisões para avaliar a qualidade operacional, a conformidade e a experiência do cliente.

O sistema foi concebido para transformar grandes volumes de conversas em auditorias rastreáveis, indicadores confiáveis e oportunidades de melhoria, preservando o histórico das decisões e permitindo contestação pelos analistas.

> **Status:** Especificação inicial do produto — em planejamento e evolução. As funcionalidades descritas representam o escopo planejado e não devem ser consideradas implementadas até que sejam desenvolvidas e testadas.

---

## 1. Problema de negócio

Auditorias manuais de atendimento apresentam limitações de escala, consistência e rastreabilidade. A cobertura pode ser insuficiente, critérios podem ser interpretados de maneira diferente entre avaliadores e indicadores podem ser distorcidos por causas externas à atuação dos analistas.

Além disso, avaliar apenas a nota final do cliente não explica o que aconteceu durante o atendimento, se houve descumprimento de procedimentos ou se a experiência foi prejudicada por fatores externos.

A operação precisa de um processo capaz de:

- Analisar atendimentos recentes em lote.
- Identificar contexto, intenção e sinais operacionais antes da auditoria.
- Acionar avaliações específicas com base em regras objetivas.
- Separar qualidade de atendimento e conformidade.
- Identificar infrações com evidências e níveis de gravidade.
- Distinguir avaliações negativas justificadas por fatores externos.
- Revisar resultados para reduzir falsos positivos e falsos negativos.
- Produzir indicadores consistentes por analista, marca, canal e período.
- Permitir contestação com rastreabilidade e revisão humana.
- Monitorar execuções, falhas, consumo de tokens e custos de IA.

## 2. Solução proposta

O AI Support Intelligence utiliza uma pipeline de processamento que combina regras determinísticas e modelos de IA especializados.

As regras determinísticas realizam classificações e acionamentos previsíveis. Os modelos de IA interpretam conversas, comparam evidências com procedimentos internos e apoiam decisões que exigem análise contextual.

Uma etapa final de revisão verifica a consistência dos resultados antes de consolidá-los nos indicadores e relatórios.

### Princípios do sistema

- **Evidência antes de decisão:** toda infração deve estar associada à conversa, à regra aplicável e aos trechos que sustentam a conclusão.
- **Qualidade e conformidade separadas:** cada pilar possui auditoria e pontuação próprias.
- **Rastreabilidade:** decisões, alterações, revisões e contestações devem manter histórico.
- **Preservação dos dados originais:** notas de clientes e resultados anteriores não devem ser apagados para melhorar indicadores.
- **Revisão humana:** casos inconclusivos ou de baixa confiança podem ser encaminhados a uma pessoa responsável.
- **Automação observável:** cada execução deve produzir informações suficientes para diagnóstico, acompanhamento e melhoria.

## 3. Fluxo operacional

O processamento é periódico e começa pela coleta em lote dos atendimentos recentes. Depois que o ciclo termina, uma nova execução inicia a próxima coleta.

### Etapa 1 — Ingestão dos atendimentos

O sistema consulta a API de atendimento e coleta os registros recentes, incluindo, conforme disponibilidade:

- Identificador do atendimento e do cliente.
- Marca ou workspace de origem.
- Canal de atendimento.
- Transcrição e histórico da conversa.
- Timestamps e duração.
- Identificação de agentes humanos e bots.
- Nota de satisfação e demais metadados.
- Links para consulta do atendimento original.

A ingestão deve suportar paginação, autenticação, filtros, tratamento de erros e prevenção de processamento duplicado.

### Etapa 2 — Cases de atendimento

Cada conversa passa inicialmente por uma camada de classificação chamada **Cases de Atendimento**.

Essa camada organiza o contexto antes da execução das auditorias. As classificações iniciais podem utilizar regex, regras determinísticas e processamento de texto.

Dimensões previstas:

- Marca e workspace.
- Canal de atendimento, incluindo canais externos.
- Área ou segmento operacional.
- Intenção do cliente.
- Sentimento e variação de sentimento ao longo da conversa.
- Assunto, motivo do contato e contexto.
- Outros sinais identificados durante a evolução do projeto.

As áreas inicialmente previstas incluem:

- Operações.
- Financeiro.
- Marketing.
- Produto.
- Compliance.
- Canais externos.

Essas categorias representam contexto de negócio e não constituem, por si só, infrações.

As classificações devem registrar os critérios utilizados e permitir evolução das regras sem perder a rastreabilidade.

### Etapa 3 — Gatilhos determinísticos

Após a classificação, regras específicas verificam os resultados dos Cases de Atendimento e determinam quais avaliações devem ser acionadas.

Exemplos conceituais:

- Um caso relacionado a prazo pode acionar uma auditoria específica de qualidade.
- Uma divergência em procedimento obrigatório pode acionar uma avaliação de conformidade.
- Uma combinação de contexto operacional, sentimento e desfecho negativo pode acionar verificações adicionais.
- Uma nota baixa de satisfação pode encaminhar o atendimento à trilha de CSAT justificado.

Cada gatilho deve possuir identificação, condições, versão da regra, justificativa do acionamento e trilha de auditoria correspondente.

O objetivo é utilizar IA de forma direcionada, fornecendo apenas o contexto necessário para cada avaliação, sem depender de uma análise genérica e indiscriminada de todas as conversas.

### Etapa 4 — Auditorias por IA

As auditorias de qualidade e conformidade são executadas separadamente, com contexto e critérios específicos.

O contexto fornecido pode incluir:

- Transcrição completa ou trechos relevantes.
- Intenção e classificação do atendimento.
- Gatilhos acionados.
- Procedimentos internos aplicáveis.
- Marca e canal.
- Tempos e eventos do atendimento.
- Evidências relevantes e metadados disponíveis.

Cada auditoria deve identificar possíveis infrações, explicar a regra aplicável, apresentar evidências e atribuir o nível de gravidade correspondente.

Resultados inconclusivos não devem ser convertidos automaticamente em infrações confirmadas.

#### Auditoria de qualidade

Avalia a condução do atendimento, a comunicação, a compreensão da necessidade do cliente, a resolução e outros critérios definidos pela operação.

#### Auditoria de conformidade

Verifica o cumprimento de políticas, procedimentos obrigatórios e regras aplicáveis à situação analisada.

Cada pilar gera um resultado independente, incluindo ocorrências, evidências, gravidades, justificativas e score.

### Etapa 5 — CSAT justificado

A trilha de CSAT justificado analisa especificamente atendimentos com notas baixas de satisfação.

O objetivo é identificar se a avaliação negativa está relacionada à atuação interna ou a fatores externos, preservando a nota original do cliente.

Fluxo previsto:

1. Filtrar os atendimentos com avaliações negativas.
2. Recuperar a conversa, o contexto e as evidências disponíveis.
3. Investigar fatores externos, como instabilidades ou problemas operacionais alheios à condução do analista.
4. Investigar possíveis falhas internas de qualidade ou conformidade.
5. Emitir uma recomendação fundamentada de abono.
6. Registrar a decisão, a justificativa e as evidências.
7. Atualizar os indicadores conforme as regras de CSAT aprovadas.

Decisões previstas:

- **Abono aprovado:** os critérios de justificação foram atendidos.
- **Abono reprovado:** as evidências não sustentam o abono, inclusive quando há falha interna atribuível ao atendimento.
- **Pendente de revisão:** as evidências são insuficientes ou a causa não pode ser determinada com segurança.

O sistema preservará a nota original, a decisão e o histórico. O abono não apagará a avaliação recebida.

O indicador de CSAT justificado será complementar ao CSAT convencional e permitirá analisar a satisfação considerando os critérios de justificativa definidos pela operação. Sua fórmula e suas regras de inclusão e exclusão serão formalizadas antes da implementação.

### Etapa 6 — Revisão final por IA

Após as auditorias e a análise de CSAT, uma etapa de revisão verifica a consistência dos resultados.

Entre os objetivos dessa etapa estão:

- Identificar falsos positivos.
- Procurar falsos negativos.
- Verificar infrações incompatíveis com as evidências.
- Identificar procedimentos incorretamente aplicados.
- Reavaliar recomendações de abono.
- Identificar abonos negados ou aprovados de maneira inadequada.
- Verificar inconsistências entre os pilares.
- Encaminhar casos inconclusivos para revisão humana.

Os resultados anteriores não serão apagados. A revisão produzirá uma versão final identificável, preservando as decisões anteriores e suas justificativas.

A revisão por IA reduz o risco de erro, mas não garante ausência de falsos positivos ou negativos. A qualidade do processo deverá ser validada por amostras revisadas por pessoas.

### Etapa 7 — Persistência e observabilidade

Os resultados serão registrados em estruturas de dados organizadas, com separação entre dados de negócio e informações técnicas.

O escopo de persistência inclui:

- Atendimentos e transcrições.
- Cases e classificações.
- Gatilhos e regras acionadas.
- Auditorias de qualidade.
- Auditorias de conformidade.
- Infrações, gravidades e evidências.
- Scores por pilar e score geral.
- CSAT original e justificado.
- Decisões e justificativas de abono.
- Revisões finais e versões dos resultados.
- Contestações e decisões humanas.
- Logs, debug, erros e tentativas.
- Duração e status das execuções.
- Modelos utilizados, tokens consumidos e custos estimados.

A estrutura deverá permitir consultar os resultados detalhadamente e fornecer dados ao projeto Automation Control Tower, responsável pela observabilidade técnica das automações.

### Etapa 8 — Relatórios de desempenho

Após a conclusão e consolidação das auditorias, os analistas receberão relatórios periódicos compactos, legíveis e orientados à ação.

Os relatórios deverão incluir:

- Desempenho geral.
- Score de qualidade.
- Score de conformidade.
- Score geral.
- Histórico de infrações e respectivas gravidades.
- Evidências e links dos atendimentos.
- Procedimentos que deveriam ter sido seguidos.
- Resumos gerados por IA.
- Situação dos pedidos de abono.
- Indicadores de CSAT.
- Oportunidades de melhoria.
- Plano de Desenvolvimento Individual (PDI), conforme critérios da operação.
- Link para contestação das avaliações elegíveis.

Os relatórios devem priorizar clareza, rastreabilidade e apresentação profissional.

### Etapa 9 — Contestação e revisão humana

O analista poderá contestar uma auditoria por meio de um formulário.

Fluxo previsto:

1. O analista envia a contestação.
2. Um webhook recebe a solicitação e associa o registro à auditoria original.
3. A IA analisa a argumentação, as evidências e os critérios aplicáveis.
4. A decisão automática é considerada somente quando as condições de confiança e validação forem atendidas.
5. Se a confiança estimada for inferior a 60%, o caso será encaminhado para revisão humana.
6. O revisor humano aprova ou rejeita a contestação.
7. A decisão, a justificativa e as alterações resultantes ficam registradas.
8. Os indicadores são atualizados conforme a decisão final.

O limiar de 60% é um requisito inicial de encaminhamento, não uma garantia estatística de acerto. A confiança do modelo deverá ser avaliada e calibrada com casos revisados.

## 4. Regras de pontuação

A pontuação inicial será baseada em infrações confirmadas, com pesos diferentes conforme a gravidade.

| Gravidade | Peso de desconto |
|---|---:|
| Baixa | 1 ponto |
| Média | 2 pontos |
| Grave | 3 pontos |
| Muito grave | 10 pontos |

A nota inicial de cada pilar é 10.

### Score por pilar

A fórmula inicial prevista é:

`Score do pilar = 10 − soma dos pesos das infrações confirmadas`

Exemplo: uma conversa com uma infração média e uma baixa em qualidade recebe:

`Score de qualidade = 10 − 2 − 1 = 7`

A conformidade é calculada separadamente, com base nas suas próprias infrações.

### Score geral da conversa

O score geral será a média aritmética dos dois pilares:

`Score geral = (Score de qualidade + Score de conformidade) / 2`

Exemplo: qualidade 7 e conformidade 9 resultam em score geral 8.

### Agregação por analista

O desempenho do analista será consolidado a partir dos resultados das conversas auditadas no período de referência.

O cálculo deverá apresentar separadamente:

- Média de qualidade.
- Média de conformidade.
- Média do score geral.
- Volume de conversas auditadas.
- Quantidade e distribuição de infrações por gravidade.
- Indicadores de CSAT convencional e justificado.

Os detalhes de agregação, limites mínimos dos scores, tratamento de auditorias pendentes, critérios de amostragem e arredondamento serão definidos na especificação funcional.

## 5. Arquitetura técnica prevista

A arquitetura proposta separa orquestração, regras de negócio, modelos de IA, persistência e apresentação.

| Componente | Responsabilidade |
|---|---|
| n8n | Orquestração dos ciclos, webhooks, integrações e notificações |
| Python | Lógica de negócio, classificação, regras e processamento |
| FastAPI | Endpoints, validação de entradas e contratos de API |
| PostgreSQL | Persistência de atendimentos, auditorias, resultados e histórico |
| Modelos de IA | Auditorias, CSAT justificado, revisão e análise de contestações |
| Dashboard | Consulta dos resultados e indicadores |
| Docker Compose | Execução reproduzível dos serviços |
| Pytest | Testes unitários e de integração |
| GitHub Actions | Verificações automatizadas de qualidade e testes |

A implementação será incremental. A escolha definitiva de provedores, modelos e integrações será documentada à medida que as decisões técnicas forem validadas.

## 6. Requisitos de confiabilidade

O sistema deverá considerar:

- Prevenção de processamento duplicado.
- Idempotência em execuções e webhooks.
- Tratamento de paginação e falhas de API.
- Retentativas controladas e registro de erros.
- Versionamento de regras, prompts e resultados.
- Separação de credenciais e dados por marca ou workspace.
- Controle de acesso a informações sensíveis.
- Registro de decisões e alterações.
- Tratamento de indisponibilidade de modelos de IA.
- Proteção contra resultados incompletos ou inconsistentes.
- Monitoramento de custos e consumo de tokens.
- Testes de regressão para regras de classificação, pontuação e abono.

## 7. Segurança e dados

O portfólio utilizará dados sintéticos e cenários fictícios.

Não devem ser publicados no repositório:

- Credenciais ou tokens reais.
- Transcrições confidenciais de clientes.
- Dados pessoais ou registros internos da empresa.
- Procedimentos proprietários não autorizados.
- Arquivos `.env` com segredos.

As configurações deverão ser documentadas por meio de um arquivo `.env.example`, sem valores secretos. Os exemplos de atendimentos e procedimentos serão criados especificamente para demonstração e testes.

## 8. Estrutura planejada do projeto

```text
ai-support-intelligence/
├── README.md
├── docker-compose.yml
├── .env.example
├── docs/
├── workflows/
│   └── n8n/
├── src/
│   ├── api/
│   ├── services/
│   ├── ai/
│   └── db/
├── mock_api/
├── data/
│   └── synthetic/
├── tests/
│   ├── unit/
│   └── integration/
├── dashboard/
└── .github/
    └── workflows/
```

A estrutura será criada conforme cada componente for implementado, sem exigir que todas as pastas existam desde o início.

## 9. Plano de implementação

1. Consolidar requisitos funcionais, categorias e regras de negócio.
2. Especificar o fluxo dos Cases de Atendimento e dos gatilhos.
3. Formalizar gravidades, scores, CSAT justificado e regras de agregação.
4. Criar a API simulada e os dados sintéticos.
5. Implementar ingestão, classificação e prevenção de duplicidade.
6. Implementar as auditorias independentes de qualidade e conformidade.
7. Implementar CSAT justificado e revisão final.
8. Implementar persistência, logs, custos e tokens.
9. Criar relatórios, contestação e revisão humana.
10. Integrar o dashboard existente, após inspeção dos arquivos.
11. Instrumentar eventos para o Automation Control Tower.
12. Validar cenários, documentar limitações e preparar demonstração.

## 10. Critérios de validação

O projeto será considerado funcional somente quando houver testes demonstrando que:

- Os atendimentos são coletados e classificados corretamente.
- Os gatilhos acionam as trilhas previstas.
- Qualidade e conformidade produzem resultados independentes.
- As gravidades e os descontos seguem as regras aprovadas.
- O score geral corresponde à média dos pilares.
- O CSAT original permanece preservado após o abono.
- A revisão final registra correções e mantém o histórico.
- Contestações seguem os critérios de encaminhamento humano.
- Resultados e evidências podem ser rastreados até a conversa original.
- Falhas, tentativas, tokens e custos ficam registrados.
- O processamento pode ser repetido sem gerar duplicidades indevidas.

## 11. Limitações e evolução

Os resultados de IA são sujeitos a erro e precisam ser validados. A classificação automática, os scores, as recomendações de abono e as revisões não substituem a governança das regras de negócio.

Antes de utilizar os resultados para decisões reais sobre desempenho profissional, será necessário validar critérios, amostras, consistência, possíveis vieses e procedimentos de contestação.

A versão inicial será desenvolvida com dados sintéticos, permitindo demonstrar o fluxo completo de ponta a ponta antes de qualquer integração com sistemas reais.

---

**AI Support Intelligence**  
*Automated auditing. Evidence-based decisions. Traceable operations.*
