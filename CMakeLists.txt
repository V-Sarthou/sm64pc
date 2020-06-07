cmake_minimum_required(VERSION 3.12)


project(sm64pc)

set(ROM_VERSION "us" CACHE STRING "Rom version")
set_property(CACHE ROM_VERSION PROPERTY STRINGS us eu jp sh)
option(ROM_VERSION "Rom version")

find_package(Python REQUIRED)
set(PYTHON_EXECUTABLE ${Python_EXECUTABLE})

include_directories(include)

add_subdirectory(tools)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(NOT EXISTS ${CMAKE_SOURCE_DIR}/baserom.${ROM_VERSION}.z64)
  message(FATAL_ERROR "Please provide ${CMAKE_SOURCE_DIR}/baserom.${ROM_VERSION}.z64")
endif()

set(SM_VERSION_CFLAGS -D VERSION_US -D NON_MATCHING -D AVOID_UB)
add_definitions(${SM_VERSION_CFLAGS})
add_definitions(-DF3DEX_GBI_2E=1)
add_definitions(-DUSE_SDL=2)

option(SM64_EXT_OPTIONS_MENU "Extended options menu" TRUE)
if(${SM64_EXT_OPTIONS_MENU})
  add_definitions(-DEXT_OPTIONS_MENU=1)
endif()

option(SM64_BETTERCAMERA "Analog camera control and mouse look" FALSE)
if(${SM64_BETTERCAMERA})
  add_definitions(-DBETTERCAMERA=1)
endif()

option(SM64_NODRAWINGDISTANCE "Disable drawing distances" FALSE)
if(${SM64_NODRAWINGDISTANCE})
  add_definitions(-DNODRAWINGDISTANCE=1)
endif()

option(SM64_TEXTURE_FIX "Model and texture fixes" FALSE)
if(${SM64_TEXTURE_FIX})
  add_definitions(-DTEXTURE_FIX=1)
endif()

option(SM64_TEXTSAVES "Text-based save support" FALSE)
if(${SM64_TEXTSAVES})
  add_definitions(-DTEXTSAVES=1)
endif()

option(SM64_EXTERNAL_DATA "Load resources from external files" FALSE)
if(${SM64_EXTERNAL_DATA})
  add_definitions(-DEXTERNAL_DATA=1)
endif()

option(SM64_LEGACY_GL "Use OpenGL 1.3 renderer" FALSE)
if(${SM64_LEGACY_GL})
  add_definitions(-DLEGACY_GL=1)
endif()

set(HEXDUMP_PATH "hexdump" CACHE FILEPATH "Path to hexdump executable")

IF (WIN32)
    if(NOT EXISTS ${HEXDUMP_PATH})
      message(FATAL_ERROR "Please provide the path to hexdump executable.")
    endif()

    set(BUILD_SHARED_LIBS OFF)
    set(CompilerFlags
        CMAKE_C_FLAGS
        CMAKE_C_FLAGS_DEBUG
        CMAKE_C_FLAGS_RELEASE
        )
    foreach(CompilerFlag ${CompilerFlags})
      string(REPLACE "/MD" "/MT" ${CompilerFlag} "${${CompilerFlag}}")
    endforeach()
ELSE ()
    set(LINK_LIBRARIES GL m)
ENDIF ()


include_directories(
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
