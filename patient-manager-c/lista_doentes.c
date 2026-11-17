#include "lista_doentes.h"
#include "lista_registos.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// Inicializa a lista de doentes
pLista cria (){
    pLista aux;
    aux = (pLista) malloc (sizeof (noLista));
    if (aux != NULL) {
        aux->doente = (doente * ) malloc(sizeof(doente));
        aux->prox = NULL;
    }
    return aux;
}

// Verifica se a lista de doentes está vazia
int vazia (pLista lista) {
    if (lista->prox == NULL) return 1;
    return 0;
}

// Procura a posição que chave inserida (id do doente) deve estar na lista de doentes
// Do menor para o maior
void procura (pLista lista, int chave, pLista *ant, pLista *actual){
    *ant = lista; 
    *actual = lista->prox;

    while ((*actual) != NULL && (*actual)->doente->id < chave) {
        *ant = *actual;
        *actual = (*actual)->prox;
    }

    if ((*actual) != NULL && (*actual)->doente->id != chave)
        *actual = NULL; 
}

// Liberta a memoria do doente e dos seus atributos
void elimina (pLista lista, int chave){
    pLista ant, actual;
    procura (lista, chave, &ant, &actual);
    if (actual != NULL) {
        ant->prox = actual->prox;
        destroi2(actual->doente->clinic_data_list);
        free(actual->doente->nome);
        free(actual->doente->cc);
        free(actual->doente->email);
        free (actual->doente);
        free (actual);
    }
}


// Insere um doente na posicção devolvida pelo procura
void insere (pLista lista, doente * d) {
    pLista no, ant, inutil;
    no = (pLista) malloc (sizeof (noLista));
    if (no != NULL) {
        no->doente = d;
        procura (lista, d->id, &ant, &inutil);
        no->prox = ant->prox;
        ant->prox = no;
    }
}

// Devolve o doente com o id inserido
pLista pesquisa (pLista lista, int chave){
    pLista ant, actual;
    procura (lista, chave, &ant, &actual);
    return (actual);
}

// Função que copia os elementos da lista ligada para um array
doente **copia_para_array(pLista lista, int len) {
    // Aloca memória para um array de ponteiros para doente
    doente **arr = (doente **)malloc(len * sizeof(doente *));
    
    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    pLista atual = lista->prox; 
    
    // Copia cada elemento da lista para o array
    for (int i = 0; i < len; i++) {
        arr[i] = atual->doente;
        atual = atual->prox;
    }
    
    return arr;
}

// Função de comparação utilizada pelo qsort para ordenar os doentes por nome
int compara_doentes(const void *a, const void *b) {
    // Converte os ponteiros para os tipos corretos
    doente *doenteA = *(doente **)a;
    doente *doenteB = *(doente **)b;
    
    // Compara os nomes dos doentes
    return strcasecmp(doenteA->nome, doenteB->nome);
}

// Função que imprime os doentes em ordem alfabética
void print_ord(pLista lista, int len) {
    // Copia os elementos da lista para um array
    doente **arr = copia_para_array(lista, len);

    // Ordena o array usando qsort e a função de comparação
    qsort(arr, len, sizeof(doente *), compara_doentes);

    // Imprime os nomes dos doentes em ordem alfabética
    for (int i = 0; i < len; i++) {
        printf("%s", arr[i]->nome); 
    }

    // Libera a memória alocada para o array
    free(arr);
}

// Função que imprime os doentes com a tensao_max superior a tensao (inserida por cliente)
void print_tensao(pLista lista, int tensao){

    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    pLista atual = lista->prox; 

    // Percorrer todos os doentes
    while(atual != NULL){
        // Verificar se a tensao_max do doente é maior que tensao
        if(atual->doente->clinic_data_list->prox != NULL && atual->doente->clinic_data_list->prox->clinic_data->tensao_max > tensao)
            printf("%s", atual->doente->nome);

        // Avançar para o próximo doente
        atual = atual->prox;
    }
}

// Função para imprimir as informações de um doente por ID
void print_doente(pLista lista, int id) {
    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    pLista atual = lista->prox;  

    while (atual != NULL) {
        if (atual->doente->id == id) {
            // Imprime as informações do doente
            printf("ID: %d\n", atual->doente->id);
            printf("Nome: %s", atual->doente->nome);
            printf("Data de nascimento: %02d/%02d/%04d\n", atual->doente->birthday.dia, atual->doente->birthday.mes, atual->doente->birthday.ano);
            printf("CC: %s", atual->doente->cc);
            printf("Telefone: %d\n", atual->doente->telephone);
            printf("Email: %s", atual->doente->email);

            // Sai da função após encontrar e imprimir o doente
            return;  
        }

        // Avançar para o próximo doente
        atual = atual->prox;  
    }
    // Se o doente com o ID fornecido não for encontrado, imprime uma mensagem
    printf("Doente com ID %d não encontrado.\n", id);
}

int existe_id(pLista lista, int id){
    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    pLista atual = lista->prox;  

    while (atual != NULL) {
        // Retorna que doente com o ID fornecido existe
        if (atual->doente->id == id) return 1;

        // Avançar para o próximo doente
        atual = atual->prox;  
    }
    // Retorna que doente com o ID fornecido não existe
    return 0;
}