#include "doente.h"
#include "registo.h"
#include "data.h"
#include "lista_doentes.h"
#include "lista_registos.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int menu();
int read_doentes(pLista lista);
void save_doentes(pLista lista);
void read_registos(pLista lista);

int main(){
    pLista lista = cria();
    int count = read_doentes(lista);
    read_registos(lista);
    int running = 1;
    while(running){
        switch (menu())
        {
            case 1:{ // Inserir novo doente
                int inteiro, c, d, m, a;
                int state = 1;
                char term;
                // char* string = (char * ) malloc(sizeof(char[50]));
                char string[60];
                doente * temp_doente = (doente * ) malloc(sizeof(doente));

                // Pedir ID
                printf("Insira o ID: ");
                while(state){
                    // Verifica se é inteiro
                    if (scanf("%d%c", &inteiro, &term) != 2 || term != '\n'){
                        printf("Introduza um ID válido: ");
                        while ((c = getchar()) != '\n') {}
                    // Verifica se já existe
                    }else if (existe_id(lista, inteiro) == 1){
                        printf("ID introduzido já existe: ");
                    }else
                        state=0;
                }
                // Guardar ID do novo doente
                temp_doente->id = inteiro;


                // Pedir Nome
                printf("Insira o Nome: ");
                state = 1;
                while(state){
                     if (fgets(string, sizeof(string)/sizeof(char), stdin) != NULL){
                        if(strlen(string)>50){
                            printf("Intoduza um nome com tamanho inferior a 50 carateres: ");   
                        }
                        else{
                            state = 0;
                        }
                    }
                }
                // Guardar Nome do novo doente
                temp_doente->nome = strdup(string);


                // Pedir a Data de Nascimento
                printf("Insira a Data de Nascimento (formato: dd/mm/aaaa): ");
                state = 1;
                while(state){
                    // Verifica se dia, mes e ano são inteiros e se é uma data possível
                    if (scanf("%d/%d/%d%c", &d, &m, &a, &term) != 4 || term != '\n'){
                        printf("Introduza uma Data de Nascimento válida: ");
                        while ((c = getchar()) != '\n') {}
                    }else if (valida_data(d,m,a) == 0){
                        printf("Introduza uma Data de Nascimento válida: ");
                    }else
                        state = 0; 
                }
                // Guardar a Data de Nascimento do novo doente
                Data x = {.dia=d,.mes=m,.ano=a};
                temp_doente->birthday = x;


                // Pedir o Número de CC
                printf("Insira o Número de CC: ");
                scanf("%s", string);
                // Acrescentar \n ao Número de CC
                char* newstr = malloc(strlen(string) + 2);
                strcpy(newstr, string);
                // Guardar o Número de CC do novo doente
                temp_doente->cc =strcat(newstr, "\n");


                // Pedir o Número de Telefone 
                printf("Insira o Número de Telefone: ");
                state = 1;
                while(state){
                    // Verifica se é inteiro
                    if (scanf("%d%c", &inteiro, &term) != 2 || term != '\n'){
                        printf("Introduza um Número de Telefone válido: ");
                        while ((c = getchar()) != '\n') {}
                    }else
                        state=0;
                }
                // Guardar o Número de Telefone do novo doente
                temp_doente->telephone = inteiro;


                // Pedir o Email
                printf("Insira o Email: ");
                scanf("%s", string);
                // Acrescentar \n ao Email
                newstr = malloc(strlen(string) + 2);
                strcpy(newstr, string);
                // Guardar o Email
                temp_doente->email = strcat(newstr, "\n");

                // Criar lista de registos para o doente
                temp_doente->clinic_data_list = cria2();

                // Inserir novo doente na lista
                insere(lista, temp_doente);
                // Atualizar o número de doentes na lista
                count++;
                break;
            }
            case 2: // Eliminar doente
                int id2, c2, state2 = 1;
                char term2;
                if (vazia(lista)){
                    printf("Não existem doentes.\n");
                }else{
                    // Pedir ID do doente a eliminar
                    printf("Insira o ID do doente a eliminar: ");
                    while(state2){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &id2, &term2) != 2 || term2 != '\n'){
                            printf("Introduza um ID válido: ");
                            while ((c2 = getchar()) != '\n') {}
                        // Verifica se existe
                        }else if (existe_id(lista, id2) == 0){
                            printf("ID introduzido não existe: ");
                        }else
                            state2=0;
                    }

                    // Eliminar o doente da lista
                    elimina(lista,id2);
                    // Atualizar o número de doentes na lista
                    count--;
                }
                break;
            case 3: // Listar doentes alfabeticamente
                if(vazia(lista))
                    printf("Não existem doentes.\n");
                else
                    print_ord(lista, count);
                break;
            case 4: // Listar doentes com tensão maxima acima de um valor
                if (vazia(lista)){
                    printf("Não existem doentes.\n");
                }else{
                    int tensao, c4, state4 = 1;
                    char term4;
                    // Pedir o valor mínimo da tensão máxima a listar
                    printf("Introduza o valor mínimo da tensão máxima: ");
                    while(state4){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &tensao, &term4) != 2 || term4 != '\n'){
                            printf("Introduza uma tensão válida: ");
                            while ((c4 = getchar()) != '\n') {}
                        }else
                            state4=0;
                    }
                    
                    // Imprimir da lista os doentes com tensão maxima acima de "tensão"
                    printf("Doentes com tensão máxima acima de %d:\n", tensao);
                    print_tensao(lista, tensao);
                }
                break;
            case 5: // Mostrar informação do doente
                int id5, c5, state5 = 1;
                char term5;
                if (vazia(lista)){
                    printf("Não existem doentes.\n");
                }else{
                    // Pedir ID do doente para mostrar a informação
                    printf("Insira o ID do doente para mostrar a informação: ");
                    while(state5){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &id5, &term5) != 2 || term5 != '\n'){
                            printf("Introduza um ID válido: ");
                            while ((c5 = getchar()) != '\n') {}
                        // Verifica se existe
                        }else if (existe_id(lista, id5) == 0){
                            printf("ID introduzido não existe: ");
                        }else
                            state5=0;
                    }
                    // Print informação do doente com ID "id5"
                    print_doente(lista, id5);
                }
                break;
            case 6: // Criar registo
                int id6,input, d, m, a, c6, state6 = 1;
                char term6;
                if (vazia(lista)){
                    printf("Não existem doentes.\n");
                }else{
                    registo * temp_registo = (registo * ) malloc(sizeof(registo));
                    // Pedir ID do doente a que vai adicionar o registo
                    printf("Insira o ID do doente a que quer adicionar o registo: ");
                    while(state6){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &input, &term6) != 2 || term6 != '\n'){
                            printf("Introduza um ID válido: ");
                            while ((c6 = getchar()) != '\n') {}
                        // Verifica se existe
                        }else if (existe_id(lista, input) == 0){
                            printf("ID introduzido não existe: ");
                        }else
                            state6=0;
                    }
                    temp_registo->id_doente = input;

                    state6 = 1;
                    // Pedir a tensão maxima
                    printf("Introduza a Tensão Máxima:");
                    while(state6){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &input, &term6) != 2 || term6 != '\n'){
                            printf("Introduza uma Tensão Máxima válida: ");
                            while ((c6 = getchar()) != '\n') {}
                        }else
                            state6=0;
                    }
                    temp_registo->tensao_max = input;

                    state6 = 1;
                    // Pedir a Tensão Mínima
                    printf("Introduza a Tensão Mínima:");
                    while(state6){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &input, &term6) != 2 || term6 != '\n'){
                            printf("Introduza uma Tensão Mínima válida: ");
                            while ((c6 = getchar()) != '\n') {}
                        }else
                            state6=0;
                    }
                    temp_registo->tensao_min = input;

                    state6 = 1;
                    // Pedir o peso
                    printf("Introduza o Peso:");
                    while(state6){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &input, &term6) != 2 || term6 != '\n'){
                            printf("Introduza um Peso válido: ");
                            while ((c6 = getchar()) != '\n') {}
                        }else
                            state6=0;
                    }
                    temp_registo->peso = input;

                    state6 = 1;
                    // Pedir a altura
                    printf("Introduza a Altura:");
                    while(state6){
                        // Verifica se é inteiro
                        if (scanf("%d%c", &input, &term6) != 2 || term6 != '\n'){
                            printf("Introduza uma Altura válida: ");
                            while ((c6 = getchar()) != '\n') {}
                        }else
                            state6=0;
                    }
                    temp_registo->altura = input;

                                    
                    state6 = 1;;
                    // Pedir a data do registo
                    printf("Insira a Data do Registo (formato: dd/mm/aaaa): ");
                    while(state6){
                        // Verifica se dia, mes e ano são inteiros e se é uma data possível
                        if (scanf("%d/%d/%d%c", &d, &m, &a, &term6) != 4 || term6 != '\n'){
                            printf("Introduza uma Data do Registo válida: ");
                            while ((c6 = getchar()) != '\n') {}
                        }else if (valida_data(d,m,a) == 0){
                            printf("Introduza uma Data do Registo válida: ");
                        }else
                            state6 = 0; 
                    }
                    // Guardar a Data de registo 
                    Data x = {.dia=d,.mes=m,.ano=a};                    
                    temp_registo->data = x;
                    insere2(pesquisa(lista,temp_registo->id_doente)->doente->clinic_data_list,temp_registo);

                }

                break;
            case 7: // exit
                running = 0;
                break;
            default:
                break;
            }
    }
    // Guardar a lista no ficheiro txt e destrui-la
    save_doentes(lista);
    return 0;
}


int menu(){
    // Opções de funcionalidades
    printf("\nOpções:\n1 - Introduzir novo doente\n2 - Eliminar doente\n3 - Listar doentes alfabeticamente\n4 - Listar doesnte com tensão maxima acima de um valor\n5 - Mostrar informação de doente\n6 - Criar registo\n7 - Exit\n");
    int option, c, state = 1;
    char term;
    // Escolha da funcionalidade
    printf("\nInsira a opção que deseja: ");
    while(state){
        // Verifica se é inteiro
        if (scanf("%d%c", &option, &term) != 2 || term != '\n'){
            printf("Introduza uma opção válida (1 - 7): ");
            while ((c = getchar()) != '\n') {}
        // Verifica que está entre 1 e 7
        }else if (option < 1 || option > 7){
            printf("Introduza uma opção válida (1 - 7): ");
        }else
            state=0;
    }
    printf("\n");
    return option;
}

void read_registos(pLista lista){
    // Abrir ficheiro de texto dos registos
    FILE *f = fopen("registos.txt", "r");
    if (f == NULL)
        return;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int i = 0;

    registo * temp_registo = NULL;
    // Percorre todo o ficheiro de texto dos registos
    while ((read = getline(&line, &len, f)) != -1) {
        switch (i){
            case 0:
                // Criar um novo registo
                temp_registo = (registo * ) malloc(sizeof(registo));
                if (temp_registo == NULL)
                    exit(EXIT_FAILURE);
                // Guardar o ID do doente no resgisto
                temp_registo->id_doente = atoi(line);
                break;
            case 1:{
                char* token = strtok(line, "/");
                int n[3] = {0,0,0};
                int j = 0;
                while (token != NULL) {
                    n[j++] = atoi(token);
                    token = strtok(NULL, "/");   
                }
                // Guardar a Data no resgisto
                Data x = {.dia=n[0],.mes=n[1],.ano=n[2]};
                temp_registo->data = x;
                break;
            }
            case 2:
                // Guardar a Tensão Máxima do doente no resgisto
                temp_registo->tensao_max = atoi(line);
                break;
            case 3:
                // Guardar a Tensão Mínima do doente no resgisto
                temp_registo->tensao_min = atoi(line);
                break;
            case 4:
                // Guardar o Peso do doente no resgisto
                temp_registo->peso = atoi(line);
                break;
            case 5:
                // Guardar a Altura do doente no resgisto
                temp_registo->altura = atoi(line);
                // Inserir o registo no doente
                insere2(pesquisa(lista,temp_registo->id_doente)->doente->clinic_data_list,temp_registo);
                i = -1;
                break;
        }
        i++;
    }
    // Fechar o ficheiro
    free(line);
    fclose(f);
}

int read_doentes(pLista lista){
    // Abrir ficheiro de texto dos doentes
    FILE *f = fopen("doentes.txt", "r");
    if (f == NULL)
        return 0;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int i = 0;
    int count = 0;
    doente * temp_doente = NULL;
    // Percorre todo o ficheiro de texto dos doentes
    while ((read = getline(&line, &len, f)) != -1) {
        switch (i)
        {
        case 0:
            // Criar um novo doente
            temp_doente = (doente * ) malloc(sizeof(doente));
            if (temp_doente == NULL)
                exit(EXIT_FAILURE);
            // Guardar o ID do doente
            temp_doente->id = atoi(line);
            break;
        case 1:
            // Guardar o Nome do doente
            temp_doente->nome = strdup(line);
            break;
        case 2:{
            char* token = strtok(line, "/");
            int n[3] = {0,0,0};
            int j = 0;
            while (token != NULL) {
                n[j++] = atoi(token);
                token = strtok(NULL, "/");   
            }
            // Guardar a Data de Nascimento do doente
            Data x = {.dia=n[0],.mes=n[1],.ano=n[2]};
            temp_doente->birthday = x;
            break;
        }
        case 3:
            // Guardar o Número de CC do doente
            temp_doente->cc = strdup(line);
            break;
        case 4:
            // Guardar o Número de Telefone do doente
            temp_doente->telephone =atoi(line);
            break;
        case 5:
            // Guardar o Email do doente
            temp_doente->email = strdup(line);
            // Criar lista de registos para o doente
            temp_doente->clinic_data_list = cria2();
            // Inserir o doente
            insere(lista,temp_doente);
            i = -1;
            // Atualizar o número de doentes na lista
            count++;
        default:
            break;
        }
        i++;
    }
    // Fechar o ficheiro
    free(line);
    fclose(f);
    return count;

}

void save_registo(FILE * f, registo * r){
    // Escrever o registo no ficheiro
    fprintf(f,"%d\n",r->id_doente);
    fprintf(f,"%d/%d/%d\n", r->data.dia,r->data.mes,r->data.ano);
    fprintf(f,"%d\n",r->tensao_max);
    fprintf(f,"%d\n",r->tensao_min);
    fprintf(f,"%d\n",r->peso);
    fprintf(f,"%d\n", r->altura);
}

void save_registos(pLista2 lista){
    // Abrir ficheiro de texto dos registos
    FILE *f = fopen("registos.txt", "a");
    if (f == NULL)
        exit(EXIT_FAILURE);
    pLista2 temp_ptr;
    temp_ptr = lista;
    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    lista = lista->prox;
    // Libertar espaço dos dados de registo
    free(temp_ptr->clinic_data);
    free (temp_ptr);
    // Guardar no ficheiro todos os registos
    while (!vazia2 (lista)) {
        temp_ptr = lista;
        lista = lista->prox;
        save_registo(f,temp_ptr->clinic_data);
        free(temp_ptr->clinic_data);
        free (temp_ptr);
    }
    save_registo(f,lista->clinic_data);
    // Libertar espaço da lista
    free(lista->clinic_data);
    free(lista);
    // Fechar o ficheiro
    fclose(f);
}

void save_doente(FILE * f, doente * d){
    // Escrever informação do doente no ficheiro
    fprintf(f,"%d\n",d->id);
    fprintf(f,"%s", d->nome);
    fprintf(f,"%d/%d/%d\n", d->birthday.dia,d->birthday.mes,d->birthday.ano);
    fprintf(f,"%s",d->cc);
    fprintf(f,"%d\n",d->telephone);
    fprintf(f,"%s", d->email);

    // Libertar espaço das caraterísticas do doente
    free(d->nome);
    free(d->cc);
    free(d->email);
    if (d->clinic_data_list->prox != NULL)
        save_registos(d->clinic_data_list);
    else{
        free(d->clinic_data_list->clinic_data);
        free(d->clinic_data_list);
    }

}

void save_doentes(pLista lista){
    // Abrir ficheiro de texto dos doentes
    FILE *f = fopen("doentes.txt", "w");
    if (f == NULL)
        exit(EXIT_FAILURE);
        
    // Prevenir registos duplicados (por isso apenas apaga-se)
    FILE *f2 = fopen("registos.txt", "w");
    if (f2 == NULL)
        exit(EXIT_FAILURE);
    fclose(f2);

    pLista temp_ptr;
    temp_ptr = lista;
    // Ponteiro para percorrer a lista, começando pelo primeiro elemento
    lista = lista->prox;
    // Libertar espaço dos dados de registo
    free(temp_ptr->doente);
    free (temp_ptr);
    // Guardar no ficheiro todos os doentes
    if (lista == NULL){
        fclose(f);
        return;
    }
    while (!vazia (lista)) {
        temp_ptr = lista;
        lista = lista->prox;
        save_doente(f,temp_ptr->doente);
        free(temp_ptr->doente);
        free (temp_ptr);
    }
    save_doente(f,lista->doente);
    // Libertar espaço da lista
    free(lista->doente);
    free(lista);
    // Fechar o ficheiro de texto de doentes
    fclose(f);
}
