# Pulso / Running motions

## Novo: GET → KEEP RUNNING

[HTML editável](motions/get-keep/index.html) · [MP4 1080 × 1920](assets/get-keep-running.mp4)

Animação de impacto, 10 segundos, 9:16, baseada no asset enviado pelo usuário. Lettering verde arredondado reconstruído manualmente em contornos vetoriais. Aos 5 segundos, GET sai e KEEP entra, mantendo RUNNING. Linhas de pista, rastros, zoom em detalhes, cortes de cor e chevrons reforçam a aceleração. Sem áudio. A palavra KEEP usa desenhos compatíveis com a referência; não se afirma extração exata do asset original.

`motions/get-keep/index.html` é autossuficiente e funciona sem dependências de rede. Inclui pausa, repetição, linha do tempo e respeito a movimento reduzido. Fonte da interface depende do sistema; lettering principal usa os mesmos caminhos vetoriais em qualquer computador.

Fontes editáveis: `motions/get-keep/source.js` (animação), `lettering.json` (contornos) e `build.py` (gera HTML independente e prova SVG). Depois de editar JS ou JSON, execute `python motions/get-keep/build.py`. A prova SVG está em `motions/get-keep/lettering-proof.svg`. A referência visual fornecida pelo usuário mantém os direitos de seu titular; a licença MIT do código não altera esses direitos.

[Relatório de teste do novo motion](tests/GET_KEEP_REPORT.md).

<img src="assets/get-keep-preview.png" width="280" alt="KEEP RUNNING: lettering arredondado branco sobre verde, com linhas de velocidade">

## Run culture / versão anterior

Filme vertical de tipografia cinética sobre cultura running: **10 segundos, proporção 9:16**. Cinco cenas combinam palavras em movimento e ilustrações vetoriais originais: corredores articulados, tênis, cidade e percurso animado.

| Tempo | Conteúdo |
| --- | --- |
| 0–2,1 s | Dê o primeiro passo — corredor, linhas de velocidade e cidade. |
| 2,1–4,2 s | Encontre seu ritmo — tênis ilustrado, órbitas e cadência. |
| 4,2–6,2 s | Ninguém corre só — grupo de corredores e ecos tipográficos. |
| 6,2–8 s | A rua é nossa — mapa de bairro e percurso em movimento. |
| 8–10 s | Corra. Respire. Repita. — grupo, chamada final e assinatura Pulso. |

## Abrir

Abra `index.html` no navegador. Tudo está incorporado no arquivo: CSS, JavaScript e desenho vetorial em Canvas. Não exige instalação, compilação, servidor, conexão ou dependências. Usa a fonte sem serifa do sistema; nenhuma fonte, fotografia ou música de terceiros é distribuída. As imagens são ilustrações, não fotografias. Sem áudio.

**Reproduzir** inicia ou pausa; **Repetir** ativa o ciclo; a linha do tempo permite examinar qualquer quadro. A animação começa automaticamente, exceto quando o sistema solicita movimento reduzido: mostra o quadro final e aguarda ação do usuário. A proporção vertical é preservada em telas pequenas e grandes.

## Arquivos

- `assets/pulso-running.mp4`: versão nova, H.264, 1080 × 1920, 30 fps, 10 segundos.
- `assets/running-preview.png`: quadro de prévia.
- `assets/scene-1.png` a `scene-5.png`: quadros de cada cena.
- `demo-4s.html` e `assets/pulso-demo.mp4`: primeira demonstração horizontal, preservada.
- `tests/REPORT.md`: testes executados e limitações.

## Desenvolvimento e créditos

Edite o HTML. Para servir opcionalmente: `python -m http.server 8080`. `window.Pulso.seek(milissegundos)` posiciona a animação determinística para captura. O desenho original de cada cena usa caminhos vetoriais, geometria, articulações e curvas; não há imagens externas carregadas durante a execução.

Criação assistida por Codex para acentinocreate. Licença MIT. Chromium/Playwright/FFmpeg são ferramentas de verificação/renderização, não dependências distribuídas no aplicativo. A fonte do sistema pode produzir diferenças de aparência em outros computadores.

Compatibilidade pretendida: versões atuais de Chrome, Edge, Firefox e Safari com Canvas 2D. Testes realmente executados estão no relatório. Repositório: https://github.com/acentinocreate/pulse. O usuário criou o repositório pela interface do GitHub; a publicação usa a conexão Git existente, sem depender da API de criação.
