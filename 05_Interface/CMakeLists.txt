cmake_minimum_required(VERSION 3.8)
project(interface)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Add .msg files under msg/ and .srv files under srv/.
file(GLOB INTERFACE_FILES CONFIGURE_DEPENDS
  RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
  "msg/*.msg"
  "srv/*.srv"
)

if(INTERFACE_FILES)
  rosidl_generate_interfaces(${PROJECT_NAME}
    ${INTERFACE_FILES}
  )
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
