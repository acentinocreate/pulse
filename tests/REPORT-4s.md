# Verificação da demonstração

Executado neste ambiente Linux com Chromium headless (`/usr/bin/chromium`), Playwright Python e FFmpeg. Viewports: 1336 × 920 (palco 1280 × 720) e 390 × 844.

12 verificações aprovadas: início por HTTP, duração, reinício, pausa, conclusão automática, repetição, renderização MP4, ausência de transbordamento móvel, respeito a movimento reduzido, ausência de erros JavaScript, ausência de solicitações remotas e dimensões/duração do vídeo. Resultados em `results.json`.

MP4: H.264, 1280 × 720, 30 fps, 144 quadros, 4,800 segundos, sem áudio. Quadros capturados da própria animação HTML com posição determinística. Inspeção visual realizada no quadro intermediário `assets/preview.png`.

A tentativa de abrir via file:// foi bloqueada pela política administrativa do Chromium (`ERR_BLOCKED_BY_ADMINISTRATOR`). Portanto file:// não foi validado aqui. Não há dependência de HTTP no código. Firefox, Safari, Edge e dispositivos físicos não foram testados.

Reprodução: instale Playwright Python e disponibilize Chromium, FFmpeg e ffprobe; execute `python tests/render.py` na raiz. O script inicia seu próprio servidor apenas em loopback, na porta 8092, e o encerra ao concluir.

Publicação: tentativa de criar `acentinocreate/pulso-tipografia` com GitHub CLI bloqueada por `Forbidden` na API. Repositório remoto não foi criado nesta execução.
