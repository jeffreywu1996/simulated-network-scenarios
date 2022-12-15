cmake_minimum_required(VERSION 3.5)
project(int_test)

if(NOT MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
else()
  add_definitions(-D_WIN32_WINNT=0x600)
endif()


file(GLOB filepaths cpp_test/*.cpp)
foreach(filepath ${filepaths})
  get_filename_component(filename ${filepath} NAME_WE)
  add_executable(${filename} ${filepath})
  target_link_libraries(${filename} pthread middleware curl)
endforeach()
