cmake_minimum_required(VERSION 3.12)

project(levels)

set(CAKE_TEXTURE_NAME cake)
set(CAKE_TEXTURE_TYPE cake)
if(${ROM_VERSION} EQUAL "eu")
  set(CAKE_TEXTURE_NAME cake_eu)
  set(CAKE_TEXTURE_TYPE cake-eu)
endif()
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/levels/ending)
add_custom_target(cake_texture
  COMMAND skyconv --type ${CAKE_TEXTURE_TYPE} --split ${CMAKE_SOURCE_DIR}/levels/ending/${CAKE_TEXTURE_NAME}.png ${CMAKE_BINARY_DIR}/levels/ending
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS extract_assets
  COMMENT "Generating cake texture C file"
)

file(GLOB_RECURSE SOURCES "*.c")
list(FILTER SOURCES EXCLUDE REGEX ".*.inc.c$")

file(GLOB_RECURSE HEADERS "*.h")

set(LEVELS_HEADER_FILE ${CMAKE_BINARY_DIR}/include/level_headers.h)
add_custom_command(
  OUTPUT ${LEVELS_HEADER_FILE}
  COMMAND cpp -I ${CMAKE_SOURCE_DIR} ${CMAKE_SOURCE_DIR}/levels/level_headers.h.in > ${CMAKE_BINARY_DIR}/include/level_headers.h.out
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/output_level_headers.py ${CMAKE_BINARY_DIR}/include/level_headers.h.out ${LEVELS_HEADER_FILE}
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${CMAKE_SOURCE_DIR}/levels/level_headers.h.in
  COMMENT "Generating levels header file"
)
list(APPEND HEADERS ${LEVELS_HEADER_FILE})

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})
add_dependencies(${PROJECT_NAME} textures cake_texture)

set(LANG_VERSIONS
  de
  fr
  jp
  us
)

foreach(LANG_VERSION ${LANG_VERSIONS})
  set(COURSE_HEADER ${CMAKE_SOURCE_DIR}/text/${LANG_VERSION}/courses.h)
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/text/${LANG_VERSION})
  set(VERSION_COURSES_C_OUTPUT ${CMAKE_BINARY_DIR}/text/${LANG_VERSION}/define_courses.inc.c)
  add_custom_target(${LANG_VERSION}_courses DEPENDS textconv ${COURSE_HEADER})
  add_custom_command(
    TARGET ${LANG_VERSION}_courses
  	COMMAND cpp ${SM_VERSION_CFLAGS} ${CMAKE_SOURCE_DIR}/text/define_courses.inc.c -o ${VERSION_COURSES_C_OUTPUT} -I ${CMAKE_SOURCE_DIR}/text/${LANG_VERSION}/
    COMMAND textconv ${CMAKE_SOURCE_DIR}/charmap.txt ${VERSION_COURSES_C_OUTPUT} ${VERSION_COURSES_C_OUTPUT}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating courses C file for ${LANG_VERSION} version"
  )
  add_dependencies(${PROJECT_NAME} ${LANG_VERSION}_courses)
endforeach()
