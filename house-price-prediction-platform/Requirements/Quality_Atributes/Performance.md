
## **Objetivo:**

A aplicação deve responder a solicitações do usuário de forma rápida e eficiente.

---

### Métricas da Performance:

- Tempo de carregamento da página: Tempo que leva para carregar completamente os elementos de uma página.

- Tempo de resposta para pesquisas efetuadas: Tempo que leva para a aplicação responder a uma solicitação do utilizador, como apresentar resultados de pesquisa, quer em imagem, quer em texto ou salvar um imóvel favorito.

- Taxa de transferência de dados: Quantidade de dados transferidos por segundo entre o servidor e o cliente.

---

### Metas: 

- Tempo de carregamento da página: inferior a 3 segundos

- Tempo de resposta para pesquisas efetuadas: inferior a 6 segundos

- Tempo para adicionar um imóvel aos favoritos: inferior a 1 segundo

- Tempo para criar uma conta: inferior a 3 segundos

- Tempo para entrar em uma conta: inferior a 2 segundos


---

### Otimização da Performance:

- Cache: Armazenar dados em cache para poder reduzir o tempo de carregamento e a utilização de recursos, principalmente os dados "frequently accessed".

- Compactação: Reduzir o tamanho de arquivos HTML, CSS e JavaScript pode diminuir o tempo de download e melhorar a taxa de transferência de dados.

---

### Considerações específicas para a aplicação:

- Impacto da geolocalização: A localização do utilizador pode afetar o tempo de resposta e a taxa de transferência de dados.

- Escalabilidade: A aplicação deve ser capaz de lidar com o aumento no número de utilizadores (ambos os cenários) e de dados.

## Cenários

1.
    **Estímulo:** Pesquisa com dados de um imóvel \
    **Fonte do estímulo:** Utilizador \
    **Contexto:** O sistema está em carga normal \
    **Artefacto:** A página de pesquisa \
    **Resposta:** O sistema devolve os resultados da pesquisa \
    **Medida da Resposta:** A resposta é apresentada em menos de 6 segundos. 

2.
    **Estímulo:** Mudar de página \
    **Fonte do estímulo:** Utilizador \
    **Contexto:** O sistema está em carga normal \
    **Artefacto:** A página de pesquisa \
    **Resposta:** O sistema devolve a página pretendida \
    **Medida da Resposta:** A resposta é apresentada em menos de 3 segundos. 

3.
    **Estímulo:** Criar conta \
    **Fonte do estímulo:** Utilizador \
    **Contexto:** O sistema está em carga normal \
    **Artefacto:** A página de pesquisa \
    **Resposta:** O sistema devolve a notificação de conta criada \
    **Medida da Resposta:** A resposta é apresentada em menos de 3 segundos. 

4.
    **Estímulo:** Entrar numa conta \
    **Fonte do estímulo:** Utilizador \
    **Contexto:** O sistema está em carga normal \
    **Artefacto:** A página de pesquisa \
    **Resposta:** O sistema devolve a notificação de entrada efetuada \
    **Medida da Resposta:** A resposta é apresentada em menos de 2 segundos.

5.
    **Estímulo:** Marcar imóvel como favorito \
    **Fonte do estímulo:** Utilizador \
    **Contexto:** O sistema está em carga normal \
    **Artefacto:** A página de pesquisa \
    **Resposta:** O sistema devolve feedback visual \
    **Medida da Resposta:** A resposta é apresentada em menos de 1 segundo.

**NOTA:** Para um *Contexto* de carga elevada mudamos apenas a *Medida de Resposta* para o seu dobro (mantendo os outros campos iguais)