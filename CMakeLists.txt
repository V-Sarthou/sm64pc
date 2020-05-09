cmake_minimum_required(VERSION 3.12)


project(sm64pc)

set(ROM_VERSION "us" CACHE STRING "Rom version")
set_property(CACHE ROM_VERSION PROPERTY STRINGS us eu jp sh)
option(ROM_VERSION "Rom version")

add_subdirectory(tools)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(NOT EXISTS ${CMAKE_SOURCE_DIR}/baserom.${ROM_VERSION}.z64)
  message(FATAL_ERROR "Please provide ${CMAKE_SOURCE_DIR}/baserom.${ROM_VERSION}.z64")
endif()

set(SM_VERSION_CFLAGS "-DVERSION_US -DNON_MATCHING -DAVOID_UB")
add_definitions(${SM_VERSION_CFLAGS})

set(HEXDUMP_PATH "hexdump" CACHE FILEPATH "")

IF (WIN32)
    option(HEXDUMP_PATH "Path to hexdump executable")
    if(NOT EXISTS ${HEXDUMP_PATH})
      message(FATAL_ERROR "Please provide the path to hexdump executable.")
    endif()

    #set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -mwindows")
    set(LINK_LIBRARIES setupapi dinput8 user32 gdi32 imm32 ole32 oleaut32 shell32 winmm version uuid)

    set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
    set(BUILD_SHARED_LIBS OFF)
    #set(CMAKE_EXE_LINKER_FLAGS "-static")
ELSE ()
    set(LINK_LIBRARIES SDL2main SDL2 GL m)
ENDIF ()


include_directories(
        include
        src
        levels
        lib
        .
        ${CMAKE_BINARY_DIR}
        ${CMAKE_BINARY_DIR}/include
)

add_subdirectory(include)
add_subdirectory(textures)
add_subdirectory(bin)
add_subdirectory(actors)
add_subdirectory(levels)
add_subdirectory(src/buffers)
add_subdirectory(src/audio)
add_subdirectory(src/engine)
add_subdirectory(src/goddard)
add_subdirectory(src/pc)
add_subdirectory(src/menu)
add_subdirectory(src/game)
add_subdirectory(lib)

set(SOURCES src/pc/pc_main.c)
add_executable(${PROJECT_NAME} ${SOURCES})
target_link_libraries(${PROJECT_NAME} game audio goddard pc menu ${LINK_LIBRARIES})
