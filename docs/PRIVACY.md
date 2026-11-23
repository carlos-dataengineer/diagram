# Privacidade e dados

- Os modelos, exemplos e imagens do projeto usam **dados fictícios**.
- Por padrão, os diagramas ficam no `localStorage` do navegador. Nada é enviado a servidores.
- No artefato do Claude, os diagramas também são guardados na conta da pessoa, em `data/users/<id>/diagrams`, um espaço privado: nem quem publicou o artefato lê os diagramas de outra pessoa.
- A geração por IA (`sample`) só existe no Claude e só é chamada quando a pessoa clica em **Gerar**. O texto enviado é a descrição digitada.
- A única requisição externa do editor é a fonte do Google Fonts.
- O instalador só copia arquivos locais; não coleta nem envia dados.
- Diagramas podem conter o que a pessoa digitar: evite segredos, tokens e dados pessoais em arquivos compartilhados.
