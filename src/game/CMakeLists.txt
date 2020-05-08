cmake_minimum_required(VERSION 3.12)

project(game)

file(GLOB SOURCES "*.c")

file(GLOB HEADERS "*.h")
list(FILTER SOURCES EXCLUDE REGEX ".*.inc.c$")

list(REMOVE_ITEM SOURCES ${PROJECT_SOURCE_DIR}/main.c)

list(APPEND SOURCES ${CMAKE_SOURCE_DIR}/data/behavior_data.c)

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})

target_link_libraries(${PROJECT_NAME} engine)

IF (NOT WIN32)
  target_link_libraries(${PROJECT_NAME} m)
ENDIF()
