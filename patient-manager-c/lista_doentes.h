#include "doente.h"
#ifndef ListaDoentes_H
#define ListaDoentes_H

typedef struct noLista
{
    doente * doente;
    struct noLista * prox;
}noLista;


typedef noLista * pLista;

pLista cria ();
int vazia (pLista lista);
void procura (pLista lista, int chave, pLista *ant, pLista *actual);
void elimina (pLista lista, int chave);
void insere (pLista lista, doente * d);
pLista pesquisa (pLista lista, int chave);
void print_ord(pLista lista, int len);
void print_tensao(pLista lista, int tensao);
void print_doente(pLista lista, int id);
int existe_id(pLista lista, int id);

#endif
