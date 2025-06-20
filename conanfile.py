from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps
from conan.tools.build import check_min_cppstd

class MyCaffeRecipe(ConanFile):
    name = "pycaffe"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    requires = [
        "boost/1.81.0",
        "protobuf/3.20.3",
        "zlib/1.3.1",
        "bzip2/1.0.8",
        "openblas/0.3.17"
    ]
    default_options = {
        "boost/*:without_python": True,
        "boost/*:shared": False,
        "protobuf/*:shared": False,
        "openblas/*:shared": False
    }

    def layout(self):
        self.folders.build = "build"
        self.folders.source = "src"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_BUILD_TYPE"] = self.settings.build_type
        tc.cache_variables["CMAKE_POLICY_VERSION_MINIMUM"] = "3.5"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.22]")

    def validate(self):
        check_min_cppstd(self, 14)
