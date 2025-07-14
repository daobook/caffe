from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps

class CaffeRecipe(ConanFile):
    name = "pycaffe"
    version = "0.0.1"
    package_type = "library"

    # 可选元数据
    license = "LICENSE"
    author = "xinetzone (735613050@qq.com)"
    # homepage = "https://caffe.berkeleyvision.org/"
    url = "https://github.com/daobook/caffe.git"
    description = "Caffe: a fast open framework for deep learning."
    topics = ('daobook', 'caffe')

    # 用于主机环境中常规依赖项（如库）的字符串列表或元组。
    requires = [
        "boost/[>1.80]",
        "protobuf/[>3.17]",
        "zlib/[>=1.2.11 <2]",
        "glog/[>=0.7.1]",
        "gflags/[>=2.2.2]",
    ]

    # 二进制配置
    settings = "os", "compiler", "build_type", "arch"
    conf = "tools.cmake.cmaketoolchain:generator=Ninja"

    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    # 源文件与本 recipe 位于同一位置，请将它们复制到 recipe 中。
    exports_sources = (
        "CMakeLists.txt", "src/*", "include/*", 
        "cmake/*", "python/*"
    )

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)
    
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    # def package_info(self):
    #     self.cpp_info.libs = ["hello"]