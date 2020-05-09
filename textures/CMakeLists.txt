cmake_minimum_required(VERSION 3.12)

project(textures)

add_custom_target(extract_assets
        COMMAND python ${CMAKE_SOURCE_DIR}/extract_assets.py ${ROM_VERSION}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        DEPENDS skyconv n64graphics mio0 aifc_decode
        COMMENT "Extracting assets from: baserom.${ROM_VERSION}.z64"
)

add_custom_target(clean_textures
        COMMAND python ${CMAKE_SOURCE_DIR}/extract_assets.py --clean
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Cleaning textures.."
)

file(GLOB_RECURSE TEXTURE_PNGS "${CMAKE_SOURCE_DIR}/textures/*.*.png" "${CMAKE_SOURCE_DIR}/actors/*.*.png" "${CMAKE_SOURCE_DIR}/levels/*.*.png")
set(TEXTURES_HEX)
foreach(TEXTURE_PNG ${TEXTURE_PNGS})
    file(RELATIVE_PATH TEXTURE_REL_PATH ${CMAKE_SOURCE_DIR} ${TEXTURE_PNG})
    get_filename_component(TEXTURE_DUMPED ${TEXTURE_REL_PATH} NAME_WLE)
    get_filename_component(REL_PATH ${TEXTURE_REL_PATH} DIRECTORY)
    get_filename_component(TEXTURE_FORMAT_TEMP ${TEXTURE_DUMPED} LAST_EXT)
    string(SUBSTRING ${TEXTURE_FORMAT_TEMP} 1 -1 TEXTURE_FORMAT)
    file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/${REL_PATH})
    set(TEXTURE_HEX ${CMAKE_BINARY_DIR}/${REL_PATH}/${TEXTURE_DUMPED}.inc.c)
    list(APPEND TEXTURES_HEX ${TEXTURE_HEX})
    add_custom_command(
            OUTPUT ${TEXTURE_HEX}
            COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/${REL_PATH}
            COMMAND n64graphics -i ${CMAKE_BINARY_DIR}/${REL_PATH}/${TEXTURE_DUMPED} -g ${CMAKE_SOURCE_DIR}/${TEXTURE_REL_PATH} -f ${TEXTURE_FORMAT}
            COMMAND ${HEXDUMP_PATH} -v -e \"1/1 0x%%X,\" ${CMAKE_BINARY_DIR}/${REL_PATH}/${TEXTURE_DUMPED} > ${TEXTURE_HEX}
            DEPENDS extract_assets
            COMMENT "Converting texture ${TEXTURE_PNG} to ${TEXTURE_HEX}"
    )
endforeach()

add_custom_target(
        ${PROJECT_NAME}
        DEPENDS extract_assets ${TEXTURES_HEX}
)
