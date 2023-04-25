from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, collect_libs, get
import os


class TeaserPPConan(ConanFile):
    version = "2.0"

    name = "teaserplusplus"
    license = "https://github.com/IntelVCL/Open3D/raw/master/LICENSE"
    description = "TEASER++ is a fast and certifiably-robust point cloud registration library written in C++, with Python and MATLAB bindings."
    url = "https://github.com/MIT-SPARK/TEASER-plusplus"

    settings = "os", "compiler", "build_type", "arch"

    requires = (
        "eigen/3.4.0",
        "boost/1.81.0",
        )

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        }

    default_options = {
        "shared": True,
        "fPIC": True,
    }

    def source(self):
        get(self,
            "https://github.com/MIT-SPARK/TEASER-plusplus/archive/refs/tags/v{}.tar.gz".format(self.version),
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["BUILD_TESTS"] = False
        tc.cache_variables["BUILD_WITH_MARCH_NATIVE"] = False
        tc.cache_variables["BUILD_PYTHON_BINDINGS"] = False
        tc.cache_variables["BUILD_TEASER_FPFH"] = False

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)

#
#     def build(self):
#         teaserpp_source_dir = os.path.join(self.source_folder, self.source_subfolder)
#
#         tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeLists.txt"),
#             """find_package(Eigen3 3.2 QUIET REQUIRED NO_MODULE)""",
#             """include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
# conan_basic_setup()
#
# SET(EIGEN3_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_EIGEN}")
# MESSAGE(STATUS "Eigen: ${EIGEN3_FOUND} inc: ${EIGEN3_INCLUDE_DIRS}")
# SET(PCL_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_PCL}")
# SET(PCL_LIBRARY_DIRS "${CONAN_LIB_DIRS_PCL}")
# SET(PCL_LIBRARIES "${CONAN_LIBS_PCL}")
# MESSAGE(STATUS "PCL: ${CONAN_LIB_DIRS_PCL} inc: ${CONAN_INCLUDE_DIRS_PCL} lib: ${PCL_LIBRARIES}")
# find_package(Eigen3 QUIET REQUIRED NO_MODULE)""")
#
#         tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeLists.txt"),
#             """find_package(PCL 1.8 QUIET REQUIRED COMPONENTS common io features kdtree)""",
#             """find_package(PCL QUIET REQUIRED COMPONENTS common io features kdtree)""")
#

