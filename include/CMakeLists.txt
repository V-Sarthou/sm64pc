cmake_minimum_required(VERSION 3.12)

project(include)

set(GENERATED_HEADERS
        ${PROJECT_BINARY_DIR}/text_strings.h
        ${PROJECT_BINARY_DIR}/text_menu_strings.h
        )

add_custom_target(
        ${PROJECT_NAME}
        DEPENDS ${GENERATED_HEADERS}
)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/text_strings.h
        COMMAND textconv ${CMAKE_SOURCE_DIR}/charmap.txt ${CMAKE_SOURCE_DIR}/include/text_strings.h.in ${CMAKE_BINARY_DIR}/include/text_strings.h
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        DEPENDS ${CMAKE_SOURCE_DIR}/include/text_strings.h.in
        COMMENT "Generating text_strings.."
)

add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/include/text_menu_strings.h
        COMMAND textconv ${CMAKE_SOURCE_DIR}/charmap_menu.txt ${CMAKE_SOURCE_DIR}/include/text_menu_strings.h.in ${CMAKE_BINARY_DIR}/include/text_menu_strings.h
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        DEPENDS ${CMAKE_SOURCE_DIR}/include/text_menu_strings.h.in
        COMMENT "Generating text_menu_strings.."
)