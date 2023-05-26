cmake_minimum_required(VERSION 3.25)
project(Sphinx)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

set(CMAKE_PREFIX_PATH "/home/carl/Qt/6.4.3/gcc_64")

find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        Network
        REQUIRED)


aux_source_directory(src SRC_LIST)

add_executable(Sphinx ${SRC_LIST})

target_link_libraries(Sphinx
        Qt::Core
        Qt::Gui
        Qt::Widgets
        Qt::Network
        )

