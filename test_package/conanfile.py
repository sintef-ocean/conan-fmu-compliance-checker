from os import path
from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import cmake_layout, CMake, CMakeDeps

class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"
    test_type = "explicit"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tested_name = str(self.tested_reference_str).split("/")[0]
        deps = CMakeDeps(self)
        deps.build_context_activated = [tested_name]
        deps.build_context_build_modules = [tested_name]
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()


    def test(self):
        if can_run(self):
            f = open(path.join(self.build_folder, "fmuchk"), "r")
            exe_name = f.readline()
            f.close()
            self.run(exe_name)
