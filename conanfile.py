from conans import ConanFile, CMake, tools
import os
from io import StringIO
import shutil
from glob import glob


class Open3dConan(ConanFile):
    version = "2.0"

    name = "teaserplusplus"
    license = "https://github.com/IntelVCL/Open3D/raw/master/LICENSE"
    description = "TEASER++ is a fast and certifiably-robust point cloud registration library written in C++, with Python and MATLAB bindings."
    url = "https://github.com/MIT-SPARK/TEASER-plusplus"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    requires = (
        "eigen/[>=3.3.9]@camposs/stable",
        "Boost/1.75.0@camposs/stable",
        # "pcl/1.11.1-r1@camposs/stable",
        
        )

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        }

    default_options = (
        "shared=True",
        "fPIC=True",
        )

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    
    def source(self):
        source_url = "https://github.com/MIT-SPARK/TEASER-plusplus/archive/refs/tags/v{}.tar.gz".format(self.version)
        archive_name = "TEASER-plusplus-{0}".format(self.version)
        tools.get(source_url)
        os.rename(archive_name, self.source_subfolder)


    def build(self):
        teaserpp_source_dir = os.path.join(self.source_folder, self.source_subfolder)

        tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeLists.txt"),
            """find_package(Eigen3 3.2 QUIET REQUIRED NO_MODULE)""",
            """include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()

SET(EIGEN3_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_EIGEN}")
MESSAGE(STATUS "Eigen: ${EIGEN3_FOUND} inc: ${EIGEN3_INCLUDE_DIRS}")
SET(PCL_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_PCL}")
SET(PCL_LIBRARY_DIRS "${CONAN_LIB_DIRS_PCL}")
SET(PCL_LIBRARIES "${CONAN_LIBS_PCL}")
MESSAGE(STATUS "PCL: ${CONAN_LIB_DIRS_PCL} inc: ${CONAN_INCLUDE_DIRS_PCL} lib: ${PCL_LIBRARIES}")
find_package(Eigen3 QUIET REQUIRED NO_MODULE)""")

        tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeLists.txt"),
            """find_package(PCL 1.8 QUIET REQUIRED COMPONENTS common io features kdtree)""",
            """find_package(PCL QUIET REQUIRED COMPONENTS common io features kdtree)""")

        cmake = CMake(self)

        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_WITH_MARCH_NATIVE"] = False
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = False
        cmake.definitions["BUILD_TEASER_FPFH"] = False

        cmake.configure(source_folder="source_subfolder", build_folder="build_subfolder")
        cmake.build()
        cmake.install()

    def package(self):

        #self.copy(pattern="*", src="bin", dst="./bin")
        self.copy(pattern="*.a", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.so", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=self.build_subfolder, keep_path=False)


    def package_info(self):
        libs = tools.collect_libs(self)
        self.cpp_info.libs = libs
        # self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
