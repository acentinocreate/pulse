# Pulso — tipografia cinética

Demonstração original de motion com a frase **LETRA VIRA MOVIMENTO**. Duração: **4,8 segundos**. Entrada de letras, expansão horizontal, mudança de direção, ecos tipográficos e assinatura final. Sem áudio.

Abra `index.html` diretamente no navegador. Tudo está no HTML: CSS, JavaScript e animação. Não exige instalação, compilação, servidor, conexão ou dependências. Usa Arial/Helvetica ou a fonte sem serifa do sistema; nenhuma fonte é distribuída. A aparência pode variar entre sistemas.

**Reproduzir** inicia ou pausa; **Repetir** ativa o ciclo; a linha do tempo permite examinar qualquer quadro. A animação começa automaticamente, exceto quando o sistema solicita movimento reduzido: nesse caso mostra o quadro final e aguarda ação do usuário.

`assets/pulso-demo.mp4` contém uma renderização de 1280 × 720, 30 quadros por segundo. `assets/preview.png` mostra um quadro da animação.

Compatibilidade pretendida: versões atuais de Chrome, Edge, Firefox e Safari com Web Animations API. Testes realmente executados estão em `tests/REPORT.md`.

## Desenvolvimento

Edite o próprio HTML. Para servir opcionalmente: `python -m http.server 8080`. A API `window.Pulso.seek(milissegundos)` posiciona o quadro para reprodução determinística e captura. Créditos de autoria: criação assistida por Codex para acentinocreate. Licença MIT; nenhuma imagem, música ou fonte de terceiros foi incluída.
