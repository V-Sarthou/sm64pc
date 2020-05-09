cmake_minimum_required(VERSION 3.12)

project(sm64pc_tools)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(n64graphics
  n64graphics.c
  utils.c
)
target_compile_definitions(n64graphics PUBLIC N64GRAPHICS_STANDALONE)
target_include_directories(n64graphics PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(n64graphics_ci
  n64graphics_ci_dir/n64graphics_ci.c
  n64graphics_ci_dir/exoquant/exoquant.c
  n64graphics_ci_dir/utils.c
)
target_include_directories(n64graphics_ci PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/n64graphics_ci_dir)

add_executable(mio0
  libmio0.c
)
target_compile_definitions(mio0 PUBLIC MIO0_STANDALONE)

add_executable(n64cksum
  n64cksum.c
  libmio0.c
  libsm64.c
  utils.c
)

add_executable(textconv
  textconv.c
  utf8.c
  hashtable.c
)

add_executable(patch_libultra_math
  patch_libultra_math.c
)

add_executable(iplfontutil
  iplfontutil.c
)
target_include_directories(iplfontutil PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(aifc_decode
  aifc_decode.c
)

add_executable(aiff_extract_codebook
  aiff_extract_codebook.c
)

add_executable(vadpcm_enc
  sdk-tools/adpcm/vadpcm_enc.c
  sdk-tools/adpcm/vpredictor.c
  sdk-tools/adpcm/quant.c
  sdk-tools/adpcm/util.c
  sdk-tools/adpcm/vencode.c
)

if(NOT WIN32)
  add_executable(tabledesign
    sdk-tools/tabledesign/codebook.c
    sdk-tools/tabledesign/estimate.c
    sdk-tools/tabledesign/print.c
    sdk-tools/tabledesign/tabledesign.c
  )
  target_link_libraries(tabledesign audiofile)
endif()

add_executable(extract_data_for_mio
  extract_data_for_mio.c
)

add_executable(skyconv
  skyconv.c
  n64graphics.c
  utils.c
)
target_include_directories(skyconv PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
if(NOT WIN32)
  target_link_libraries(skyconv m)
endif()
