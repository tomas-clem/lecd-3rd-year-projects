#include "data.h"
#include "registo.h"
#include "lista_registos.h"
#ifndef Doentes_H
#define Doentes_H

typedef struct doente
{
    int id;
    char * nome;
    Data birthday;
    char * cc;
    int telephone;
    char * email;
    pLista2 clinic_data_list;
}doente;

#endif