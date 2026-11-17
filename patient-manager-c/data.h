#ifndef Datas_H
#define Datas_H

typedef struct Data
{
   int dia,mes,ano;
} Data;

int compara_datas(Data d1, Data d2);
int valida_data(int dia, int mes, int ano);

#endif