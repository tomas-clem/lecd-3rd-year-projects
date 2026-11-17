#include "registo.h"
#ifndef ListaRegistos_H
#define ListaRegistos_H

typedef struct noLista2
{
    registo * clinic_data;
    struct noLista2 * prox;
}noLista2;


typedef noLista2 * pLista2;

pLista2 cria2 ();
int vazia2 (pLista2 lista);
pLista2 destroi2 (pLista2 lista);
void procura2 (pLista2 lista, Data date, pLista2 *ant, pLista2 *actual);
void insere2 (pLista2 lista, registo * clinic_data);

#endif
