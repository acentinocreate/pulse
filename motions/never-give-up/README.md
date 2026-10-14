# Never give up. → Nunca desista.

Motion esportivo de 10 segundos. Abra index.html para reproduzir, pausar, repetir ou percorrer a timeline. O fundo de inspeção serve apenas ao visualizador; as exportações são transparentes. Nenhum elemento gráfico foi adicionado além das frases fornecidas.

vector-1.svg é Asset 5.svg, intacto. vector-2.svg é Asset 6.svg, intacto. Todos os contornos e cores são preservados: verde #30d949 para a frase inglesa, creme #e5e1cf para a portuguesa. A troca ocorre na região dos 5 segundos, por uma coreografia de saída/entrada das letras; não se trata de interpolação dos pontos entre anatomias incompatíveis.

O desenho final é o vetor 2 original, posicionado no centro do quadro e sem deformação. Entrada por letras, impulsos de ritmo, zoom, inclinações e deslocamentos ocorrem durante o motion. Nos quadros de repouso, camadas estáticas dos mesmos contornos substituem as camadas de transformação, sem sobreposição visível, para reproduzir os originais sem diferenças de antialiasing.

motion.svg é a animação SMIL independente: reproduz uma vez e mantém o desenho final. index.html incorpora esse SVG e os controles. O HTML respeita movimento reduzido e mostra o vetor 2 pausado; o SVG independente não detecta essa preferência.

WebM VP9 com alpha real: horizontal 1920 × 1080 e vertical 1080 × 1920, 30 fps, sem áudio. A versão vertical mantém as proporções e centraliza a arte com margens transparentes; não reorganiza as palavras. Suporte a WebM com alpha varia entre navegadores e editores.

Para alterar os arquivos-fonte ou o roteiro, edite os SVGs ou build.py e execute python build.py com FontTools instalado. O parser de FontTools só calcula limites para os pivôs da animação: os contornos d nunca são regenerados. Nenhuma fonte tipográfica é necessária para reproduzir o resultado.

Direitos sobre os assets permanecem com seu titular. A licença MIT do repositório aplica-se ao código e não transfere direitos sobre as artes enviadas.
