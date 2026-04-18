# DeckPilot — Documentação do Projeto

## 1. Nome da solução

**DeckPilot**

Uma aplicação web com foco em geração e avaliação de decks de Yu-Gi-Oh! com apoio de inteligência artificial.

---

## 2. Problema escolhido

Montar um deck de Yu-Gi-Oh! pode ser um processo difícil, principalmente para jogadores iniciantes ou para quem deseja testar rapidamente ideias de listas.

Os principais problemas observados são:

* dificuldade em escolher um arquétipo adequado ao estilo do jogador;
* dificuldade em transformar uma ideia em uma lista inicial de deck;
* dificuldade em revisar se a lista criada faz sentido estrategicamente;
* falta de uma experiência simples de conversa para gerar, ajustar e avaliar decks.

O projeto busca resolver isso por meio de uma aplicação onde o usuário conversa com uma IA para criar decks e depois utiliza um avaliador chamado **Deck Doctor** para analisar a qualidade da lista gerada.

---

## 3. Objetivo da aplicação

O objetivo do DeckPilot é permitir que um usuário:

1. converse com uma IA para solicitar um deck;
2. receba uma proposta inicial de lista;
3. refine essa lista ao longo da conversa;
4. visualize o deck gerado no front-end;
5. envie o deck para avaliação automática com o **Deck Doctor**;
6. receba um diagnóstico com resumo, forças, riscos e sugestões.

No estágio atual, o foco está em entregar um **MVP funcional**, priorizando o fluxo principal do produto mesmo que a coerência final dos decks ainda não esteja ideal.

---

## 4. Descrição do caso de uso

### Caso de uso principal

Um jogador acessa o sistema e informa, por meio de um chat, o tipo de deck que deseja montar.

Exemplos:

* “Quero um deck Branded consistente para torneio local.”
* “Não sei qual deck jogar, quero algo forte mas fácil de pilotar.”
* “Deixa esse deck mais barato.”

A IA responde com uma proposta de deck e o sistema tenta validar as cartas com base no catálogo local armazenado no banco. Quando a geração é bem-sucedida, o deck é salvo e exibido na interface.

Depois disso, o usuário pode clicar em **Levar para avaliação**, enviando o deck salvo para o **Deck Doctor**, que produz um diagnóstico textual estruturado.

### Fluxo resumido

1. usuário entra na tela de geração;
2. o front cria uma sessão de chat;
3. o usuário envia uma mensagem;
4. a IA interpreta a intenção e responde com um JSON estruturado;
5. se houver `generated_deck`, o backend valida e salva o deck;
6. o deck aparece no painel lateral;
7. o usuário pode refinar a lista na mesma sessão;
8. o usuário envia o deck para avaliação;
9. o Deck Doctor retorna um parecer sobre a lista.

---

## 5. Tecnologias utilizadas

### Backend

* **Python 3.11**
* **FastAPI**
* **SQLAlchemy**
* **Alembic**
* **Pydantic / pydantic-settings**
* **PostgreSQL / Neon**
* **OpenAI Python SDK** para integração com **Groq** no fluxo de chat
* **google-genai** para integração com **Gemini** no fluxo do Deck Doctor

### Frontend

* **Next.js**
* **React**
* **TypeScript**
* **Tailwind CSS**
* **Axios**

### IA

* **Groq (conta 1)**: usado no chat de geração/refinamento
* **Groq (conta 2)**: usado no Deck Doctor

---

## 6. Arquitetura geral da solução

A solução é dividida em duas partes principais:

### Front-end

Responsável por:

* interface do usuário;
* tela de geração de deck;
* exibição do chat;
* exibição do deck gerado;
* tela de avaliação do deck.

### Back-end

Responsável por:

* persistência dos dados;
* gerenciamento de sessões e mensagens de chat;
* geração de decks com IA;
* validação e salvamento de decks;
* ligação entre sessões de chat e decks gerados;
* avaliação do deck com Deck Doctor.

### Fluxo geral

**Front-end** → chama endpoints do **FastAPI** → backend processa regras e integra com a **IA** → backend salva dados no **PostgreSQL/Neon** → front exibe resultado.

### Visão por módulos

* **cards**: catálogo e importação de cartas;
* **chat**: sessões, mensagens, contexto, orquestração da conversa;
* **decks**: deck, deck cards, validação e diagnóstico;
* **ai**: integração com modelos de linguagem.

---

## 7. Estrutura atual do projeto

### Backend

A estrutura do backend foi organizada por domínio.

#### Exemplo de organização

* `app/models/cards/`
* `app/models/chat/`
* `app/models/decks/`
* `app/models/simulations/`
* `app/services/cards/`
* `app/services/chat/`
* `app/services/decks/`
* `app/services/ai/` *(ou equivalente, dependendo da reorganização final)*

### Frontend

Estrutura mínima atual:

* `src/app/`
* `src/components/chat/`
* `src/components/deck/`
* `src/components/doctor/`
* `src/features/chat/`
* `src/features/deck/`
* `src/features/doctor/`
* `src/lib/`

---

## 8. Instruções de instalação e execução do backend

### Pré-requisitos

* Python 3.11+
* ambiente virtual (`venv`)
* banco PostgreSQL/Neon configurado

### Instalação

1. acessar a pasta do backend;
2. criar e ativar o ambiente virtual;
3. instalar dependências;
4. configurar variáveis de ambiente;
5. aplicar migrations;
6. iniciar a API.

### Exemplo de passos

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Variáveis de ambiente do backend

Exemplo de `.env`:

```env
DATABASE_URL=sua_url_do_neon

GROQ_API_KEY=sua_chave_groq_conta1
LLM1_MODEL=llama-3.3-70b-versatile

GROQ2_API_KEY=sua_chave_groq_conta2
LLM2_MODEL=llama-3.3-70b-versatile
```

### Endereço local padrão

```text
http://127.0.0.1:8000
```

### Documentação automática da API

```text
http://127.0.0.1:8000/docs
```

---

## 9. Instruções de instalação e execução do front-end

### Pré-requisitos

* Node.js
* npm

### Instalação

1. acessar a pasta do front;
2. instalar dependências;
3. configurar `.env.local`;
4. iniciar o servidor do Next.js.

### Exemplo de passos

```bash
npm install
npm run dev
```

### Variáveis de ambiente do front-end

Exemplo de `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Endereço local padrão

```text
http://localhost:3000
```

---

## 10. Explicação de como a IA foi integrada

A IA foi integrada em dois fluxos distintos.

### 10.1 Chat de geração de deck

O chat utiliza atualmente **Groq**.

#### Funcionamento

* o usuário envia uma mensagem;
* o backend monta o contexto da conversa;
* o serviço `chat_ai_service` envia um prompt para a IA;
* a IA retorna um JSON estruturado com:

  * `intent`
  * `reply`
  * `questions`
  * `suggested_archetypes`
  * `deck_request`
  * `generated_deck`
* se houver `generated_deck`, o backend valida as cartas localmente e salva o deck.

### 10.2 Deck Doctor

O Deck Doctor utiliza atualmente **Groq (conta 2)**.

#### Funcionamento

* o usuário escolhe um deck salvo;
* o backend monta uma entrada estruturada com dados do deck e análise básica;
* o serviço `deck_doctor_ai_service` envia o prompt ao Gemini;
* o modelo retorna um JSON com:

  * `summary`
  * `strengths`
  * `risks`
  * `suggestions`

### Estratégia atual de providers

* **Groq (conta 1)** foi mantido no chat por simplicidade e custo reduzido para o MVP;
* **Groq (conta 2)** foi mantido no doctor para separar as cotas e evitar rate limit durante o desenvolvimento.

---

## 11. Funcionalidades implementadas até o momento

### Backend

* CRUD básico relacionado a decks e cartas;
* catálogo local de cartas;
* importação de cartas;
* sessões de chat;
* mensagens de chat;
* geração de deck via IA;
* refinamento de deck na mesma conversa;
* salvamento automático do deck gerado;
* vínculo formal entre sessão de chat e decks gerados;
* histórico de decks gerados por sessão;
* avaliação de deck via Deck Doctor;
* integração com front-end via CORS.

### Frontend

* landing page inicial;
* tela de geração de deck;
* chat conectado ao backend;
* painel lateral exibindo o deck gerado;
* preview de carta em popup com imagem ampliada e descrição;
* card visual de “deck gerado” no chat;
* botão para levar o deck para avaliação;
* tela de avaliação conectada ao doctor.

---

## 12. Exemplos de uso da aplicação

### Exemplo 1 — gerar um deck conhecido

Usuário:

```text
Quero um deck Branded consistente para torneio local.
```

Resultado esperado:

* a IA entende a intenção;
* gera uma lista inicial;
* o backend tenta validar e salvar as cartas;
* o deck aparece no painel lateral.

### Exemplo 2 — descobrir um deck

Usuário:

```text
Não sei qual deck jogar, quero algo forte mas fácil de pilotar.
```

Resultado esperado:

* a IA sugere alguns arquétipos;
* o usuário escolhe um;
* a conversa evolui até gerar uma lista.

### Exemplo 3 — refinar um deck

Usuário:

```text
Agora deixa esse deck mais barato.
```

Resultado esperado:

* a IA usa o deck salvo da conversa como base;
* gera uma nova proposta;
* o sistema salva a nova versão.

### Exemplo 4 — avaliar um deck

Usuário:

* gera ou seleciona um deck;
* clica em **Levar para avaliação**.

Resultado esperado:

* o Deck Doctor analisa a lista;
* a tela de avaliação mostra:

  * resumo;
  * pontos fortes;
  * riscos;
  * sugestões.

---

## 13. Limitações atuais do MVP

O projeto ainda está em fase de MVP, então existem limitações conhecidas.

### 13.1 Coerência dos decks gerados

A IA ainda pode gerar listas incoerentes, incompletas ou com cartas pouco sinérgicas.

### 13.2 Matching de cartas no catálogo

A validação e o salvamento ainda dependem muito de correspondência por nome, o que pode causar:

* cartas inválidas;
* cartas não encontradas;
* decks parcialmente salvos;
* listas com menos cartas do que o esperado.

### 13.3 Qualidade variável do refinamento

O fluxo de refinamento já existe, mas ainda não garante alta qualidade estratégica.

### 13.4 Dependência de prompts

Boa parte do comportamento da IA depende de engenharia de prompt e ainda pode ser instável.

### 13.5 Consumo de tokens

O uso de modelos de IA ainda pode gerar limitações de cota/rate limit, especialmente no Groq.

### 13.6 Cabeçalho simplificado na avaliação

A tela de avaliação ainda pode exibir dados genéricos no topo em vez de todos os metadados reais do deck, dependendo do endpoint utilizado.

---

## 14. Possíveis evoluções futuras

### Melhorias na geração de deck

* melhorar matching de cartas no catálogo;
* usar busca semântica ou fuzzy match;
* reintroduzir ferramentas auxiliares de catálogo com mais controle;
* melhorar consistência estratégica do deck;
* usar regras mais fortes por arquétipo.

### Melhorias na avaliação

* enriquecer o doctor com mais análise estrutural;
* exibir coerência de curva, sinergia e consistência;
* comparar versões do mesmo deck.

### Melhorias de experiência do usuário

* histórico completo de sessões;
* histórico visual de versões de decks;
* seleção de uma versão anterior como base;
* exportação de deck para formatos externos;
* favoritos, tags e organização de decks.

### Melhorias de arquitetura

* separar melhor serviços por domínio;
* refinar organização de models, services e repositories;
* criar testes automatizados para geração e avaliação;
* adicionar observabilidade e logs mais claros para integração com IA.

---

## 15. Estado atual do projeto

No estado atual, o DeckPilot já demonstra o fluxo principal do produto:

* conversar com uma IA;
* gerar uma lista inicial de deck;
* exibir esse deck no front-end;
* salvar a versão gerada;
* levar o deck para avaliação;
* receber um diagnóstico automático.

Mesmo com limitações na coerência da lista, o sistema já cumpre o papel de **MVP funcional**, permitindo validar a proposta de valor da solução.

---