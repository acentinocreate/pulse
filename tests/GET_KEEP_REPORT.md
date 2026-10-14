# GET → KEEP RUNNING — implementação e validação

## Entrega

Motion de 10 segundos, 9:16, 1080 × 1920, 30 fps, 300 quadros, sem áudio. Identidade verde/branco e lettering grosso arredondado, com entrada individual de letras, rastros de velocidade, linhas de pista, chevrons, zoom e cortes de composição. GET sai na preparação da troca e KEEP começa a entrar aos 5 segundos; RUNNING continua na composição. Encerramento legível com KEEP RUNNING.

Lettering reconstruído manualmente em nove contornos vetoriais a partir da imagem raster enviada na conversa. Não foi usado o arquivo vetorial original, nem realizada extração exata dos pixels. GET e KEEP são desenvolvimentos do estilo observado; os desenhos de K/E/T/P são adaptações compatíveis, não contornos fornecidos pelo usuário. Não se afirma identidade geométrica exata com o asset. Direitos sobre o asset de referência permanecem com o titular; MIT aplica-se ao código.

`motions/get-keep/index.html` incorpora os dados e a animação e não precisa dos arquivos-fonte para executar. Código editável em `source.js` e contornos em `lettering.json`. Geração do HTML: `python motions/get-keep/build.py`. Prova SVG em `lettering-proof.svg`. A animação anterior foi preservada; a página inicial agora oferece um link para o novo motion.

## Testes executados

16 verificações aprovadas em `get-keep-results.json`: início HTTP; GET antes do ponto médio; KEEP no ponto médio; aumento real da largura do desenho de KEEP no raster após a troca; uso de contornos vetoriais; duração; reinício; pausa; parada aos 10 segundos; repetição; renderização MP4; ausência de transbordamento horizontal no celular; movimento reduzido; ausência de erros JavaScript; ausência de solicitações remotas; dimensões/duração do MP4.

O teste da mudança inclui leitura dos pixels brancos na região das palavras antes/depois, além da identificação de palavra na timeline. Não equivale a uma avaliação artística da transição. Inspeção visual feita no quadro de 5,5 segundos e nos quadros de revisão de 1,2 / 4,6 / 9,7 segundos.

Execução: Chromium headless, Playwright Python, FFmpeg e ffprobe neste Linux. Controles em 1336 × 920, exportação em 1080 × 1920, mobile em 390 × 844. ffprobe confirmou MP4 H.264 de 10,000 segundos, sem áudio. Quadros renderizados do Canvas do próprio HTML, com seek determinístico.

## Limitações e verificações não executadas

file:// foi tentado e bloqueado pela política administrativa do navegador (ERR_BLOCKED_BY_ADMINISTRATOR); não validado aqui. Firefox, Safari, Edge, celulares físicos e desempenho em hardware móvel não foram testados. Texto auxiliar usa fonte monoespaçada do sistema e pode variar; o lettering principal é vetorial e não depende de fonte instalada. Sem trilha ou efeitos sonoros.

## Reprodução

Com Playwright Python, Chromium em /usr/bin/chromium, FFmpeg e ffprobe instalados: `python tests/get_keep_checks.py`. O script inicia e encerra servidor loopback na porta 8093, captura 300 quadros e exporta `assets/get-keep-running.mp4`. Resultados e imagens são escritos no repositório.
