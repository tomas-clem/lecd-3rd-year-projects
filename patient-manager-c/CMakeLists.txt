CMAKE_MINIMUM_REQUIRED(VERSION 3.10)

# set the project name
PROJECT(pppProject)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin")

# add the executable
ADD_EXECUTABLE(main main.c lista_doentes.c data.c lista_registos.c)

