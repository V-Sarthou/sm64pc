cmake_minimum_required(VERSION 3.12)

project(pc)

include(FetchContent)

include_directories(audio controller gfx)

set(PC_LINK_LIBRARIES)
set(PC_DEFINITIONS)

set(SOURCES
  cheats.c
  cliopts.c
  configfile.c
  ini.c
  mixer.c
  platform.c
  ultra_reimplementation.c

  audio/audio_null.c
  audio/audio_sdl.c

  controller/controller_emscripten_keyboard.c
  controller/controller_entry_point.c
  controller/controller_keyboard.c
  controller/controller_recorded_tas.c
  controller/controller_sdl.c

  fs/dirtree.c
  fs/fs.c
  fs/fs_packtype_dir.c
  fs/fs_packtype_zip.c

  gfx/gfx_opengl.c
  gfx/gfx_opengl_legacy.c
  gfx/gfx_pc.c
  gfx/gfx_sdl2.c
)

set(HEADERS
  cheats.h
  cliopts.h
  configfile.h
  ini.h
  mixer.h
  platform.h

  audio/audio_api.h
  audio/audio_null.h
  audio/audio_sdl.h

  controller/controller_api.h
  controller/controller_emscripten_keyboard.h
  controller/controller_keyboard.h
  controller/controller_recorded_tas.h
  controller/controller_sdl.h

  fs/dirtree.h
  fs/fs.h

  gfx/gfx_cc.h
  gfx/gfx_opengl.h
  gfx/gfx_pc.h
  gfx/gfx_rendering_api.h
  gfx/gfx_screen_config.h
  gfx/gfx_sdl.h
  gfx/gfx_window_manager_api.h
)

set(GL_LOADER "GLAD" CACHE STRING "OpenGL loader library")
set_property(CACHE GL_LOADER PROPERTY STRINGS GLEW GLAD)

if(GL_LOADER STREQUAL "GLEW")
  if(WIN32)
    set(GLEW_DIR "" CACHE PATH "Directory containing GLEW cmake config")
  endif()
  find_package(GLEW PATHS ${GLEW_DIR})
endif()

if(NOT GLEW_FOUND)
  FetchContent_Declare(
    glad
    GIT_REPOSITORY https://github.com/Dav1dde/glad.git
    GIT_TAG        master
  )
  FetchContent_GetProperties(glad)
  if(NOT glad_POPULATED)
    FetchContent_Populate(glad)
  endif()

  if(${SM64_LEGACY_GL})
    set(GLAD_API "gl=1.3" CACHE STRING "" FORCE)
  else()
    set(GLAD_API "gles2=2.0" CACHE STRING "" FORCE)
  endif()

  set(USE_MSVC_RUNTIME_LIBRARY_DLL OFF CACHE BOOL "" FORCE)
  add_subdirectory(${glad_SOURCE_DIR} ${glad_BINARY_DIR})
  list(APPEND PC_LINK_LIBRARIES glad)
  list(APPEND PC_DEFINITIONS SM64_USE_GLAD)
else()
  list(APPEND PC_LINK_LIBRARIES GLEW::glew_s)
endif()


FetchContent_Declare(
  sdl2
  GIT_REPOSITORY https://github.com/SDL-mirror/SDL.git
  GIT_TAG        master
)
FetchContent_GetProperties(sdl2)
if(NOT sdl2_POPULATED)
  FetchContent_Populate(sdl2)
endif()
set(LIBC ON CACHE STRING "" FORCE)
set(FORCE_STATIC_VCRT ON CACHE STRING "" FORCE)
add_subdirectory(${sdl2_SOURCE_DIR} ${sdl2_BINARY_DIR})
target_compile_definitions(SDL2-static PRIVATE wcslcpy=wcsncpy wcslcat=wcsncat)
list(APPEND PC_LINK_LIBRARIES SDL2-static)

add_library(${PROJECT_NAME} STATIC ${SOURCES} ${HEADERS})
target_compile_definitions(${PROJECT_NAME} PUBLIC ${PC_DEFINITIONS})
target_link_libraries(${PROJECT_NAME} ${PC_LINK_LIBRARIES})
