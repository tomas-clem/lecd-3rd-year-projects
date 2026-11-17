#include "data.h"
#ifndef Registos_H
#define Registos_H

typedef struct registo
{
    int id_doente;
    Data data;
    int tensao_max;
    int tensao_min;
    int peso;
    int altura;
}registo;

#endif