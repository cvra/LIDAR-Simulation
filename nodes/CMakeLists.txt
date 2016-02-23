cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

find_package(Boost REQUIRED COMPONENTS system)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIRS})
link_directories(${PROTUBUF_LIBRARY_DIRS})

find_package(gazebo REQUIRED)
include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")

add_executable(robotpose robotpose.cpp)
target_link_libraries(robotpose
    ${GAZEBO_LIBRARIES}
    ${Boost_LIBRARIES}
    ${PROTUBUF_LIBRARIES}
    pthread
)

add_executable(laserscan laserscan.cpp)
target_link_libraries(laserscan
    ${GAZEBO_LIBRARIES}
    ${Boost_LIBRARIES}
    ${PROTUBUF_LIBRARIES}
    pthread
)

include (FindPkgConfig)
if (PKG_CONFIG_FOUND)
  pkg_check_modules(GAZEBO gazebo)
endif()
