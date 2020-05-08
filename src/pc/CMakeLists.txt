cmake_minimum_required(VERSION 3.12)

project(pc)

include_directories(audio controller gfx)

IF (WIN32)
option(SDL2_DIR "Directory containing SDL cmake config" "")
ENDIF ()

IF (WIN32)
option(GLEW_DIR "Directory containing GLEW cmake config" "")
ENDIF ()

find_package(SDL2 REQUIRED PATHS ${SDL2_DIR})

find_package(GLEW REQUIRED PATHS ${GLEW_DIR})

file(GLOB_RECURSE SOURCES "*.c")

file(GLOB_RECURSE HEADERS "*.h")

list(REMOVE_ITEM SOURCES ${PROJECT_SOURCE_DIR}/pc_main.c)

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})
target_link_libraries(${PROJECT_NAME}
  GLEW::glew_s
  SDL2::SDL2-static
  SDL2::SDL2main
)
