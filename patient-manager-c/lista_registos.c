#include "lista_registos.h"
#include <stdlib.h>


// Inicializa a lista de registos
pLista2 cria2 (){
    pLista2 aux;
    aux = (pLista2) malloc (sizeof (noLista2));
    if (aux != NULL) {
        aux->clinic_data = (registo * ) malloc(sizeof(registo));
        aux->prox = NULL;
    }
    return aux;
}

// Verifica se a lista de registos está vazia
int vazia2 (pLista2 lista) {
    if (lista->prox == NULL) return 1;
    return 0;
}


// Liberta a memoria da lista de registos
pLista2 destroi2 (pLista2 lista){
    pLista2 temp_ptr;
    while (!vazia2 (lista)) {
        temp_ptr = lista;
        lista = lista->prox;
        free(temp_ptr->clinic_data);
        free (temp_ptr);
    }
    free(lista->clinic_data);
    free(lista);
    return NULL;
}

// Procura a posição na lista de registo tendo em conta a data
// Da data mais recente para a mais antiga
void procura2 (pLista2 lista, Data date, pLista2 *ant, pLista2 *actual){
    *ant = lista; 
    *actual = lista->prox;

    while ((*actual) != NULL && compara_datas((*actual)->clinic_data->data, date) == 1) {
        *ant = *actual;
        *actual = (*actual)->prox;
    }

    if ((*actual) != NULL && compara_datas((*actual)->clinic_data->data, date) != 0)
        *actual = NULL;
}

// Insere o registo na posição devolvida pelo procura2
void insere2 (pLista2 lista, registo * clinic_data) {
    pLista2 no, ant, inutil;
    no = (pLista2) malloc (sizeof (noLista2));
    if (no != NULL) {
        no->clinic_data = clinic_data;
        procura2 (lista, clinic_data->data, &ant, &inutil);
        no->prox = ant->prox;
        ant->prox = no;
    }
}