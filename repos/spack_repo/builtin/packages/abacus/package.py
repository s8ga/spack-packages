# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import re

from spack_repo.builtin.build_systems import cmake, makefile
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Abacus(CMakePackage, CudaPackage, MakefilePackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    homepage = "https://abacus.deepmodeling.com/"
    url = "https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.27.tar.gz"
    git = "https://github.com/deepmodeling/abacus-develop.git"

    maintainers("bitllion", "s8ga")

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    # Version 3.10.1 is an "LTS" release that predates 3.9.0.19. Unfortunately,
    # the LTS branch is now less robust than development branch due to lack of
    # backport mechanism, so 3.9.0.27 is currently choosen as preferred.
    version("3.10.1", sha256="06873eba8a4e0bc085177a6580455b28e4b62ea8a18f8afe71a02105756d91a0")
    version(
        "3.10.0",
        sha256="332ed08bb18489f50dcaacdcca8f6ee7ff68e485d49585a2eb9797547898021b",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/LTSv3.10.0.tar.gz",
    )
    version(
        "3.9.0.27",
        sha256="066128d48517373b7b6d4d841f6bf2d8ceff94ae8c175ab089ff482b40789008",
        preferred=True,
    )
    version(
        "3.9.0.25",
        sha256="020f325030d1091596d1dce96f359e80a196266f2266b7b9cbcb1e5b49e957fd",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.25.tar.gz",
    )
    version(
        "3.9.0.20",
        sha256="0e7ad0328ae7d56ef04aa6c7e7f036d4dbc0b764177ea9fbc023bb581ba821aa",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.20.tar.gz",
    )
    version("3.9.0.19", sha256="c985af3d8ac6edb5767b7a094ac2fd2e0ea70b46cf353cd5a4b60096b289939d")
    version(
        "3.9.0.15",
        sha256="34b19c27d85b51b3591b6a150add78ba997568383ddb41b49c8dc45f7e113529",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.15.tar.gz",
    )
    version(
        "3.9.0.10",
        sha256="a8ab692bdb7a17bebacdeb96691a42cfaf3cb363112cd0b9d07a786d4f1cb4e2",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.10.tar.gz",
    )
    version(
        "2.2.3",
        sha256="88dbf6a3bdd907df3e097637ec8e51fde13e2f5e0b44f3667443195481320edf",
        deprecated=True,
    )
    version(
        "2.2.2",
        sha256="4a7cf2ec6e43dd5c53d5f877a941367074f4714d93c1977a719782957916169e",
        deprecated=True,
    )
    version(
        "2.2.1",
        sha256="14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f",
        deprecated=True,
    )

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("lcao", default=True, description="Enable LCAO algorithm")
    variant("elpa", default=True, description="Enable ELPA support", when="+mpi")
    variant("libxc", default=True, description="Enable LibXC support")
    variant("libri", default=False, description="Enable LibRI support", when="@3: +mpi +lcao")
    variant("dftd4", default=False, description="Enable DFT-D4 support", when="@3.11:")
    variant("pexsi", default=False, description="Enable PEXSI support", when="+mpi +lcao")
    variant("json", default=False, description="Enable JSON output support", when="@3.11:")

    # DeePKS / ML: the option was renamed between release lines -- LTS 3.10.x
    # uses ENABLE_DEEPKS, the 3.9.0.x develop line uses ENABLE_MLALGO (DeePKS
    # + ML-KEDF). Disjoint version gates; requesting the absent variant on a
    # given version errors ("variant not found").
    variant(
        "deepks",
        default=False,
        when="@3.10",
        description="DeePKS (maps to ENABLE_DEEPKS, LTS line)",
    )
    variant(
        "mlalgo",
        default=False,
        when="@3.9.0.10:3.9.0.27",
        description="ML algorithms: DeePKS + ML-KEDF (maps to ENABLE_MLALGO, develop line)",
    )
    # NEP landed on the develop line in 3.9.0.27 (3.10.x LTS never gained
    # FindNEP, so it is excluded).
    variant(
        "nep",
        default=False,
        when="@3.9.0.27",
        description="Enable NEP neuroevolution potential (FindNEP.cmake)",
    )
    variant("deepmd", default=False, description="Enable DeePMD-kit (Deep Potential MD)")
    variant("rapidjson", default=False, description="Enable RapidJSON usage")

    # GPU acceleration: +cuda / cuda_arch are inherited from CudaPackage.
    variant(
        "cuda-mpi",
        default=False,
        when="+cuda",
        description="Enable CUDA-aware MPI (USE_CUDA_MPI)",
    )
    variant(
        "nccl",
        default=False,
        when="+cuda",
        description="Enable NCCL-backed multi-GPU collectives (ENABLE_NCCL_PARALLEL_DEVICE)",
    )
    variant(
        "cusolvermp",
        default=False,
        when="+cuda",
        description="Enable cuSOLVERMp distributed GPU solver",
    )
    variant(
        "cublasmp",
        default=False,
        when="+cusolvermp",
        description="Enable cuBLASMp distributed GPU BLAS (requires +cusolvermp)",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("fftw precision=float,double +openmp", when="+openmp")
    depends_on("fftw precision=float,double ~openmp", when="~openmp")
    depends_on("elpa +mpi +openmp", when="+elpa +openmp")
    depends_on("elpa +mpi ~openmp", when="+elpa ~openmp")
    # Bidirectional CUDA constraint (cp2k pattern) so cuda_arch propagates
    # cleanly to the solver instead of leaving elpa at cuda_arch=none.
    depends_on("elpa+cuda", when="+elpa+cuda")
    depends_on("elpa~cuda", when="+elpa~cuda")
    depends_on("libxc@5.1.7:", when="+libxc")
    # Force the CMake build of dftd4: the meson build (dftd4's default)
    # installs no CMake package config, which ABACUS's find_package(dftd4)
    # needs.
    depends_on("dftd4@4.2: build_system=cmake", when="+dftd4")
    depends_on("libri", when="+libri")
    depends_on("libcomm", when="+libri")
    # Older releases require Cereal for LCAO builds
    # Current versions use it only with LibRI
    depends_on("cereal", when="@:2")
    depends_on("cereal", when="@3:3.10 +lcao")
    depends_on("cereal", when="@3.11: +libri")
    # Force the CMake build of PEXSI: only PEXSI installs ship the
    # PEXSIConfig.cmake that ABACUS's find_package(PEXSI) requires.
    depends_on("pexsi@2.0: build_system=cmake", when="+pexsi")
    depends_on("nlohmann-json@3.12:", when="+json")

    # ML: libtorch via py-torch + the libnpy header (libnpy_INCLUDE_DIR
    # avoids an ABACUS FetchContent download at build time).
    #
    # Upper bound 2.4: ABACUS uses the torch::linalg C++ namespace, removed
    # in pytorch 2.5 (functions moved to the torch::linalg_* prefix), so
    # every ABACUS version requires py-torch <= 2.4. spack-packages
    # deprecates py-torch@:2.9 wholesale, so +deepks/+mlalgo need
    # `spack install --deprecated`.
    depends_on("py-torch@2.1:2.4 ~cuda", when="+deepks")
    depends_on("py-torch@2.1:2.4 ~cuda", when="+mlalgo")
    conflicts(
        "^cuda@13:",
        when="+deepks +cuda",
        msg="py-torch 2.1:2.4 cannot build against CUDA 13; use CUDA 12.x.",
    )
    conflicts(
        "^cuda@13:",
        when="+mlalgo +cuda",
        msg="py-torch 2.1:2.4 cannot build against CUDA 13; use CUDA 12.x.",
    )
    depends_on("libnpy", when="+deepks")
    depends_on("libnpy", when="+mlalgo")

    # NEP (FindNEP expects <prefix>/{include,lib})
    depends_on("nep-cpu", when="+nep")
    depends_on("deepmdkit", when="+deepmd")
    depends_on("rapidjson", when="+rapidjson")

    # GPU acceleration. cuda_arch is sticky and does not propagate across
    # dependency edges (nccl conflicts on cuda_arch=none), so per-arch edges
    # are enumerated explicitly.
    depends_on("cuda", when="+cuda")
    depends_on("nccl+cuda", when="+nccl")
    depends_on("cusolvermp+cuda", when="+cusolvermp")
    depends_on("cublasmp+cuda", when="+cublasmp")
    for _arch in CudaPackage.cuda_arch_values:
        with when(f"cuda_arch={_arch}"):
            depends_on(f"nccl cuda_arch={_arch}", when="+nccl")
            depends_on(f"cusolvermp cuda_arch={_arch}", when="+cusolvermp")
            depends_on(f"cublasmp cuda_arch={_arch}", when="+cublasmp")
    # +cuda-mpi needs an MPI built with CUDA support; "mpi+cuda" cannot be
    # required directly because it would demand +cuda of every provider.
    requires(
        "^openmpi+cuda",
        "^mpich+cuda",
        when="+cuda-mpi",
        policy="one_of",
        msg="+cuda-mpi requires an MPI implementation built with CUDA support "
        "(openmpi+cuda or mpich+cuda).",
    )
    depends_on("openblas", when="build_system=cmake")
    depends_on("scalapack", when="+mpi build_system=cmake")
    depends_on("mkl", when="build_system=makefile")
    depends_on("cmake@3.16:", type="build", when="build_system=cmake")

    build_system(conditional("cmake", when="@3:"), "makefile", default="cmake")

    # LTS 3.10.x +pexsi compile fix (missing include + Gint signature).
    patch("lts-pexsi-compile.patch", when="@3.10 +pexsi")
    # LTS CUDA 13 compatibility: cherry-pick of upstream PR #6772 + #6813.
    # The v3.10.x tags predate these fixes: CMakeLists.txt needs
    # find_package(CUDAToolkit) before the version check + C++17 for CUDA 13
    # (CCCL/Thrust requires it); source files (device.cpp, global.h,
    # helper_cuda.h) have CUDA 13 API fixes.
    patch("lts-cuda13-fix.patch", when="@3.10 +cuda")
    # v3.9.0.10 compile fix: uint64_t used without #include <cstdint>
    # (fixed in later develop versions).
    patch("v3.9.0.10-cstdint.patch", when="@3.9.0.10")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("GIT_SUBMODULE", False),
            self.define("ENABLE_FLOAT_FFTW", True),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_LCAO", "lcao"),
            self.define_from_variant("ENABLE_PEXSI", "pexsi"),
            self.define_from_variant("ENABLE_LIBXC", "libxc"),
            self.define_from_variant("ENABLE_LIBRI", "libri"),
            self.define_from_variant("ENABLE_RAPIDJSON", "rapidjson"),
        ]

        if spec.satisfies("@3.11:"):
            args += [
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("ENABLE_ELPA", "elpa"),
                self.define_from_variant("ENABLE_DFTD4", "dftd4"),
                self.define_from_variant("ENABLE_JSON", "json"),
            ]

        if spec.satisfies("+libri"):
            args += [
                self.define("LIBRI_DIR", spec["libri"].prefix),
                self.define("LIBCOMM_DIR", spec["libcomm"].prefix),
            ]

        if spec.satisfies("@:3.10"):
            args += [
                self.define_from_variant("USE_OPENMP", "openmp"),
                self.define_from_variant("USE_ELPA", "elpa"),
            ]

        if spec.satisfies("@3.10"):
            args.append(self.define_from_variant("ENABLE_DEEPKS", "deepks"))
            # LTS still has ENABLE_PAW but requires libpaw_interface (no
            # spack package). Force OFF -- PAW is not supported in this build.
            args.append(self.define("ENABLE_PAW", False))

        if spec.satisfies("@3.9.0.10:3.9.0.27"):
            args.append(self.define_from_variant("ENABLE_MLALGO", "mlalgo"))
            # USE_SW exists @3.9.0.10: but x86 does not need Sunway.
            args.append(self.define("USE_SW", False))

        # ML: libtorch + libnpy for +deepks (LTS) / +mlalgo (develop line)
        if "+deepks" in spec or "+mlalgo" in spec:
            self._add_torch_args(args, spec)
            args.append(self.define("libnpy_INCLUDE_DIR", spec["libnpy"].prefix.include))

        # NEP was introduced on the develop line @3.9.0.27
        if "+nep" in spec:
            args.append(self.define("NEP_DIR", spec["nep-cpu"].prefix))

        # DeePMD is variable-driven (a defined DeePMD_DIR enables it)
        if "+deepmd" in spec:
            args.append(self.define("DeePMD_DIR", spec["deepmdkit"].prefix))

        # GPU acceleration: ABACUS uses CMAKE_CUDA_ARCHITECTURES (CMake 3.18+
        # native); CudaPackage provides the multi-valued cuda_arch variant.
        if "+cuda" in spec:
            args.append(self.define_from_variant("USE_CUDA", "cuda"))
            args.append(self.define_from_variant("USE_CUDA_MPI", "cuda-mpi"))
            args.append(self.define_from_variant("ENABLE_NCCL_PARALLEL_DEVICE", "nccl"))
            args.append(self.define("ENABLE_CUSOLVERMP", "+cusolvermp" in spec))
            args.append(self.define("ENABLE_CUBLASMP", "+cublasmp" in spec))
            if spec.satisfies("^cuda@12.8:"):
                args.append("-DCMAKE_CUDA_FLAGS=-static-global-template-stub=false")
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch[0] != "none":
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", ";".join(cuda_arch)))
        return args

    def _add_torch_args(self, args, spec):
        """Locate TorchConfig.cmake under py-torch.

        py-torch buries TorchConfig.cmake in its python site-packages tree
        (confirmed empirically and corroborated by cp2k's cmake_cp2k.sh:
        "PyTorch's TorchConfig.cmake is buried in the Python site-packages
        directory"). The python version in the path is dynamic, so the
        directory is glob-discovered rather than hard-coded.
        """
        torch = spec["py-torch"]
        pattern = join_path(
            str(torch.prefix),
            "lib",
            "python*",
            "site-packages",
            "torch",
            "share",
            "cmake",
            "Torch",
        )
        matches = glob.glob(pattern)
        if not matches:
            raise InstallError(
                "TorchConfig.cmake not found under py-torch prefix. Expected pattern: {0}".format(
                    pattern
                )
            )
        args.append(self.define("Torch_DIR", matches[0]))


class MakefileBuilder(makefile.MakefileBuilder):
    @property
    def build_directory(self):
        return join_path(self.stage.source_path, "source")

    def edit(self, pkg, spec, prefix):
        if spec.satisfies("+openmp"):
            inc_var = "_openmp-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl,-rpath=${ELPA_LIB_DIR}"
        else:
            inc_var = "-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}"

        tempInc = f"""
FORTRAN = ifort
CPLUSPLUS = icpc
CPLUSPLUS_MPI = mpiicpc
LAPACK_DIR = $(MKLROOT)
FFTW_DIR = {spec["fftw"].prefix}
ELPA_DIR = {spec["elpa"].prefix}
ELPA_INCLUDE = -I${{ELPA_DIR}}/include/elpa{inc_var}{spec["elpa"].version}
CEREAL_DIR = {spec["cereal"].prefix}
OBJ_DIR = obj
OBJ_DIR_serial = obj
NP      = 14
"""

        with open(join_path(self.build_directory, "Makefile.vars"), "w") as f:
            f.write(tempInc)

        lineList = []
        Pattern1 = re.compile("^ELPA_INCLUDE_DIR")
        Pattern2 = re.compile("^ELPA_LIB\\s*= ")
        with open(join_path(self.build_directory, "Makefile.system"), "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif Pattern1.search(line) or Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(join_path(self.build_directory, "Makefile.system"), "w") as f:
            f.writelines(lineList)

        with open(join_path(self.build_directory, "Makefile.system"), "a") as f:
            f.write(system_var)

    def install(self, pkg, spec, prefix):
        install_tree("bin", prefix.bin)
