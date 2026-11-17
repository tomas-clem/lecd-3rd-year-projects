# Testabilidade: 

### Exemplo de testabilidade nº 1

Objetivo: Execução de testes de Interface de Utilizador

**Fonte de Estímulo**: Equipa que assegura a qualidade do sistema (Quality Assurance) efetua testes de usabilidade. 

**Estímulo**: Execução de testes automáticos e/ ou manuais nas interfaces dos utilizadores. (Sendo mais benéfico a execução de testes automáticos, dado que estes fornecem informação detalhada acerca da cobertura do software em análise).

**Ambiente**: Desde as primeiras versões desenvolvidas até ao lançamento efetivo e definitivo do produto.  

**Artefacto**: Interface gráfica do utilizador. 

**Resposta**: O sistema fornece indicação se o teste foi validado ou se apresentou algum erro, validando ou não o sistema.

**Medida da Resposta**: Tempo que o conjunto de testes  de interface de utilizador, sendo estes testes automáticos e testes manuais forem passados. Considerando que um teste passa quando todas as condições são verificadas corretamente. Os testes automáticos podem demorar 5 minutos, 15 minutos, 1 hora ou 1 dia.   

################# 

### Exemplo de testabilidade nº 2

Objetivo: Teste de Segurança do Sistema. 

**Fonte de Estímulo**: Equipa responsável pela segurança do sistema, avalia a robustez do sistema contra vulnerabilidade. 

**Estímulo**: Realização de testes que pretendem simular o acesso não autorizado no sistema, com o objetivo de percepção das vulnerabilidades do sistema. 

**Ambiente**: Até que cada funcionalidade esteja completamente terminada. Assim como, antes do sistema final ser lançado efetivamente. E quando o sistema está finalizado executá-los de forma periódica. 

**Artefacto**: Totalidade da infraestrutura do sistema, incluindo a aplicação web, base de dados e infraestrutura da rede. 

**Resposta**: O sistema sinaliza se houve algum acesso indevido ao sistema ou não.

**Medida da Resposta**:  Quantos dos testes de segurança foram corretamente efetuados e quantos deles não foram. Sendo 100% dos testes corretamente passados, o que indica que segurança no sistema.


###########

### Exemplo de testabilidade nº 3

Objetivo: Testar a Performance do Modelo e o Tempo de Resposta (output).

**Fonte de Estímulo**: Equipa de desenvolvimento otimiza os modelos (previsão de preço de um imóvel, indicação das características mais comuns para um determinado valor, indicação de qual tipo de imóvel é mais comum numa localização, entre outros) e avalia o tempo de resposta com base também em disponibilidade.  

**Estímulo**: Otimizar os algoritmos.  

**Ambiente**: Testar com vários dados de teste diferentes e representativos. 

**Artefacto**: Algoritmo de machine learning e sistema de resposta.

**Resposta**: Teste de desempenho permite executar os testes de disponibilidade e desempenho para avaliar o tempo de resposta e a precisão do algoritmo, em diferentes condições.

**Medida da Resposta**: A precisão do algoritmo deve ter no mínimo um valor de 90% e o tempo de entrega ao utilizador não deve exceder os 6 segundos, independentemente da carga a que o sistema está exposto. 

########################

### Exemplo de testabilidade nº 4

Objetivo: Testar se o código efetuado está legível e compreensível. 

**Fonte de Estímulo**: Equipa responsável pela revisão do código.

**Estímulo**: Rever o código-fonte das várias funções efetuadas, com o objetivo de este apresentar legibilidade e compreensibilidade. 

**Ambiente**: Ferramenta de revisão de código. 

**Artefacto**: Função/ conjunto de funções em análise.

**Resposta**: Indicação se o código apresenta ou não legibilidade e compreensibilidade. Podendo esta indicação ser efetuado numa escala de 1 a 5, sendo que 1 indica baixa legibilidade e compreensibilidade e 5 indica alta legibilidade e compreensibilidade.
 
**Medida da Resposta**: Sendo a legibilidade e compreensibilidade medidas pela falta de comentários elucidativos, nomenclatura coerente e documentação inerente ao software/ parte de software em desenvolvimento, estes são medidos por ferramentas que permitem analisar esses parâmetros. 
