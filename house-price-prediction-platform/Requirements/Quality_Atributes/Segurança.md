# Security

- O sistema deve garantir que a integridade dos dados utilizados não seja comprometida.
- O sistema deve manter a confidencialidade dos dados dos utilizadores de forma a que a informação dos seus imoveis não seja acedida por terceiros
- O sistema deve manter os dados de autenticação (passwords) encriptados para que em caso de acesso não autorizado, estes não sejam comprometidos.
- O sistema deve conseguir manter-se disponivel mesmo em caso de tentativas de uso ilegitimo.


## Cenário 1  
 - **Fonte de Estimulo:** Utilizador não identificado.
 - **Estímulo:** Aceder a funcionalidades disponiveis apenas para utilizadores autenticados.
 - **Ambiente:** Sobre condições normais.
 - **Artefacto:** Serviços do sistema.
 - **Resposta:** Bloqueia a tentativa de uso.
 - **Medida da Resposta:** Probabilidade de deteção da tentativa.
  
## Cenario 2
 - **Fonte de Estimulo:** Utilizador autenticado
 - **Estímulo:** Aceder a qualquer funcionalidade
 - **Ambiente:** Sobre carga/Sobre ataque
 - **Artefacto:** Serviços do sistema
 - **Resposta:** Reponder normalmente
 - **Medida da Resposta:** % de aumento no tempo de resposta necessario para responder.
  
## Cenario 3
 - **Fonte de Estimulo:** Individuo com acesso aos dados
 - **Estímulo:** Alteração na base de dados
 - **Ambiente:** Sobre carga/Sobre ataque
 - **Artefacto:** Dados
 - **Resposta:** Regista o que mudou, quando e quem o fez.
 - **Medida da Resposta:** Tempo necessário para detetar e recuperar caso uma alteração indevida ocorra na base de dados.

## Cenário 4
 - **Fonte de Estimulo:** Utilizador não identificado.
 - **Estímulo:** Tentar autenticar usando força bruta.
 - **Ambiente:** Online.
 - **Artefacto:** Sistema de Autenticação.
 - **Resposta:** Bloqueia as tentativas de login.
 - **Medida da Resposta:** Probabilidade de deteção do uso de força bruta.