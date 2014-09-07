cmake_minimum_required(VERSION 2.8.9)

project(CornerAnnotation)

set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/CornerAnnotation")
set(EXTENSION_CATEGORY "IGT")
set(EXTENSION_CONTRIBUTORS "Atsushi Yamada (Shiga University of Medical Science)")
set(EXTENSION_DESCRIPTION "This is an module to display annotations, time count, node elements on each panels on the Slicer user interface")
set(EXTENSION_ICONURL "http://www.slicer.org/slicerWiki/images/e/e1/CornerAnnotationIcon.png")
set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/2/2a/CA-1.png")

find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

add_subdirectory(CornerAnnotation)

include(${Slicer_EXTENSION_CPACK})