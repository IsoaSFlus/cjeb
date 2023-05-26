cmake_minimum_required(VERSION 3.8)

project(fcitx5-table-hanma VERSION 1.0.0)

find_package(ECM 1.0 REQUIRED)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

include(FeatureSummary)
include(GNUInstallDirs)
include(ECMUninstallTarget)

find_package(Gettext REQUIRED)
find_package(LibIMETable REQUIRED)
find_package(Fcitx5Core REQUIRED)

set(MB_FILE)
set(CONF_FILE)

fcitx5_translate_desktop_file("hanma.conf.in" "hanma.conf")
add_custom_command(OUTPUT "hanma.main.dict"
	DEPENDS "hanma.txt"
	COMMAND LibIME::tabledict ARGS "${CMAKE_CURRENT_SOURCE_DIR}/hanma.txt"
	"${CMAKE_CURRENT_BINARY_DIR}/hanma.main.dict")
set(MB_FILE ${MB_FILE} "${CMAKE_CURRENT_BINARY_DIR}/hanma.main.dict")
set(CONF_FILE ${CONF_FILE} "${CMAKE_CURRENT_BINARY_DIR}/hanma.conf")

add_custom_target(table_data ALL DEPENDS ${MB_FILE})

install(FILES ${CONF_FILE} DESTINATION "${FCITX_INSTALL_PKGDATADIR}/inputmethod")
install(FILES ${MB_FILE} DESTINATION "${FCITX_INSTALL_PKGDATADIR}/table")

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
