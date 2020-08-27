#


cmake_minimum_required(VERSION 3.15)
project(testingclion)

find_package( OpenCV REQUIRED )
INCLUDE_DIRECTORIES( ${OpenCV_INCLUDE_DIRS} )

find_package( PkgConfig REQUIRED)

pkg_search_module( TESSERACT REQUIRED tesseract )

pkg_search_module( LEPTONICA REQUIRED lept )

include_directories( ${TESSERACT_INCLUDE_DIRS} )

include_directories( ${LEPTONICA_INCLUDE_DIRS} )

link_directories( ${TESSERACT_LIBRARY_DIRS} )

link_directories( ${LEPTONICA_LIBRARY_DIRS} )

set(CMAKE_CXX_STANDARD 17)

add_executable(OCR main.cpp main.h)

target_link_libraries( OCR ${OpenCV_LIBS} )

target_link_libraries( OCR ${TESSERACT_LIBRARIES} )

target_link_libraries( OCR ${LEPTONICA_LIBRARIES} )

include_directories(${OpenCV_INCLUDE_DIRS})