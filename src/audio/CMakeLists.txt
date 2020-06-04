cmake_minimum_required(VERSION 3.12)

project(audio)

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/sound/samples)

file(GLOB SOUND_SAMPLE_AIFFS "${CMAKE_SOURCE_DIR}/sound/samples/*/*.aiff")

set(SOUND_SAMPLE_AIFCS "")
foreach(SOUND_SAMPLE_AIFF ${SOUND_SAMPLE_AIFFS})
  string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR} SOUND_SAMPLE_AIFC ${SOUND_SAMPLE_AIFF})
  string(REPLACE ".aiff" ".table" SOUND_SAMPLE_TABLE ${SOUND_SAMPLE_AIFC})
  string(REPLACE ".aiff" ".aifc" SOUND_SAMPLE_AIFC ${SOUND_SAMPLE_AIFC})
  list(APPEND SOUND_SAMPLE_AIFCS ${SOUND_SAMPLE_AIFC})
  add_custom_command(
    OUTPUT ${SOUND_SAMPLE_AIFC}
    COMMAND aiff_extract_codebook ${SOUND_SAMPLE_AIFF} > ${SOUND_SAMPLE_TABLE}
    COMMAND vadpcm_enc -c ${SOUND_SAMPLE_TABLE} ${SOUND_SAMPLE_AIFF} ${SOUND_SAMPLE_AIFC}
    COMMENT "Generating ${SOUND_SAMPLE_AIFC} from ${SOUND_SAMPLE_AIFF}"
    DEPENDS ${SOUND_SAMPLE_AIFF}
  )
endforeach()

set(SOUND_SEQUENCE_FILES "")
file(GLOB SOUND_SEQUENCE_FILES_ASM "${CMAKE_SOURCE_DIR}/sound/sequences/*.s" "${CMAKE_SOURCE_DIR}/sound/sequences/${ROM_VERSION}/*.s")
foreach(SOUND_SEQUENCE_FILE_ASM ${SOUND_SEQUENCE_FILES_ASM})
  string(REPLACE ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR} SOUND_SEQUENCE_FILE ${SOUND_SEQUENCE_FILE_ASM})
  string(REPLACE ".s" ".o" SOUND_SEQUENCE_FILE_OBJ ${SOUND_SEQUENCE_FILE})
  string(REPLACE ".s" ".m64" SOUND_SEQUENCE_FILE ${SOUND_SEQUENCE_FILE})
  list(APPEND SOUND_SEQUENCE_FILES ${SOUND_SEQUENCE_FILE})
  add_custom_command(
    OUTPUT ${SOUND_SEQUENCE_FILE}
    #COMMAND as -march=vr4300 -mabi=32 -I ${CMAKE_SOURCE_DIR}/include -I ${CMAKE_BINARY_DIR} --defsym VERSION_US=1 --defsym F3D_OLD=1 -o ${SOUND_SEQUENCE_FILE_OBJ} ${SOUND_SEQUENCE_FILE_ASM}
    COMMAND as -I ${CMAKE_SOURCE_DIR}/include -I ${CMAKE_BINARY_DIR} --defsym VERSION_US=1 --defsym F3D_OLD=1 -o ${SOUND_SEQUENCE_FILE_OBJ} ${SOUND_SEQUENCE_FILE_ASM}
    COMMAND objcopy -j .rodata ${SOUND_SEQUENCE_FILE_OBJ} -O binary ${SOUND_SEQUENCE_FILE}
    COMMENT "Generating ${SOUND_SEQUENCE_FILE} from ${SOUND_SEQUENCE_FILE_ASM}"
    DEPENDS ${SOUND_SEQUENCE_FILE_ASM}
  )
endforeach()
file(GLOB SOUND_SEQUENCE_FILES_M64 "${CMAKE_SOURCE_DIR}/sound/sequences/*.m64" "${CMAKE_SOURCE_DIR}/sound/sequences/${ROM_VERSION}/*.m64")
list(APPEND SOUND_SEQUENCE_FILES ${SOUND_SEQUENCE_FILES_M64})

file(GLOB SOUND_BANK_FILES "${CMAKE_SOURCE_DIR}/sound/sound_banks/*.json")

add_custom_command(
  OUTPUT
    ${CMAKE_BINARY_DIR}/sound/sound_data.ctl
    ${CMAKE_BINARY_DIR}/sound/sound_data.tbl
	COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/assemble_sound.py ${CMAKE_BINARY_DIR}/sound/samples/ ${CMAKE_SOURCE_DIR}/sound/sound_banks/ ${CMAKE_BINARY_DIR}/sound/sound_data.ctl ${CMAKE_BINARY_DIR}/sound/sound_data.tbl ${SM_VERSION_CFLAGS} --endian little --bitwidth 64
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${SOUND_BANK_FILES} ${SOUND_SAMPLE_AIFCS}
  COMMENT "Generating sound_data.ctl and sound_data.tbl"
)

add_custom_command(
  OUTPUT
    ${CMAKE_BINARY_DIR}/sound/bank_sets
    ${CMAKE_BINARY_DIR}/sound/sequences.bin
	COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/assemble_sound.py --sequences ${CMAKE_BINARY_DIR}/sound/sequences.bin ${CMAKE_BINARY_DIR}/sound/bank_sets ${CMAKE_SOURCE_DIR}/sound/sound_banks/ ${CMAKE_SOURCE_DIR}/sound/sequences.json ${SOUND_SEQUENCE_FILES} ${SM_VERSION_CFLAGS} --endian little --bitwidth 64
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${SOUND_BANK_FILES} ${CMAKE_SOURCE_DIR}/sound/sequences.json ${SOUND_SEQUENCE_FILES}
  COMMENT "Generating bank_sets and sequences.bin"
)

add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/sound/sound_data.ctl.c
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/binary_to_c_array.py ${CMAKE_BINARY_DIR}/sound/sound_data.ctl gSoundDataADSR
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${CMAKE_BINARY_DIR}/sound/sound_data.ctl
  COMMENT "Creating sound_data.ctl.c from sound_data.ctl"
)

add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/sound/sound_data.tbl.c
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/binary_to_c_array.py ${CMAKE_BINARY_DIR}/sound/sound_data.tbl gSoundDataRaw
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${CMAKE_BINARY_DIR}/sound/sound_data.tbl
  COMMENT "Creating sound_data.tbl.c from sound_data.tbl"
)

add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/sound/sequences.bin.c
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/binary_to_c_array.py ${CMAKE_BINARY_DIR}/sound/sequences.bin gMusicData
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${CMAKE_BINARY_DIR}/sound/sequences.bin
  COMMENT "Creating sequences.bin.c from sequences.bin"
)

add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/sound/bank_sets.c
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/binary_to_c_array.py ${CMAKE_BINARY_DIR}/sound/bank_sets gBankSetsData
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  DEPENDS ${CMAKE_BINARY_DIR}/sound/bank_sets
  COMMENT "Creating bank_sets.c from bank_sets"
)

file(GLOB SOURCES "*.c")

list(APPEND SOURCES
  ${CMAKE_BINARY_DIR}/sound/sound_data.ctl.c
  ${CMAKE_BINARY_DIR}/sound/sound_data.tbl.c
  ${CMAKE_BINARY_DIR}/sound/sequences.bin.c
  ${CMAKE_BINARY_DIR}/sound/bank_sets.c
)

file(GLOB HEADERS "*.h")

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})
add_dependencies(${PROJECT_NAME} extract_assets)

target_link_libraries(${PROJECT_NAME} buffers)
