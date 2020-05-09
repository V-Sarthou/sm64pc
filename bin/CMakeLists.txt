cmake_minimum_required(VERSION 3.12)

project(bin)

file(GLOB SOURCES "*.c" "eu/*.c")

file(GLOB SKYBOXES "${CMAKE_SOURCE_DIR}/textures/skyboxes/*.png")
foreach(SKYBOX ${SKYBOXES})
  get_filename_component(SKYBOX_NAME ${SKYBOX} NAME_WLE)
  set(SKYBOX_C_FILE ${CMAKE_BINARY_DIR}/bin/${SKYBOX_NAME}_skybox.c)
  add_custom_command(
    OUTPUT ${SKYBOX_C_FILE}
    COMMAND skyconv --type sky --split ${SKYBOX} ${CMAKE_BINARY_DIR}/bin
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    DEPENDS extract_assets
    COMMENT "Generating ${SKYBOX_NAME} skybox C file"
  )
  list(APPEND SOURCES ${SKYBOX_C_FILE})
endforeach()

add_library(${PROJECT_NAME} STATIC ${SOURCES})
add_dependencies(${PROJECT_NAME} textures)

set(LANG_VERSIONS
  de
  fr
  jp
  us
)

foreach(LANG_VERSION ${LANG_VERSIONS})
  set(TEXT_HEADERS
    ${CMAKE_SOURCE_DIR}/text/${LANG_VERSION}/courses.h
    ${CMAKE_SOURCE_DIR}/text/${LANG_VERSION}/dialogs.h
  )
  set(VERSION_DEFINES_C_OUTPUT ${CMAKE_BINARY_DIR}/text/${LANG_VERSION}/define_text.inc.c)
  add_custom_target(${LANG_VERSION}_text DEPENDS textconv ${TEXT_HEADERS})
  add_custom_command(
    TARGET ${LANG_VERSION}_text
    COMMAND cpp ${SM_VERSION_CFLAGS} ${CMAKE_SOURCE_DIR}/text/define_text.inc.c -o ${VERSION_DEFINES_C_OUTPUT} -I ${CMAKE_SOURCE_DIR}/text/${LANG_VERSION}/
    COMMAND textconv ${CMAKE_SOURCE_DIR}/charmap.txt ${VERSION_DEFINES_C_OUTPUT} ${VERSION_DEFINES_C_OUTPUT}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating text C file for ${LANG_VERSION} version"
  )
  add_dependencies(${PROJECT_NAME} ${LANG_VERSION}_text)
endforeach()
