# Logo original GET → KEEP — relatório

## Implementação

Animação direta da logo enviada em Asset 1.svg, sem fundo ou elementos gráficos adicionados. O original foi preservado byte por byte em motions/logo-get-keep/original.svg. Seus 15 contornos e as cores #30d949 / #fff são reutilizados no SVG animado. GET e RUNNING não foram redesenhados. KEEP é um novo desenho vetorial para acompanhar a altura, as hastes e o arredondamento de GET; não se afirma fidelidade a um KEEP original inexistente no arquivo.

10 segundos; entrada com deslocamentos e inclinações, impulsos de cadência nos próprios contornos, saída de GET e entrada de KEEP na região dos 5 segundos, repouso final. RUNNING mantém a posição durante a troca. Controles de visualização ficam fora da animação, assim como o fundo de inspeção. Nenhuma trilha ou efeito sonoro.

WebM horizontal de 1518 × 1010 e derivado 9:16 de 1080 × 1920, ambos VP9, 30 fps, 300 quadros, 10,000 segundos, com alpha. A versão vertical escala proporcionalmente e acrescenta apenas área transparente ao redor. SVG animado SMIL independente, HTML autossuficiente, logo final estática SVG e PNG com transparência.

## Testes executados

27 verificações aprovadas em logo-motion-results.json: inicialização HTTP; retenção de todos os caminhos originais; cores originais; igualdade RGBA pixel por pixel entre o quadro de repouso GET e o SVG fornecido na mesma viewport; transparência e presença da logo; GET antes e KEEP depois do ponto médio; posição de RUNNING na troca; duração; alpha do PNG final; renderização WebM; ausência de transbordamento móvel; reinício/pausa/conclusão/repetição; movimento reduzido no HTML; SVG independente e seu quadro final; ausência de erros JavaScript e de solicitações remotas; dimensões/duração; sinalização de alpha; alpha efetivamente decodificado no WebM horizontal; renderização vertical, dimensões/duração 9:16 e transparência efetiva de sua margem.

Execução completa de renderização registrada em logo-motion-render-results.json. Uma segunda execução reutilizou os vídeos já renderizados e repetiu a validação, incluindo a comparação explícita de todos os canais RGBA; não houve nova codificação nessa segunda passagem. O decoder libvpx-vp9 foi selecionado explicitamente para verificar alpha: o decoder VP9 nativo de algumas versões do FFmpeg pode descartá-lo. Não foi usada apenas a presença de metadados como prova de transparência.

Linux, Chromium headless, Playwright Python, FFmpeg/ffprobe. Preview em 1600 × 1200, render em 1518 × 1010 e viewport móvel em 390 × 844. Inspeção visual do preview GET de 1,5 s e da logo final. Nenhum dispositivo físico usado. Defeito de serialização do namespace SVG no teste de comparação foi corrigido antes da execução completa; a comparação passou a gerar SVG nativo no documento HTML de referência.

## Limitações

file:// foi tentado e bloqueado administrativamente (ERR_BLOCKED_BY_ADMINISTRATOR); não validado neste ambiente. Firefox, Safari, Edge, dispositivos físicos e importação em editores de vídeo comerciais não foram testados. Suporte a WebM VP9 com alpha varia entre aplicativos. O SVG independente reproduz uma vez e não detecta preferência por movimento reduzido; o HTML detecta essa preferência e mostra o quadro final pausado. Validação técnica não substitui avaliação da proposta de KEEP e do ritmo do motion pelo usuário.

## Reprodução

Gere os arquivos: python motions/logo-get-keep/build.py. Com Playwright Python, Chromium em /usr/bin/chromium e FFmpeg/ffprobe com libvpx disponíveis: python tests/logo_motion_checks.py. O script inicia/encerra servidor loopback em 8094, renderiza quadros transparentes, codifica WebM e valida alpha após decodificação. Para revalidar vídeos existentes sem recodificar: python tests/logo_motion_checks.py --reuse-exports.
