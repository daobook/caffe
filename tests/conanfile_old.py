from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.build import check_min_cppstd
import os

class CaffeConan(ConanFile):
    name = "caffe_project"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    requires = [
        "openblas/0.3.25",
        "boost/1.81.0",
        "protobuf/3.21.12",
        "zlib/1.3.1",
        "bzip2/1.0.8",
        "glog/0.7.1",
        "gflags/2.2.2",
    ]
    default_options = {
        "boost:shared": False,
        "boost:without_python": True,
        "openblas:shared": False,
        "protobuf:shared": False
    }

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.22]")

    def layout(self):
        self.folders.source = "src"
        self.folders.build = "build"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_BUILD_TYPE"] = self.settings.build_type
        tc.cache_variables["CMAKE_POLICY_VERSION_MINIMUM"] = "3.5"
        # 限制构建线程数，稳定 openblas 构建
        tc.cache_variables["CMAKE_BUILD_PARALLEL_LEVEL"] = "2"
        tc.generate()
        CMakeDeps(self).generate()

    def validate(self):
        check_min_cppstd(self, 14)

    def build(self):
        # 显式指定并发度（与 CMAKE_BUILD_PARALLEL_LEVEL 一致）
        cmake = CMake(self)
        cmake.configure()
        cmake.build(args=["-j2"])
