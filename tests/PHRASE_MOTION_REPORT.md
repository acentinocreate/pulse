# Never give up. → Nunca desista. — implementação e teste

## Entrega

Motion de 10 segundos, com entrada sequenciada por letra, impulsos de cadência, zoom, deslocamentos e inclinações rápidas. A troca do vetor 1 para o vetor 2 ocorre na região dos 5 segundos. Repouso final para leitura. Somente os elementos fornecidos são animados; nenhum fundo, imagem, grafismo adicional, texto auxiliar ou marca-d'água integra as exportações. Sem áudio.

Asset 5.svg foi preservado byte por byte como vector-1.svg: 12 contornos, cor #30d949. Asset 6.svg foi preservado byte por byte como vector-2.svg: 13 contornos, cor #e5e1cf. Nenhuma fonte foi substituída, nenhum contorno redesenhado e nenhum parâmetro d modificado. A passagem é uma coreografia de saída/entrada, não um morph de pontos entre topologias diferentes.

SVG e HTML autossuficientes. WebM VP9 com alpha real: 1920 × 1080 e 1080 × 1920, 30 fps, 300 quadros, 10,000 segundos. A versão vertical conserva as proporções e centraliza o resultado com margens transparentes. Cores e outlines são exatos no SVG mestre; os vídeos usam compressão e conversão YUV, portanto não se afirma igualdade RGB pixel por pixel do vídeo comprimido.

## Correção implementada

A primeira comparação dos repousos encontrou diferenças de rasterização por antialiasing dos grupos animados, apesar de contornos e cores idênticos. Quadros de repouso passaram a usar camadas estáticas dos mesmos contornos, sem sobreposição visível com as camadas de movimento. A comparação de todos os canais RGBA então apresentou diferença zero para os dois SVGs originais no mesmo enquadramento. O vídeo foi novamente renderizado após a correção. Há 25 contornos fornecidos e 50 elementos path no mestre (cópias para movimento/repouso); nenhuma forma nova foi desenhada.

## Testes executados

31 verificações aprovadas em phrase-motion-results.json. Incluem: inicialização HTTP; preservação de cada contorno e cor de ambos os assets; igualdade RGBA dos dois quadros de repouso; transparência desses quadros; movimento observado no raster; ordem da transição; uso somente dos contornos fornecidos; renderização WebM; ausência de transbordamento horizontal móvel; duração; reinício, pausa, conclusão e repetição; movimento reduzido no HTML; SVG independente e seu estado final; ausência de erros JavaScript e de solicitações remotas; dimensões/duração e sinalização de alpha; alpha realmente decodificado nos dois vídeos.

Execução completa com recodificação está em phrase-motion-render-results.json. A revalidação posterior reutilizou os vídeos e repetiu as verificações após tornar o template HTML independente dos outros motions; não se contabilizam essas passagens como testes adicionais. ffprobe confirmou formato e duração; FFmpeg com decoder libvpx-vp9 confirmou pixels transparentes e pixels opacos. Não foi usada apenas a presença de metadados de alpha como prova.

Ambiente Linux, Chromium headless, Playwright Python, FontTools 4.61.1, FFmpeg e ffprobe. Preview em 1600 × 1100, raster/exportação em 1920 × 1080, móvel em 390 × 844. Inspeção visual dos repousos inglês e português. Nenhum dispositivo físico utilizado.

## Não executados e limitações

file:// foi tentado e bloqueado por política administrativa (ERR_BLOCKED_BY_ADMINISTRATOR). Não foi validado aqui. Firefox, Safari, Edge, celulares físicos e editores comerciais de vídeo não foram testados. Suporte a WebM VP9 com alpha varia conforme aplicativo. SVG independente reproduz uma vez, congela o desenho final e não detecta movimento reduzido; o HTML detecta a preferência e mostra o vetor 2 pausado. O vídeo vertical mantém a frase em uma linha, sem reorganizar a arte original. Não se afirma qualidade estética garantida: ritmo e transição devem ser avaliados pelo usuário.

## Reprodução

Para gerar SVG/HTML: com FontTools 4.61.1 instalado, python motions/never-give-up/build.py. O parser calcula limites para pivôs; não altera ou reescreve os contornos originais.

Com Playwright Python, Chromium em /usr/bin/chromium e FFmpeg/ffprobe com libvpx: python tests/phrase_motion_checks.py. O script inicia/encerra um servidor loopback na porta 8097, captura 300 quadros transparentes, codifica vídeos e valida os exports. Para revalidar arquivos existentes: python tests/phrase_motion_checks.py --reuse-exports.

Direitos dos assets permanecem com seu titular. A licença MIT do repositório aplica-se ao código. Não são distribuídos arquivos de fontes tipográficas.
