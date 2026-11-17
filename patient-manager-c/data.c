#include "data.h"

// Compara duas datas dadas
int compara_datas(Data d1, Data d2){
    if (d1.ano == d2.ano && d1.mes == d2.mes && d1.dia == d2.dia){
        return 0;
    }else{
        if((d1.ano < d2.ano) || (d1.ano == d2.ano && d1.mes<d2.mes) || (d1.ano == d2.ano && d1.mes == d2.mes && d1.dia < d2.dia)){
            return -1;
        }else{
            return 1;
        }
    }
}

// Função para validar a data
int valida_data(int dia, int mes, int ano) {
    // Verifica se os valores estão dentro dos limites
    if (ano < 1900) return 0;
    if (mes < 1 || mes > 12) return 0;
    if (dia < 1 || dia > 31) return 0;

    // Verificação de dias em cada mês
    if (mes == 2) {
        // Verificação de ano bissexto
        int bissexto = (ano % 4 == 0 && (ano % 100 != 0 || ano % 400 == 0));
        if (bissexto && dia > 29) return 0;
        if (!bissexto && dia > 28) return 0;
    } else if (mes == 4 || mes == 6 || mes == 9 || mes == 11) {
        if (dia > 30) return 0;
    }
    return 1;
}