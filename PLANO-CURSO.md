# Plano do curso — openpcbot v3: seu Jarvis local

Formato: `formato-curso-v2` (INEMA.CLUB, dark âmbar + camada de aprendizagem). Self-contained,
abre em `file://`, publica no GitHub Pages da raiz (`inematds/curso-openpcbotv3`).

- **courseId** (`<meta name="inema-course">` e `manifest.course`): `curso-openpcbotv3`
- **Título:** openpcbot v3: seu Jarvis local
- **Subtítulo:** assistente pessoal multicanal com fila durável, cérebro com memória e custo por chamada, rodando na sua máquina
- **Público:** quem vai instalar, usar e configurar o v3 (o Nei hoje; qualquer pessoa técnica que clone o repo). Define termos na primeira aparição (erro #31).
- **Fonte de verdade do conteúdo:** `~/projetos/openpcbotv3/README.md` (seções 1 a 15, incluindo 9b), `CHANGELOG.md` (3.0.0 a 3.2.3), `CLAUDE.md`, `docs/CONECTORES.md`, `docs/INCORPORAR-V3.md`, `PLANO-MIGRACAO-V3.md`. Nada inventado: comando, flag, arquivo e número saem desses arquivos. Se não estiver lá, não entra.
- **Template de estrutura:** os arquivos já em `curso/trilhaN/index.html` e `modulo-N-1.html` (copiados de `curso-open-source-ai-v2`). Manter nav, CSS, snippets, medidores, `data-inema-*`, TOC. Trocar TODO o conteúdo.

## Trilhas e módulos (4 trilhas × 2 módulos, 6 tópicos cada = 48 tópicos)

### Trilha 1 · Fundamentos (emerald) — "Entenda o que roda"
- **1.1 O que é o openpcbot v3** · 🧠 · "Um Jarvis que cabe na sua máquina"
  Tópicos: (1) assistente pessoal multicanal: Telegram, CLI, HTTP; (2) as seis camadas: canais, bus, fila, orquestrador, cérebro, gestor do Ollama, custo; (3) de onde veio: v1 → v2 (`openpcbot`, `@inemaclaudebot`) → v3 ao lado (`@inemav3bot`, porta 3142), estrangulamento, não corte; (4) o que roda local e o que vai pra nuvem: Ollama (custo zero) vs OpenRouter/Claude por tier; (5) regras de ouro (módulo ≤500 linhas, toda chamada de LLM pelo gateway, Ollama só via systemd, sem mídia paga sem confirmação); (6) o que ele já faz hoje (3.2.3) e o que ainda não (fase 8, fase 10).
- **1.2 O caminho de uma mensagem** · 🔀 · "Do Telegram ao resultado, passo a passo"
  Tópicos: (1) adaptador de canal publica no bus; chats que respondem vs chats observados; (2) janela `collect` de 2 s e os outros modos; (3) roteador em Ollama pequeno decide direto vs agente e o tier; (4) resposta direta: identidade + persona + USER.md + memória em 3 camadas + histórico; (5) agente: job na lane `agente`, `claude -p`, especialistas read-only em paralelo + lead, sessão retomada; (6) depois da resposta: turno logado, memória com regex PT-BR, proposta pro vault, custo em `chamadas_llm`.

### Trilha 2 · Instalar e operar (blue) — "Coloque no ar e mantenha no ar"
- **2.1 Subir o v3** · 🚀 · "Do clone ao serviço em 20 minutos"
  Tópicos: (1) pré-requisitos: Node, Ollama como serviço systemd na 11434, `claude` CLI, `.env` do v2 pras keys compartilhadas; (2) bot próprio no BotFather e `TELEGRAM_BOT_TOKEN_V3` (o token do v2 é recusado); (3) `.env` do v3: `ALLOWED_CHAT_ID`, `PORT_V3`, `PISO_RAM_GB`, `ORCAMENTO_MENSAL_USD`, `DASHBOARD_TOKEN_V3`, `HTTP_BIND_V3`; (4) `config/*.yaml`: `ollama.yaml` (papéis roteador/geral/embed, mesmas tags do v2), `precos.yaml`, `orcamento.yaml`; (5) `bash scripts/instalar-servico.sh`: build, unit `--user`, `MemoryMax=2G`, restart sem sudo; (6) primeira conversa: `/versao`, `/health`, `/chatid`, `npm run cli`.
- **2.2 Operar no dia a dia** · 🩺 · "Diagnóstico, logs e o que fazer quando quebra"
  Tópicos: (1) `npm run doctor` (o que cada linha checa) e `npm run doctor -- --deep` (4 probes reais); (2) `journalctl --user -u openpcbotv3` e o dashboard em `:3142/`; (3) `/health`, `/status`, `/usage`: ler fila, Ollama, RAM, custo; (4) alertas no Telegram com dedupe (Ollama fora, RAM baixa, lease morto, zumbi, 3 falhas, orçamento 70/100 %); (5) backup noturno `VACUUM INTO` + `age`/gzip, retenção 14, e restauração; (6) quando quebra: `FALHAS.md` (uma linha por falha), restart, `/parar tudo`, garantias de memória na coexistência (nunca descarregar modelo alheio).

### Trilha 3 · Usar no dia a dia (purple) — "Converse, delegue, lembre"
- **3.1 Comandos e conversa** · 💬 · "Tudo que o bot entende"
  Tópicos: (1) mapa dos comandos por grupo (fila, custo, saúde, memória, tarefas, cron, controle da conversa); (2) fila na prática: `/status [id]`, `/cancelar`, `/prioridade`, lanes `chat|agente|ollama|cron|io`; (3) `/tarefa add [quando] <texto>`, formatos de `quando`, lembretes, `/daily` às 8h; (4) `/cron lista|on|off` e os jobs padrão (lembretes, indexar-memoria, decaimento, consolidacao-noturna, backup-noturno, daily-8h); (5) `/agentes`, `/skills`, `/novo` vs `/compress`; (6) pedir trabalho de agente: como escrever o pedido, acompanhar com `/status N`, o que volta e onde fica (`store/saidas`).
- **3.2 Cérebro e conectores** · 🧬 · "Memória que aprende com você"
  Tópicos: (1) o que o cérebro guarda: `memories` (FTS5 + salience), vetores bge-m3, `conversation_log`, insights; (2) `/memoria lista|buscar|salvar|esquecer` e o retrieval em 3 camadas com teto de tokens; (3) vault: `MEMORY.md` e `USER.md`, propostas automáticas, `/memoria propostas|aprovar|descartar`; (4) consolidação noturna: duplicatas, contradições → `superseded`, insights, `/consolidar`; (5) conectores: várias contas Gmail, várias agendas, Telegram observado (`/fontes`, `/fontes ingerir gmail|agenda`, `docs/CONECTORES.md`, credencial Google uma vez, `token_gmail_<conta>.json`); (6) o que a memória ainda não faz (frase inteira, não fato extraído) e como corrigir uma memória errada.

### Trilha 4 · Configurar e estender (amber) — "Deixe o Jarvis com a sua cara"
- **4.1 Controle da conversa** · 🎛️ · "Parar, priorizar, dar voz"
  Tópicos: (1) interruptores `/parar tudo|agentes|<agente> [motivo]` e `/retomar`: o que bloqueia, o que continua, persistência em `prefs`, o limite de 30 s; (2) modos de fila `/fila collect|followup|steer|interrupt` com a diferença honesta pro OpenClaw (steer não injeta no agente; interrupt descarta resposta em voo por geração); (3) persona em 3 camadas: `IDENTIDADE.md`, `agents/<id>/SOUL.md`, `personalidades/<nome>.md` + `/personality`; (4) `/context [detail]`: ler o custo fixo do prompt e cortar overhead; (5) `mcp_config` por agente com `--strict-mcp-config`; (6) `/ajuda <comando>` e o CHANGELOG 3.2.x como fonte.
- **4.2 Agentes, skills, custo e o que vem** · 🧩 · "Estenda sem quebrar"
  Tópicos: (1) `agents/<id>/agent.yaml` + `CLAUDE.md`: modelo (alias opus/sonnet/haiku/fable), effort, `read_only`, `cwd`; especialistas vs lead; (2) `skills/<id>/SKILL.md`: só metadata entra no prompt, rascunhos em `skills/_rascunhos/`, as 15 skills herdadas do v2; (3) custo: tiers local→barato→premium, `precos.yaml`, orçamento com aviso 70 % e trava 100 %, `/usage` por tier e agente; (4) gestor do Ollama: papéis, 1 modelo grande residente, preflight de RAM, `descarregar_alheios: false`, `/ollama preflight <m>`; (5) canais extras: Slack (probe OAuth, desligado até o corte), WhatsApp (recusa enquanto o v2 é dono), HTTP `POST /mensagem`; (6) roadmap: fase 8 (corte, só com ordem), fase 10 (cliente MCP no caminho Ollama, servidor MCP do inemavox, voz no Telegram), `docs/INCORPORAR-V3.md` e o que Hermes/OpenClaw ensinaram.

## Regras de conteúdo (além dos erros críticos da skill)

- Sem travessão em nenhum texto (regra da identidade do projeto). Sem clichê.
- Todo comando, flag, arquivo e número vem da fonte de verdade. Marcar variável com `<isto-voce-troca>`.
- Cada módulo: 6 tópicos, 500 a 800 linhas, ≥2 SVG futuristas inline (cor da trilha + ciano `#38bdf8`, `role="img"` + `aria-label` que ensina), ≥2 grids ✓/✗, ≥1 timeline, ≥2 tip boxes, ≥1 code box copy-run com objetivo + bloco + como verificar (módulos práticos: todos exceto 1.1, que ainda tem ≥1 code box de `/versao`).
- Módulos de fundamento (1.1, 1.2) definem cada termo na primeira vez ("Novo aqui?").
- IDs: `data-inema-topic="modulo-N-M#topico-K"`, `data-inema-module="N-M"`, `data-inema-block="mN-M-tK-pJ"`.
- Manifesto idêntico em todas as páginas (o `index.html` da raiz é a referência; um script confere).
