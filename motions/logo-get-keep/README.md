# Logo original: GET → KEEP RUNNING

Abra index.html para visualizar a animação, pausar, repetir ou percorrer os 10 segundos. O fundo de inspeção não faz parte da animação. Os elementos brancos do arquivo original precisam de contraste para serem vistos.

original.svg é a cópia intacta do arquivo fornecido pelo usuário. Todos os 15 caminhos d e cores são reutilizados, sem redesenhar GET ou RUNNING. KEEP foi desenhado em keep.svg para esta proposta. GET sai e KEEP entra aos 5 segundos; RUNNING mantém a posição durante a troca. Somente a logo é animada.

logo-animated.svg contém animação SMIL independente e transparente; reproduz uma vez e permanece no quadro final. O visualizador HTML controla essa mesma timeline, respeita movimento reduzido e permite repetição. O SVG independente reproduz automaticamente e não implementa detecção de movimento reduzido.

keep-running.svg contém a versão final estática com KEEP. Para alterar KEEP, edite keep.svg. Para alterar a animação, edite build.py; depois execute python motions/logo-get-keep/build.py. index.html incorpora todo o SVG e os controles, sem dependências durante a reprodução.

WebM com transparência usa VP9 com alpha: prefira navegadores/editores que suportem esse formato. O alpha foi efetivamente decodificado e verificado. O formato horizontal é 1518 × 1010; a alternativa 9:16 é 1080 × 1920 e conserva a logo proporcionalmente centralizada. Sem áudio.

Os direitos da logo e do asset enviado permanecem com seu titular; a licença MIT do projeto aplica-se ao código e não transfere direitos sobre a marca.
