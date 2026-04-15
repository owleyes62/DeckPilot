# DeckPilot

> Your AI-powered Yu-Gi-Oh! deckbuilding copilot.

---

## Nome da Solução

**DeckPilot** — Copiloto de deckbuilding para Yu-Gi-Oh! com geração, diagnóstico e simulação de consistência via IA.

---

## Problema Escolhido

Jogadores de Yu-Gi-Oh! enfrentam uma curva de aprendizado alta na construção de decks: entender quais cartas incluir, quantas cópias de cada, como equilibrar os ratios e o quão consistente o deck será na mão inicial são perguntas difíceis de responder sem experiência ou ferramentas adequadas.

As ferramentas existentes (como o TCG Deck-Rec) recomendam decks, mas não explicam o porquê das escolhas, não validam contra regras reais do jogo e não oferecem uma análise de consistência estatística integrada ao mesmo fluxo.

---

## Objetivo da Aplicação

O DeckPilot oferece um fluxo completo e auditável de deckbuilding:

1. **Gerar** um deck completo (Main/Extra/Side) a partir de um arquétipo ou estilo de jogo
2. **Validar** cada carta sugerida contra uma base de dados real (sem alucinações)
3. **Diagnosticar** o deck com checks determinísticos e sugestões em linguagem natural
4. **Simular** milhares de mãos iniciais via Monte Carlo e interpretar os resultados com IA

---

## Descrição do Caso de Uso

Um jogador quer montar um deck do arquétipo "Branded" para jogar em torneios locais:

1. Acessa o **Deck Generator**, digita "Branded" e o estilo "combo" — a IA gera um deck de 40 cartas (Main/Extra/Side) com resumo da win condition e como pilotar.
2. O deck é validado automaticamente contra a base YGOJSON — cartas inexistentes ou banidas são sinalizadas.
3. O jogador vai ao **Deck Doctor** — o sistema analisa distribuição de tipos, redundâncias, tamanho e gera um diagnóstico com pontos fortes, riscos e sugestões de cortes.
4. No **Hand Simulation**, o sistema roda 10.000 mãos iniciais, exibe a chance de abrir starters, chance de brick e distribuição de mãos jogáveis — a IA interpreta o resultado e sugere ajustes.
5. O jogador exporta o deck final em `.ydk` para usar em simuladores como YGOPro.

---

## Tecnologias Utilizadas

### Front-end
| Tecnologia | Uso |
|---|---|
| Next.js | Framework React para a aplicação web |
| Tailwind CSS | Estilização |
| Axios | Chamadas HTTP para o back-end |
| Vercel | Deploy |

### Back-end
| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| FastAPI | Framework da API REST |
| LangChain | Orquestração do LLM (geração, diagnóstico, interpretação) |
| SQLAlchemy | ORM |
| Alembic | Migrations do banco de dados |
| Railway | Deploy |

### IA e Dados
| Tecnologia | Uso |
|---|---|
| Grok (xAI) | LLM para geração de decks, diagnóstico e interpretação de simulações |
| YGOJSON | Base de dados local de cartas (fonte principal, offline) |
| YGOPRODeck API | Enriquecimento de dados e imagens (fallback/complemento) |

### Banco de Dados
| Tecnologia | Uso |
|---|---|
| PostgreSQL (Neon) | Persistência de decks gerados e histórico de simulações |

### Simulação
| Tecnologia | Uso |
|---|---|
| Python puro | Simulação Monte Carlo de mãos iniciais |

---

## Arquitetura Geral da Solução

```
┌──────────────────────────────────────────────────────┐
│                    FRONT-END                          │
│                Next.js (Vercel)                       │
│                                                       │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────┐ │
│  │    Deck      │ │    Deck      │ │     Hand      │ │
│  │  Generator   │ │   Doctor     │ │  Simulation   │ │
│  └──────┬───────┘ └──────┬───────┘ └──────┬────────┘ │
└─────────┼────────────────┼────────────────┼──────────┘
          └────────────────┼────────────────┘
                           │ HTTP (REST / Axios)
┌──────────────────────────▼───────────────────────────┐
│                    BACK-END                           │
│                FastAPI (Railway)                      │
│                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │  /deck      │  │  /doctor    │  │  /simulation │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘  │
│         │                │                │           │
│  ┌──────▼────────────────▼────────────────▼───────┐   │
│  │                   Services                     │   │
│  │                                                │   │
│  │  ┌────────────┐  ┌──────────┐  ┌───────────┐  │   │
│  │  │ LangChain  │  │  Deck    │  │  Monte    │  │   │
│  │  │ + Grok LLM │  │Validator │  │  Carlo    │  │   │
│  │  └────────────┘  └──────────┘  └───────────┘  │   │
│  │                                                │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │           Card Repository               │   │   │
│  │  │   YGOJSON (local) + YGOPRODeck (API)    │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └────────────────────────┬───────────────────────┘   │
└───────────────────────────┼───────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │    PostgreSQL (Neon)   │
                │ decks / simulations /  │
                │       history         │
                └───────────────────────┘
```

### Fluxo completo

```
Usuário informa arquétipo / estilo
         ↓
LangChain + Grok gera deck em JSON estruturado
         ↓
Validação contra YGOJSON (carta existe? está banida?)
         ↓
Deck Doctor — checks determinísticos + LLM diagnóstico
         ↓
Monte Carlo — simulação de mãos + LLM interpreta
         ↓
Export .ydk + persistência no Neon
```

### Estrutura do repositório

```
/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                    # Deck Generator
│   │   ├── doctor/page.tsx             # Deck Doctor
│   │   └── simulation/page.tsx         # Hand Simulation
│   ├── components/
│   │   ├── DeckList.tsx
│   │   ├── DiagnosticReport.tsx
│   │   └── SimulationChart.tsx
│   ├── lib/
│   │   └── api.ts                      # Axios client
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── deck.py             # Geração e export
│   │   │       ├── doctor.py           # Diagnóstico
│   │   │       └── simulation.py       # Monte Carlo
│   │   ├── core/
│   │   │   ├── config.py               # Settings / env vars
│   │   │   └── database.py             # Conexão Neon
│   │   ├── models/                     # SQLAlchemy models
│   │   ├── schemas/                    # Pydantic schemas
│   │   ├── repositories/               # Acesso ao banco
│   │   └── services/
│   │       ├── deck_generator.py       # LangChain + Grok
│   │       ├── deck_validator.py       # Validação contra YGOJSON
│   │       ├── deck_doctor.py          # Heurísticas + LLM
│   │       ├── simulation.py           # Monte Carlo
│   │       └── card_repository.py      # YGOJSON + YGOPRODeck
│   ├── data/
│   │   └── ygojson/                    # Base local de cartas
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
│
├── DOCS.md
└── README.md
```

---

## Instruções de Instalação e Execução

### Pré-requisitos

- Node.js 18+
- Python 3.11+
- Conta no [Neon](https://neon.tech) (PostgreSQL gratuito)
- Chave de API da [xAI (Grok)](https://console.x.ai)

---

### Back-end

```bash
# 1. Entrar na pasta do back-end
cd backend

# 2. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves:
# DATABASE_URL=postgresql://...
# XAI_API_KEY=...

# 5. Baixar base YGOJSON
# Copiar os arquivos JSON para backend/data/ygojson/

# 6. Rodar as migrations
alembic upgrade head

# 7. Iniciar o servidor
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.
Documentação automática em `http://localhost:8000/docs`.

---

### Front-end

```bash
# 1. Entrar na pasta do front-end
cd frontend

# 2. Instalar dependências
npm install

# 3. Configurar variáveis de ambiente
cp .env.example .env.local
# Editar .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Iniciar o servidor de desenvolvimento
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`.

---

## Como a IA Foi Integrada

A IA participa em três momentos distintos do fluxo, sempre combinada com lógica determinística:

### 1. Deck Generator — LangChain + Grok

O LLM recebe o arquétipo/estilo e gera o deck em JSON estruturado com main, extra e side deck. O output é obrigatoriamente validado contra a base YGOJSON antes de ser exibido — qualquer carta inexistente ou banida é removida e sinalizada.

```python
# Exemplo simplificado — services/deck_generator.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = """Você é um especialista em Yu-Gi-Oh! TCG.
Gere um deck completo para o arquétipo "{archetype}" com estilo "{style}".
Retorne SOMENTE um JSON válido com as chaves: main (40 cartas), extra (até 15), side (até 15).
Cada carta deve ter: name (str), copies (1-3).
Inclua também: win_condition (str) e how_to_pilot (str)."""

chain = LLMChain(llm=grok_llm, prompt=PromptTemplate(...))
```

### 2. Deck Doctor — Heurísticas + Grok

Checks determinísticos são executados primeiro (tamanho do deck, limites de cópias, distribuição de tipos, redundâncias). O resultado dessas regras é então enviado ao LLM, que redige o diagnóstico em linguagem natural com justificativas para cada sugestão.

### 3. Hand Simulation — Monte Carlo + Grok

A simulação roda em Python puro: 10.000 iterações de mãos iniciais de 5 cartas, calculando probabilidades de abrir starters, bricks e mãos jogáveis. O resultado estatístico é enviado ao LLM, que o interpreta e sugere ajustes concretos no deck.

---

## Exemplos de Uso da Aplicação

### Gerar um deck
- Página: **Deck Generator**
- Ação: Digitar "Swordsoul" + selecionar estilo "combo" → clicar em "Generate"
- Resultado: Deck de 40 cartas (Main/Extra/Side) + resumo da win condition + botão de export `.ydk`

### Diagnosticar um deck
- Página: **Deck Doctor**
- Ação: Colar uma decklist ou usar o deck gerado → clicar em "Diagnose"
- Resultado: Relatório com pontos fortes, riscos, sugestões de cortes e adições com justificativas

### Simular consistência
- Página: **Hand Simulation**
- Ação: Selecionar o deck → clicar em "Simulate"
- Resultado: Gráficos com chance de abrir starters, chance de brick + interpretação da IA com sugestões

---

## Limitações Atuais do MVP

- A base YGOJSON precisa ser baixada e mantida manualmente (sem atualização automática)
- O LLM pode ocasionalmente sugerir cartas com nomes ligeiramente errados — a validação corrige, mas pode reduzir o deck
- A simulação não considera a ordem de jogo (primeiro ou segundo) nem efeitos específicos das cartas
- Não há autenticação — qualquer usuário acessa todos os decks salvos
- O Deck Doctor não cobre todas as interações entre arquétipos
- Sem suporte a importação de decks no formato `.ydk` ainda

---

## Possíveis Evoluções Futuras

- **Import `.ydk`**: permitir importar decks prontos de simuladores para diagnóstico
- **Atualização automática da base**: sincronizar YGOJSON periodicamente via job agendado
- **Simulação avançada**: considerar efeitos de cartas, ordem de jogo e going first/second
- **Autenticação e perfis**: salvar coleção pessoal de decks por usuário
- **Metagame awareness**: integrar dados de torneios recentes para sugerir decks competitivos
- **Comparador de decks**: comparar dois decks lado a lado em consistência e diagnóstico
- **Histórico de versões**: acompanhar a evolução de um deck ao longo do tempo