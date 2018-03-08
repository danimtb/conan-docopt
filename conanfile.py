from conans import ConanFile, CMake, tools
import os

class DocoptConan(ConanFile):
    name = "docopt"
    version = "0.6.2"
    description = "docopt helps you create most beautiful command-line interfaces easily"
    license = "MIT and Boost"
    url = "https://github.com/conan-community/conan-docopt"
    homepage = "https://github.com/docopt/docopt.cpp"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        tools.get("%s/archive/v%s.zip" % (self.homepage, self.version))
        os.rename("docopt.cpp-%s" % self.version, "sources")
        tools.replace_in_file("sources/CMakeLists.txt", "include(GNUInstallDirs)", """include(GNUInstallDirs)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="sources")
        cmake.build()

    def package(self):
        self.copy("docopt.h", "include", "sources")
        self.copy("docopt_value.h", "include", "sources")
        self.copy("docopt_util.h", "include", "sources")
        self.copy("*docopt*.a", "lib", keep_path=False)
        self.copy("*docopt*.dll", "bin", keep_path=False)
        if self.options.shared:
            self.copy("*docopt.lib", "lib", keep_path=False)
            self.copy("*docopt*.so", "lib", keep_path=False)
            self.copy("*docopt*.dylib", "lib", keep_path=False)
        else:
            self.copy("*docopt_s.lib", "lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if "objects" in self.cpp_info.libs:
            self.cpp_info.libs.remove("objects")
