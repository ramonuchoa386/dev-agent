# GitHub Multi-Agent Automation System

Sistema multi-agent que automatiza a resolução de issues em repositórios, integrando análise, planejamento e execução de alterações em código.  
A arquitetura utiliza **LangGraph** para orquestração dos agentes e **ChromaDB** como memória persistente de repositórios, garantindo eficiência e aprendizado contínuo.

---

## Visão Geral

O sistema foi projetado para atuar como um **copiloto inteligente de manutenção de software**.  
Ele identifica issues, analisa o repositório, planeja as alterações necessárias e executa modificações automatizadas em código, gerando um Pull Request pronto para revisão.

---

## Arquitetura

### Fluxos de Decisão
- **Verificação no ChromaDB**: se o repositório já foi indexado, pula esta etapa.  
- **Validação de contexto**: garante que há informação suficiente antes de aplicar uma correção.  

### Agentes (LangGraph)
1. **Agent de Análise**: interpreta a issue e identifica possíveis causas.  
2. **Agent de Planejamento**: define quais arquivos devem ser modificados.  
3. **Agent de Execução**: realiza clone, cria branch, aplica alterações e abre Pull Request.  

### Operações Git Automatizadas
- Clone do repositório  
- Criação de branch a partir da branch da issue  
- Alteração dos arquivos identificados  
- Commit e push  
- Criação de Pull Request  
- Notificação por e-mail  

---

## Principais Recursos

- **Concorrência**: locks de repositórios e filas para evitar conflitos.  
- **Segurança**: sandbox de testes, análise de impacto e verificação de dependências.  
- **Qualidade**: testes automatizados obrigatórios e retry inteligente.  
- **Feedback Loop**: aprendizado contínuo baseado em PRs aprovados/rejeitados.  
- **Observabilidade**: dashboards em tempo real, métricas e monitoramento de filas.  
- **Fallback**: múltiplas abordagens em caso de falha e degradação controlada do sistema.  

---

## Tecnologias

- **LangGraph**: orquestração de agentes  
- **ChromaDB**: memória persistente e otimização de consultas  
- **FastAPI**: API REST para webhooks do GitHub  
- **Ollama (CodeLlama)**: modificação de código local  
- **Docker**: containerização e deploy simplificado  

---

## Diagrama da Arquitetura

```mermaid
graph TD
    A[Notificação de Issue do GitHub] --> A1[Lock de repo]
    A1 --> A2{Repo processando?}
    A2 -->|Sim| A3[Queue]
    A2 -->|Não| B{Repo no ChromaDB?}
    
    B -->|Não| C[Clonar Repo<br/>Branch da Issue]
    B -->|Sim| B1[Verificar se ChromaDB<br/>está atualizado]
    
    B1 -->|Desatualizado| C
    B1 -->|Atualizado| G[Carregar dados do ChromaDB]
    
    C --> C1{Branch existe e<br/>está atualizada?}
    C1 -->|Não| ERR1[Branch inválida]
    C1 -->|Sim| D[Indexar Código Fonte<br/>no ChromaDB]
    
    D --> E[Repo indexado com sucesso]
    E --> F[Agent: Análise do Erro]
    G --> F
    
    F --> F1[Log: Iniciando análise]
    F1 --> H{Informação suficiente<br/>para entender o erro?}
    
    H -->|Não| H1[Tentar estratégias alternativas]
    H1 --> H2{Alternativa encontrada?}
    H2 -->|Não| I[Informação insuficiente<br/>Classificar e notificar]
    H2 -->|Sim| J
    H -->|Sim| J[Output: Análise detalhada do erro]
    
    J --> J1[Agent: Análise de Impacto e Segurança]
    J1 --> J2{Alteração segura?}
    J2 -->|Não| ERR2[Alteração muito arriscada]
    J2 -->|Sim| K[Agent: Planejamento de Correção<br/>Prompt enriquecido com ChromaDB]
    
    K --> K1[Analisar dependências<br/>e compatibilidade]
    K1 --> L[Output: Plano de correção<br/>com lista de arquivos]
    
    L --> M[Agent: Execução em Sandbox]
    M --> M1[Criar ambiente isolado]
    M1 --> N[Clonar repo localmente]
    N --> O[Criar nova branch<br/>a partir da branch da issue]
    O --> P[Aplicar alterações<br/>conforme planejamento]
    
    P --> P1[Executar testes automatizados]
    P1 --> P2{Todos os testes passaram?}
    P2 -->|Não| P3[Retry com correções]
    P3 --> P4{Tentativas < limite?}
    P4 -->|Sim| P
    P4 -->|Não| ERR3[Falha nos testes]
    
    P2 -->|Sim| Q[Code review automatizado]
    Q --> Q1{Passou na validação<br/>de segurança?}
    Q1 -->|Não| ERR4[Problemas de segurança]
    Q1 -->|Sim| R[Criar commit com<br/>mensagem descritiva]
    
    R --> S[Push das alterações<br/>para repositório remoto]
    S --> T[Criar Pull Request<br/>com contexto detalhado]
    T --> T1[Notificar stakeholders]
    T1 --> T2[Registrar métricas<br/>de sucesso]
    T2 --> T3[Liberar lock do repositório]
    T3 --> U[Processo concluído com sucesso]
    
    %% Tratamento de Erros
    ERR1 --> ERR_HANDLER[Handler de Erro]
    ERR2 --> ERR_HANDLER
    ERR3 --> ERR_HANDLER
    ERR4 --> ERR_HANDLER
    I --> ERR_HANDLER
    
    ERR_HANDLER --> ERR5[Log detalhado do erro]
    ERR5 --> ERR6[Notificar com contexto]
    ERR6 --> ERR7[Atualizar métricas]
    ERR7 --> ERR8[Liberar lock]
    ERR8 --> V[Processo interrompido com contexto]
    
    %% Feedback Loop
    U --> FB1[Aguardar feedback do PR]
    FB1 --> FB2{PR foi aprovado/rejeitado?}
    FB2 -->|Rejeitado| FB3[Aprender com rejeição<br/>Ajustar prompts]
    FB2 -->|Aprovado| FB4[Registrar sucesso<br/>Reforçar padrões]
    FB3 --> FB5[Salvar lições aprendidas]
    FB4 --> FB5
    
    %% Monitoramento
    A3 --> MON1[Dashboard: Fila]
    F1 --> MON2[Dashboard: Análise]
    P1 --> MON3[Dashboard: Testes]
    T2 --> MON4[Dashboard: Sucesso]
    ERR7 --> MON5[Dashboard: Erros]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style H fill:#fff3e0
    style J2 fill:#fff3e0
    style P2 fill:#fff3e0
    style Q1 fill:#fff3e0
    style F fill:#e8f5e8
    style K fill:#e8f5e8
    style M fill:#e8f5e8
    style J1 fill:#e8f5e8
    style U fill:#c8e6c9
    style V fill:#ffcdd2
    style ERR1 fill:#ffcdd2
    style ERR2 fill:#ffcdd2
    style ERR3 fill:#ffcdd2
    style ERR4 fill:#ffcdd2
    style ERR_HANDLER fill:#fff3e0
    style FB3 fill:#e3f2fd
    style FB4 fill:#e8f5e8
    style A1 fill:#f3e5f5
    style M1 fill:#fff8e1
    
    classDef agent fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef action fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef success fill:#c8e6c9,stroke:#4caf50,stroke-width:3px
    classDef error fill:#ffcdd2,stroke:#f44336,stroke-width:3px
    classDef security fill:#fff8e1,stroke:#ffc107,stroke-width:2px
    classDef feedback fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef monitor fill:#f1f8e9,stroke:#8bc34a,stroke-width:1px
    
    class F,K,M,J1 agent
    class B,H,J2,P2,Q1,H2,P4,C1,FB2 decision
    class C,D,N,O,P,R,S,T,T1,A1 action
    class U success
    class ERR1,ERR2,ERR3,ERR4,V error
    class M1,Q security
    class FB3,FB4,FB5 feedback
    class MON1,MON2,MON3,MON4,MON5 monitor
````

---

## Setup

```bash
cp .env.example .env   # configure variáveis
docker-compose up -d   # iniciar serviços
docker exec -it github-automation-ollama ollama pull codellama:7b
python config/setup.py # adicionar configuração de repositório
```

---

## Configuração do GitHub Webhook

1. Acesse: `Settings > Webhooks` no repositório GitHub
2. Adicione: `http://your-domain:8000/webhook/github`
3. Selecione evento: `Issues`
4. Content type: `application/json`

---

## Fluxo de Trabalho

1. Issue é criada e marcada com label (ex: `bug`).
2. Webhook envia evento para o sistema.
3. O **Agent de Análise** interpreta a issue.
4. O **Agent de Planejamento** define arquivos a alterar.
5. O **Agent de Execução** aplica modificações e abre PR.
6. Desenvolvedor recebe notificação e pode revisar o PR.
7. Feedback (merge ou rejeição) é armazenado no ChromaDB para aprendizado.

---

## Exemplo de Issue (Input)

```json
{
  "id": 123,
  "title": "Bug: versão incorreta em app.json",
  "body": "A versão configurada no arquivo src/config/app.json não está atualizada.",
  "labels": ["bug"],
  "repository": "github.com/org/project"
}
```

---

## Exemplo de Pull Request (Output)

```text
Title: Fix: Ajuste de configuração em app.json

Body:
Este PR foi gerado automaticamente pelo sistema multi-agent.

- Issue: #123
- Alterações aplicadas:
  - src/config/app.json (atualização de versão)
  - package.json (atualização de dependências)
- Testes executados em ambiente sandbox
- Code review automatizado aprovado

Por favor, revise as alterações antes do merge.
```

---

## Monitoramento

```bash
# Logs do sistema
docker logs github-automation-agent-1 -f

# Status dos serviços
docker-compose ps
```

---

## Estrutura do Projeto

```
project/
├── agents/
│   ├── base_agent.py
│   ├── webhook_processor.py
│   ├── repository_analyzer.py
│   ├── code_modifier.py
│   └── pr_creator.py
├── services/
│   ├── rag_service.py
│   ├── git_service.py
│   └── github_service.py
├── models/
│   └── schemas.py
├── workflow/
│   └── graph.py
├── config/
│   └── setup.py
├── tests/
│   ├── test_agents.py
│   ├── test_services.py
│   └── test_workflow.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── main.py
└── README.md
```

---

## Personalização

Para adaptar o sistema a novos cenários:

1. Crie novos agentes herdando de `BaseAgent`.
2. Implemente o método `execute()`.
3. Adicione o agente ao workflow (`workflow/graph.py`).
4. Ajuste regras de decisão em `should_continue()`.