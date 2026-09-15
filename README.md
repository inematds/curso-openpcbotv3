# Curso: openpcbot v3, seu Jarvis local

Curso completo sobre o [openpcbotv3](https://github.com/inematds/openpcbotv3): o que é, como instalar e operar, como usar no dia a dia e como configurar e estender. Formato INEMA.CLUB v2 (dark âmbar com camada de aprendizagem: progresso, marcar lido, dúvidas, anotações, minha jornada, temas).

**No ar:** https://inematds.github.io/curso-openpcbotv3/

## Trilhas

| # | Trilha | Módulos |
|---|---|---|
| 1 | Fundamentos | 1.1 O que é o openpcbot v3 · 1.2 O caminho de uma mensagem |
| 2 | Instalar e operar | 2.1 Subir o v3 · 2.2 Operar no dia a dia |
| 3 | Usar no dia a dia | 3.1 Comandos e conversa · 3.2 Cérebro e conectores |
| 4 | Configurar e estender | 4.1 Controle da conversa · 4.2 Agentes, skills, custo e o que vem |

8 módulos, 48 tópicos, cerca de 6 horas. Conteúdo espelha a versão **3.2.3** do projeto (2026-09-14); a fonte de verdade é o `README.md` e o `CHANGELOG.md` do openpcbotv3.

## Como rodar local

Abra `index.html` no navegador. Não há build nem servidor: HTML + Tailwind via CDN + JS inline; funciona em `file://`.

## Estrutura

```
index.html            landing (mapa do curso, progresso, minha jornada)
curso/trilhaN/        index.html (mapa da trilha, cards, modais) + modulo-N-1.html, modulo-N-2.html
assets/               learn.css, learn.js (camada de aprendizagem)
capa/capa.png         capa oficial 1280x720
manifest.json         estrutura do curso (o mesmo JSON embutido em toda página)
scripts/verificar.py  checagem mecânica dos erros críticos do formato
PLANO-CURSO.md        plano tópico a tópico
```

## Manutenção

Mudou o projeto? Atualize o módulo correspondente e rode `python3 scripts/verificar.py` antes do push. O manifesto embutido precisa ser idêntico em todas as páginas (o script confere).
