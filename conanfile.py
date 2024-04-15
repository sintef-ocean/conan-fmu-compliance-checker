from os import path
import posixpath
from conan import ConanFile, conan_version
from conan.tools.microsoft import is_msvc_static_runtime, is_msvc
from conan.tools.files import (
    apply_conandata_patches, export_conandata_patches, get, copy, save, rename)
from conan.tools.scm import Version
from conan.tools.env import Environment
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

required_conan_version = ">=2.0"


class PackageConan(ConanFile):
    name = "fmu-compliance-checker"
    description = "short description"
    license = "BSD-3-Clause"
    url = "https://github.com/sintef-ocean/conan-fmu-compliance-checker"
    homepage = "https://github.com/modelica-tools/FMUComplianceChecker"
    topics = ("fmi", "fmi-standard", "compliance")
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "fmuchk.cmake", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["fmilib/*"].with_fmus = True
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("fmi1/1.0.1")
        self.requires("fmi2/2.0.4")
        self.requires("fmilib/2.4.1@sintef/stable")
        #self.requires("fmilib/2.4.1") # Pending fmilib on conan center index

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if is_msvc(self):
            tc.variables["FMUCHK_BUILD_WITH_STATIC_RTLIB"] = is_msvc_static_runtime(self)

        copy(self, "*.h", self.dependencies["fmi1"].cpp_info.components["cosim"].includedirs[0],
             path.join(self.build_folder, "fmis", "FMI1"))
        copy(self, "*.h", self.dependencies["fmi2"].cpp_info.includedirs[0],
             path.join(self.build_folder, "fmis", "FMI2"))
        copy(self, "*.fmu", self.dependencies["fmilib"].cpp_info.resdirs[0],
             path.join(self.build_folder, "fmus"), keep_path=False)

        tc.variables["FMUCHK_INSTALL_PREFIX"] = posixpath.join(self.build_folder, "install").replace("\\", "/")
        tc.variables["FMUCHK_FMI_STANDARD_HEADERS"] = posixpath.join(self.build_folder, "fmis").replace("\\", "/")
        tc.variables["FMUCHK_FMIL"] = str(self.build_folder).replace("\\", "/")

        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if not self.conf.get("tools.build:skip_test", default=True):
            env = Environment()
            env.define("CTEST_OUTPUT_ON_FAILURE", "ON")
            with env.vars(self).apply():
                cmake.test()

        cmake.install()  # It installs to build folder

    def package(self):
        copy(self, pattern="LICENSE", dst=path.join(self.package_folder, "licenses"),
             src=self.source_folder)

        copy(self, pattern="*", dst=path.join(self.package_folder, "bin"),
             src=path.join(self.build_folder, "install"), keep_path=False)

        # This removes a lint hook error
        save(self, path.join(self.package_folder, "bin", "fmuCheckExecutable"),
             "The executable is named fmuCheck.{os}{arch}")

        copy(self, "fmuchk.cmake", self.export_sources_folder,
             path.join(self.package_folder, "res"))

    def package_info(self):
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = ["res"]
        self.cpp_info.includedirs = []
        self.cpp_info.builddirs = ["res"]

        self.cpp_info.set_property("cmake_build_modules",
                                   [path.join("res", "fmuchk.cmake")])

        self.cpp_info.set_property("cmake_file_name", "FMUComplianceChecker")
