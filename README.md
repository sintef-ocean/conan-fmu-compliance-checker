[![Linux GCC](https://github.com/sintef-ocean/conan-fmu-compliance-checker/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-fmu-compliance-checker/actions?query=workflow%3A"Linux+GCC")
[![Windows MSVC](https://github.com/sintef-ocean/conan-fmu-compliance-checker/workflows/Windows%20MSVC/badge.svg)](https://github.com/sintef-ocean/conan-fmu-compliance-checker/actions?query=workflow%3A"Windows+MSVC")

[Conan.io](https://conan.io) recipe for [Modelica tools' FMUComplianceChecker](https://github.com/modelica-tools/FMUComplianceChecker).

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:
   ```
   [options]
   eprosima-fmu-compliance-checker:with_tools=True

   [tool_requires]
   cmake/[>=3.25.0]
   fmu-compliance-checker/2.0.4@sintef/stable
   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv

   ```

   A command line tool `fmuCheck.linux64` or `fmuCheck.win64` is available to check FMUs when virtual environment is active.
   There is also a convenience executable target `FMUComplianceChecker::executable` for CMake users that can be used,
   as well as `add_fmu_compliance_check(testName fmuPath)`, which adds an `add_test()` using the executable target.
   ```
   find_package(FMUComplianceChecker REQUIRED CONFIG)
   add_fmu_compliance_check("MyFMU_is_compliant" ${PATH_TO_FMU})
   ```

## Package options

| Option | Allowed values | Default |
|--------|----------------|---------|
| fPIC   | [True, False]  | True    |

To build and run tests, set `tools.build:skip_test=False` in `global.conf`, in `[conf]` or
`--conf` as part of `conan install`.

## Known recipe issues
