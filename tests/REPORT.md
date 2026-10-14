# Run culture — relatório de implementação e teste

Implementado: versão vertical 9:16, 10 segundos, cinco cenas; tipografia animada com entrada, inclinação, recortes e transições; ilustrações vetoriais originais de corredores com articulações animadas, tênis, cidade e percurso progressivo. Reprodução, pausa, repetição e busca na linha do tempo. Movimento reduzido mostra quadro final e aguarda reprodução explícita. Sem áudio, fontes externas, fotografias ou serviços remotos. Primeira versão horizontal preservada em demo-4s.html.

Execução: Chromium headless, Playwright Python, FFmpeg e ffprobe neste ambiente Linux. Viewports 1336 × 920 para controles, 1080 × 1920 para exportação, e 390 × 844 para celular. Dispositivo físico não usado.

12 verificações aprovadas em results.json: início HTTP, duração, reinício, pausa, parada após 10 segundos, repetição, renderização MP4, ausência de transbordamento horizontal móvel, movimento reduzido, ausência de erros JavaScript, ausência de solicitações remotas e formato/duração do vídeo.

MP4 independente inspecionado por ffprobe: H.264, 1080 × 1920, 30 fps, 300 quadros, 10,000 segundos, sem áudio. Cada quadro foi capturado do Canvas do HTML com posição determinística; mesmas ilustrações e animações do aplicativo. Inspeção visual executada nos quadros das cenas 2, 3 e 5. Quadros ilustrativos de todas as cenas entregues em assets/scene-N.png.

Não executados: Firefox, Safari, Edge, testes em dispositivos físicos. file:// tentado e bloqueado por política administrativa (ERR_BLOCKED_BY_ADMINISTRATOR); não validado aqui. O código usa apenas Canvas local e não depende de HTTP. Fontes do sistema podem alterar a aparência entre computadores. Sem comparação de performance em hardware móvel real.

Reprodução: com Playwright Python, Chromium em /usr/bin/chromium e FFmpeg/ffprobe no PATH, execute python tests/render.py. O script inicia e encerra seu próprio servidor na porta loopback 8092 e gera o vídeo e quadros. Os registros da versão horizontal anterior estão preservados em REPORT-4s.md e results-4s.json; não foram reexecutados nesta atualização.

Publicação: repositório independente versionado. A criação inicial pela API foi bloqueada por Forbidden; posteriormente o usuário criou acentinocreate/pulse pela interface do GitHub. O envio utiliza Git HTTPS. Os resultados de teste acima correspondem à execução original; não foram reexecutados para esta atualização de documentação.
