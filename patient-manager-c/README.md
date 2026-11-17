# Patient Manager in C

A command-line application for a doctor to manage patients and their clinical records (blood pressure, weight, height), written in C with linked lists.

*Developed with Óscar Ferrão. Course: Principles of Procedural Programming, University of Coimbra, 2023/24. Programmer's manual: [programmer-manual-pt.pdf](programmer-manual-pt.pdf) (Portuguese).*

## Features

1. Add a patient (ID, name, date of birth, ID card number, phone, email), with input validation.
2. Delete a patient.
3. List patients alphabetically.
4. List patients whose maximum blood pressure is above a given value.
5. Show a patient's details.
6. Add a clinical record to a patient.

Patients are kept in a linked list. Each patient has their own linked list of clinical records. Data is loaded from `doentes.txt` (patients) and `registos.txt` (records) at start-up, and patients are saved back to `doentes.txt` on exit.

| File | Contents |
|---|---|
| `main.c` | Menu and input handling |
| `lista_doentes.c/.h` | Patient list: insert, delete, search, sorted listing |
| `lista_registos.c/.h` | Clinical record list |
| `data.c/.h` | Dates and date validation |
| `doente.h`, `registo.h` | Data structures |

## How to build and run

```bash
cmake -S . -B build
cmake --build build
./bin/main        # run from this folder so it finds doentes.txt and registos.txt
```

Re-tested for this repository with GCC 11 on Ubuntu: it builds, loads the sample data, and lists, searches and filters correctly.

## Known limitations

- Clinical records added during a session are not saved: only `doentes.txt` is written on exit.
- Patients read from `doentes.txt` are not validated (the sample file has a test entry with the date `12/45/5656`).
- The program's text is in Portuguese.
