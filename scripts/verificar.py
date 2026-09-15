#!/usr/bin/env python3
"""Verificação mecânica do curso (erros críticos que dá pra checar por grep).
Roda da raiz do repo: python3 scripts/verificar.py. Sai com 1 se algo falhar."""
import glob, json, re, sys

falhas = []
def falha(f, msg): falhas.append(f"{f}: {msg}")

raiz = open('index.html', encoding='utf8').read()
m = re.search(r'<script type="application/json" data-inema-manifest>(.*?)</script>', raiz, re.S)
manifesto = m.group(1).strip() if m else ''
man = json.loads(manifesto)
topicos_esperados = {mod['id']: mod['topics'] for t in man['tracks'] for mod in t['modules']}
hrefs = {mod['id']: mod['href'] for t in man['tracks'] for mod in t['modules']}

paginas = ['index.html'] + sorted(glob.glob('curso/*/*.html'))
for f in paginas:
    s = open(f, encoding='utf8').read()
    mm = re.search(r'<script type="application/json" data-inema-manifest>(.*?)</script>', s, re.S)
    if not mm or mm.group(1).strip() != manifesto: falha(f, 'manifesto ausente ou diferente da raiz')
    if '<meta name="inema-course" content="curso-openpcbotv3">' not in s: falha(f, 'meta inema-course errado')
    if '—' in s: falha(f, f'{s.count("—")} travessão(ões)')
    if 'justify-center' in re.sub(r'<svg.*?</svg>', '', s, flags=re.S): falha(f, 'justify-center presente')
    if 'inema.pro' not in s: falha(f, 'link PRO ausente')
    if 'text-sky-400' not in s or 'inema.club' not in s: falha(f, 'link INEMA.CLUB ausente')
    if 'learn.css' not in s or 'learn.js' not in s or 'INEMA.init' not in s: falha(f, 'camada de aprendizagem incompleta')
    if not re.search(r'<head>\s*<meta charset[^>]*>\s*<meta name="viewport"[^>]*>\s*<meta name="inema-course"[^>]*>\s*<script>\s*\(function', s): falha(f, 'anti-FOUC não é o primeiro script do head')
    for velho in ['Command Center', 'open-source-ai', 'Seguro mental', 'Opere com estabilidade', 'Stack Local', 'Escolha o modelo certo', 'Monte o painel']:
        if velho in s: falha(f, f'resíduo do template: {velho}')
    for rotulo in ['Fundamentos', 'Instalar e operar', 'Usar no dia a dia', 'Configurar e estender']:
        if rotulo not in s: falha(f, f'nav sem o rótulo "{rotulo}"')
    if '.dark .border-dark-600' not in s or '.dark .divide-dark-600' not in s: falha(f, 'bordas suavizadas (dark) incompletas')

    mod = re.search(r'curso/trilha(\d)/modulo-(\d-\d)\.html', f)
    if mod:
        n, mid = mod.groups()
        linhas = s.count('\n') + 1
        if not 500 <= linhas <= 900: falha(f, f'{linhas} linhas (esperado 500 a 800)')
        top = re.findall(r'data-inema-topic="modulo-' + mid + r'#topico-(\d)"', s)
        if sorted(top) != [str(i) for i in range(1, 7)] or len(top) != 6: falha(f, f'data-inema-topic: {top}')
        if topicos_esperados.get(mid) != 6: falha(f, 'manifesto topics != 6')
        if f'data-inema-module="{mid}"' not in s: falha(f, 'data-inema-module ausente')
        if len(re.findall(r'<svg[^>]*role="img"', s)) < 2: falha(f, 'menos de 2 SVG role=img')
        if 'aria-pressed' not in s: falha(f, 'marcar-lido sem aria-pressed')
        if 'Resumo do' not in s: falha(f, 'sem resumo do módulo')
        if not re.search(r'<title>Módulo ' + mid.replace('-', '.') + r': .+\| openpcbot v3: seu Jarvis local</title>', s): falha(f, 'title fora do padrão')
        if s.count('data-inema-block=') < 12: falha(f, 'poucos blocos anotáveis')
        if 'scroll-margin-top' not in s: falha(f, 'sem scroll-margin-top')
    idx = re.search(r'curso/trilha(\d)/index\.html', f)
    if idx:
        n = idx.group(1)
        if 'Mapa da trilha' not in s: falha(f, 'sem "Mapa da trilha"')
        if 'Navegacao Rapida' in s or 'Navegação Rápida' in s: falha(f, 'usa "Navegação Rápida"')
        for k in ('1', '2'):
            mid = f'{n}-{k}'
            if f'<iframe src="modulo-{mid}.html"' not in s and f"<iframe src='modulo-{mid}.html'" not in s: falha(f, f'modal sem iframe do módulo {mid}')
            if f'href="modulo-{mid}.html"' not in s: falha(f, f'sem "Ver Completo" do módulo {mid}')
            if f'id="modulo-{mid}"' not in s: falha(f, f'card sem id modulo-{mid}')
            if f'data-inema-meter="modulo:{mid}"' not in s: falha(f, f'sem medidor do módulo {mid}')
        if f'data-inema-meter="trilha:{n}"' not in s: falha(f, 'sem medidor da trilha')
        if len(re.findall(r'<svg[^>]*role="img"', s)) < 1: falha(f, 'sem hero SVG')
        if 'Conteúdo detalhado' not in s and 'Conteudo detalhado' not in s: falha(f, 'sem "Conteúdo detalhado"')
        if s.count('aria-expanded') < 12: falha(f, f'accordions: {s.count("aria-expanded")} aria-expanded (esperado ≥12)')
        if not re.search(r'<title>Trilha ' + n + r': .+\| openpcbot v3: seu Jarvis local</title>', s): falha(f, 'title fora do padrão')

for mid, href in hrefs.items():
    if href not in paginas: falha('manifest', f'href inexistente {href}')

print(f'{len(paginas)} páginas verificadas')
for x in falhas: print('❌', x)
print('OK' if not falhas else f'{len(falhas)} falha(s)')
sys.exit(1 if falhas else 0)
