cmake_minimum_required(VERSION 3.12)

project(game)

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/assets)

file(GLOB MARIO_ANIM_DEPS "${CMAKE_SOURCE_DIR}/assets/anims/*.inc.c")
add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/assets/mario_anim_data.c
	COMMAND python ${CMAKE_SOURCE_DIR}/tools/mario_anims_converter.py > ${CMAKE_BINARY_DIR}/assets/mario_anim_data.c
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${MARIO_ANIM_DEPS}
  COMMENT "Extracting mario anims from: assets/anims"
)

file(GLOB DEMO_DATA_DEPS "${CMAKE_SOURCE_DIR}/assets/demos/*.bin")
list(APPEND DEMO_DATA_DEPS ${CMAKE_SOURCE_DIR}/assets/demo_data.json)
add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/assets/demo_data.c
	COMMAND python ${CMAKE_SOURCE_DIR}/tools/demo_data_converter.py ${CMAKE_SOURCE_DIR}/assets/demo_data.json ${SM_VERSION_CFLAGS} > ${CMAKE_BINARY_DIR}/assets/demo_data.c
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${DEMO_DATA_DEPS}
  COMMENT "Extracting demo data from: assets/demos"
)

file(GLOB SOURCES "*.c")

file(GLOB HEADERS "*.h")
list(FILTER SOURCES EXCLUDE REGEX ".*.inc.c$")

list(REMOVE_ITEM SOURCES ${PROJECT_SOURCE_DIR}/main.c)

list(APPEND SOURCES
  ${CMAKE_SOURCE_DIR}/data/behavior_data.c
  ${CMAKE_BINARY_DIR}/assets/mario_anim_data.c
  ${CMAKE_BINARY_DIR}/assets/demo_data.c
)

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})

target_link_libraries(${PROJECT_NAME} bin actors levels engine)

IF (NOT WIN32)
  target_link_libraries(${PROJECT_NAME} m)
ENDIF()
