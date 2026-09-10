# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import re

from spack_repo.builtin.build_systems import makefile
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Abacus(CMakePackage, CudaPackage, MakefilePackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles

    Version support policy (TEMPORARY): the moving develop branch is
    intentionally NOT packaged here -- it has diverged from the 3.9.0.x
    line (PEXSI CMake config switch, LibComm auto-discovery, ...) and
    tracking a moving target breaks reproducibility. The develop line is
    capped at v3.9.0.27; support returns when the next line (3.11.x)
    stabilizes. LTS 3.10.x is unaffected.

    NOTE for +deepks/+mlalgo: ABACUS uses the torch::linalg C++ namespace,
    removed in pytorch 2.5, so these variants need py-torch@2.1:2.4 --
    versions that spack-packages marks deprecated. Install with
    `spack install --deprecated` until ABACUS migrates to the
    torch::linalg_* namespace."""

    homepage = "http://abacus.ustc.edu.cn/"
    url = "https://github.com/abacusmodeling/abacus-develop/archive/refs/tags/v3.9.0.19.tar.gz"
    git = "https://github.com/abacusmodeling/abacus-develop.git"

    # bitllion is the current maintainer of this recipe; to be re-added
    # (with consent) when the big PR is finalized.
    maintainers("s8ga")

    license("LGPL-3.0-or-later")

    # NOTE: no "develop" branch version on purpose -- see the version support
    # policy in the class docstring. Highest supported develop-line release:
    # 3.9.0.27. LTS 3.10.x is unaffected. Revisit when 3.11.x stabilizes.
    version("3.10.1", sha256="06873eba8a4e0bc085177a6580455b28e4b62ea8a18f8afe71a02105756d91a0")
    version(
        "3.10.0",
        sha256="332ed08bb18489f50dcaacdcca8f6ee7ff68e485d49585a2eb9797547898021b",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/LTSv3.10.0.tar.gz",
    )
    version(
        "3.9.0.27",
        sha256="066128d48517373b7b6d4d841f6bf2d8ceff94ae8c175ab089ff482b40789008",
        url="https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v3.9.0.27.tar.gz",
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

    variant("openmp", default=True, description="Enable OpenMP support")
    variant("lcao", default=True, description="Enable LCAO algorithm")
    variant("elpa", default=True, description="Enable ELPA support")
    variant("libxc", default=True, description="Enable LibXC support")

    # Core build options (all versions).
    # NOTE: there is deliberately no "mpi" variant: ABACUS is an MPI code and
    # serial builds are not supported upstream, so MPI is an unconditional
    # dependency (see depends_on("mpi") below).
    variant(
        "float-fftw",
        default=True,
        description="Enable single-precision FFTW backend (matches official CI default)",
    )
    variant(
        "native-optimization",
        default=False,
        description="Enable host-native CPU optimizations (-march=native)",
    )
    variant(
        "debug",
        default=False,
        description="Enable developer debug messages (DEBUG_INFO)",
    )
    variant(
        "mathlib",
        default=False,
        description="Build ABACUS libmath from source (USE_ABACUS_LIBM, "
        "only useful for old compilers lacking optimized libm)",
    )

    # Variants gated on LCAO (forced OFF by CMake otherwise)
    variant(
        "pexsi",
        default=False,
        when="+lcao",
        description="Enable PEXSI for large-scale electronic structure (requires LCAO)",
    )

    # Optional scientific libraries (all versions)
    variant("libri", default=False, description="Enable EXX with LibRI")
    variant("rapidjson", default=False, description="Enable RapidJSON usage")
    variant("deepmd", default=False, description="Enable DeePMD-kit (Deep Potential MD)")

    # ML: follow upstream option names exactly.
    #   LTS (3.10.x) uses ENABLE_DEEPKS
    #   develop line @3.9.0.8: uses ENABLE_MLALGO (unified DeePKS + ML-KEDF)
    # `mlalgo` covers the 3.9.0.x develop line (up to the 3.9.0.27 cap, see
    # docstring) while excluding LTS 3.10.x. Requesting the absent variant on
    # a given version auto-errors (spack: "variant not found").
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
        description="ML algorithms: DeePKS + ML-KEDF (maps to ENABLE_MLALGO, develop)",
    )

    # New features on the develop line (version-gated to their introduction).
    # NEP lands in 3.9.0.27 (develop-line cap) : 3.10.x LTS never gained
    # FindNEP, so it is excluded.
    variant(
        "nep",
        default=False,
        when="@3.9.0.27",
        description="Enable NEP neuroevolution potential (FindNEP.cmake)",
    )

    # GPU acceleration. +cuda and cuda_arch are inherited from CudaPackage.
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

    # MPI is unconditional: serial (~MPI) builds are not supported by ABACUS.
    # The deprecated 2.2.x makefile build is serial-only and likewise not
    # supported; those versions carry deprecated=True and are kept for
    # reproducibility of old environments only.
    depends_on("mpi")

    # FFTW: the CMake line uses the fftw-api virtual (MKL can provide it);
    # the deprecated 2.2.x makefile build keeps the direct dependency its
    # MakefileBuilder expects (spec["fftw"]).
    depends_on("fftw-api@3", when="build_system=cmake")
    depends_on("fftw+openmp", when="+openmp ^[virtuals=fftw-api] fftw")
    depends_on("fftw~openmp", when="~openmp ^[virtuals=fftw-api] fftw")
    # Single-precision FFTW: ENABLE_FLOAT_FFTW links FFTW3::FFTW3_FLOAT
    # (CMake line only; the 2.2.x makefile build links double-precision FFTW).
    depends_on(
        "fftw precision=float",
        when="+float-fftw build_system=cmake ^[virtuals=fftw-api] fftw",
    )
    depends_on("fftw+openmp", when="+openmp build_system=makefile")
    depends_on("fftw~openmp", when="~openmp build_system=makefile")

    # BLAS/LAPACK split between the two build systems: OpenBLAS on the CMake
    # line, MKL on the deprecated 2.2.x makefile one.
    depends_on("openblas", when="build_system=cmake")
    depends_on("mkl", when="build_system=makefile")
    depends_on("scalapack", when="+lcao")

    # LCAO dependencies
    depends_on("cereal")
    # ELPA: bidirectional cuda constraint (cp2k pattern) so cuda_arch
    # propagates cleanly via sticky + unify. Without this, the solver can
    # leave elpa at cuda_arch=none even when abacus has cuda_arch set.
    depends_on("elpa~cuda", when="+elpa~cuda")
    depends_on("elpa+cuda", when="+elpa+cuda")
    # Reverse propagation: build elpa ~openmp when ABACUS is ~openmp
    depends_on("elpa~openmp", when="~openmp+elpa")
    # Recent develop FindELPA.cmake uses pkg-config to locate ELPA
    depends_on("pkgconfig", type="build", when="+elpa")

    # Optional libraries
    depends_on("libxc", when="+libxc")
    depends_on("libri", when="+libri")
    depends_on("libcomm", when="+libri")
    # Force the CMake build: the makefile build of pexsi does not install a
    # PEXSIConfig.cmake, which ABACUS's find_package(PEXSI) requires.
    depends_on("pexsi build_system=cmake", when="+pexsi")
    depends_on("rapidjson", when="+rapidjson")
    depends_on("deepmdkit", when="+deepmd")

    # ML: libtorch via py-torch + libnpy header (libnpy_INCLUDE_DIR avoids
    # ABACUS FetchContent download at build time).
    #
    # Upper bound 2.4: ABACUS uses the torch::linalg C++ namespace, which was
    # removed in pytorch 2.5 (2024-10; functions moved to torch::linalg_*
    # prefix). develop HEAD is mid-migration but still uses the old namespace,
    # so every ABACUS version (LTS + develop) requires py-torch <= 2.4.
    # spack-packages deprecates py-torch@:2.9 wholesale, so +deepks/+mlalgo
    # need `spack install --deprecated` (see also the docstring note).
    depends_on("py-torch@2.1:2.4 ~cuda", when="+deepks")
    depends_on("py-torch@2.1:2.4 ~cuda", when="+mlalgo")
    depends_on("libnpy", when="+deepks")
    depends_on("libnpy", when="+mlalgo")
    # torch 2.1-2.4 predate CUDA 13 (2025-08): py_torch's cuda ladder leaves
    # @11: open, but a source build of torch 2.4 against CUDA 13 fails on the
    # same CCCL/C++17 removals that the LTS cuda13 patch fixes for ABACUS.
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

    # NEP (self-built nep-cpu package; FindNEP expects <prefix>/{include,lib})
    depends_on("nep-cpu", when="+nep")

    # GPU acceleration.
    # ABACUS uses find_package(CUDAToolkit REQUIRED) + enable_language(CUDA).
    depends_on("cuda", when="+cuda")
    # nccl/cusolvermp/cublasmp: force +cuda so the toolkit unifies, and
    # propagate cuda_arch explicitly (sticky variants do not traverse
    # dependency edges; nccl conflicts on cuda_arch=none). Enumerated
    # per-arch edges mirror what cusolvermp/cublasmp do internally.
    depends_on("nccl+cuda", when="+nccl")
    depends_on("cusolvermp+cuda", when="+cusolvermp")
    depends_on("cublasmp+cuda", when="+cublasmp")
    for _arch in CudaPackage.cuda_arch_values:
        with when(f"cuda_arch={_arch}"):
            depends_on(f"nccl cuda_arch={_arch}", when="+nccl")
            depends_on(f"cusolvermp cuda_arch={_arch}", when="+cusolvermp")
            depends_on(f"cublasmp cuda_arch={_arch}", when="+cublasmp")
    # CUDA-aware MPI: the MPI implementation must be built with CUDA
    # support. `depends_on("mpi+cuda")` would be unsatisfiable: the virtual
    # would require EVERY provider to have a +cuda variant, but providers
    # disagree on accelerator handling (openmpi: +cuda; mpich/mvapich2:
    # none). Restrict to the providers that can express it (abinit's
    # gpu_aware_mpi pattern).
    requires(
        "^openmpi+cuda",
        "^mpich+cuda",
        when="+cuda-mpi",
        policy="one_of",
        msg="+cuda-mpi requires an MPI implementation built with CUDA support "
        "(openmpi+cuda or mpich+cuda).",
    )

    depends_on("cmake", type="build", when="build_system=cmake")

    build_system(conditional("cmake", when="@3.0.0:"), "makefile", default="cmake")

    # ------------------------------------------------------------------ #
    #  Conflicts                                                         #
    # ------------------------------------------------------------------ #

    # GNU+MKL is unsupported on LTS and on develop <3.9.0.25: FindMKL only
    # locates Intel Fortran interfaces there, so %gcc linking fails.
    conflicts(
        "%gcc ^intel-oneapi-mkl",
        when="@3.10",
        msg="LTS MKL only provides Intel Fortran interfaces. "
        "Use %intel-oneapi-compilers with intel-oneapi-mkl, or pick a "
        "non-MKL BLAS/FFTW provider (e.g. openblas + fftw).",
    )
    conflicts(
        "%gcc ^intel-oneapi-mkl",
        when="@:3.9.0.24",
        msg="develop <3.9.0.25: GNU+MKL not supported (same as LTS).",
    )

    # cuBLASMp requires cuSOLVERMp (enforced by CMake, conflict for clarity)
    conflicts("+cublasmp", when="~cusolvermp", msg="cuBLASMp requires +cusolvermp")

    # ------------------------------------------------------------------ #
    #  Patches                                                           #
    # ------------------------------------------------------------------ #

    # LTS PEXSI compile fix: upstream bug (missing #include + Gint_inout
    # signature mismatch) fixed in PR #6689 on develop, but not cherry-picked
    # to the LTS branch. See issue #6684.
    patch("lts-pexsi-compile.patch", when="@3.10 +pexsi")

    # LTS CUDA 13 compatibility: cherry-pick of PR #6772 + #6813 from LTS
    # HEAD. The v3.10.x tags predate these fixes: CMakeLists.txt needs
    # find_package(CUDAToolkit) before the version check + C++17 for CUDA 13
    # (CCCL/Thrust requires it). Source files (device.cpp, global.h,
    # helper_cuda.h) have CUDA 13 API fixes.
    patch("lts-cuda13-fix.patch", when="@3.10 +cuda")

    # v3.9.0.10 compile fix: uint64_t used without #include <cstdint>
    # (fixed in later develop versions)
    patch("v3.9.0.10-cstdint.patch", when="@3.9.0.10")

    # ------------------------------------------------------------------ #
    #  CMake arguments                                                   #
    # ------------------------------------------------------------------ #

    def cmake_args(self):
        spec = self.spec
        args = [
            # --- shared variant -> option mapping (all versions) ---
            self.define("ENABLE_MPI", True),
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define_from_variant("ENABLE_LCAO", "lcao"),
            self.define_from_variant("USE_ELPA", "elpa"),
            self.define_from_variant("ENABLE_LIBRI", "libri"),
            self.define_from_variant("ENABLE_LIBXC", "libxc"),
            self.define_from_variant("ENABLE_PEXSI", "pexsi"),
            self.define_from_variant("ENABLE_RAPIDJSON", "rapidjson"),
            self.define_from_variant("ENABLE_FLOAT_FFTW", "float-fftw"),
            self.define_from_variant("ENABLE_NATIVE_OPTIMIZATION", "native-optimization"),
            self.define_from_variant("DEBUG_INFO", "debug"),
            self.define_from_variant("USE_ABACUS_LIBM", "mathlib"),
            # --- GPU acceleration (variant-driven) ---
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_CUDA_MPI", "cuda-mpi"),
            self.define_from_variant("ENABLE_NCCL_PARALLEL_DEVICE", "nccl"),
            self.define("ENABLE_CUSOLVERMP", "+cusolvermp" in spec),
            self.define("ENABLE_CUBLASMP", "+cublasmp" in spec),
            # --- shared force-disabled (not supported) ---
            self.define("USE_ROCM", False),
            self.define("USE_DSP", False),
            self.define("USE_CUDA_ON_DCU", False),
            self.define("GIT_SUBMODULE", False),
        ]

        # FFT backend: MKL (MKLROOT) vs FFTW3 (FFTW3_DIR).
        # FindMKL reads the *CMake variable* ${MKLROOT} (not the env var), so
        # it must be passed explicitly. intel-oneapi-mkl ships MKL under
        # <prefix>/mkl/<version>/{include,lib}; `latest` symlinks the active
        # version and is stable across MKL releases.
        if "^intel-oneapi-mkl" in spec:
            mkl = spec["intel-oneapi-mkl"]
            args.append(self.define("MKLROOT", join_path(mkl.prefix, "mkl", "latest")))
        else:
            args.append(self.define("FFTW3_DIR", spec["fftw-api"].prefix))

        # Cereal: FindCereal expects CEREAL_INCLUDE_DIR = the include dir
        # itself (it searches for cereal/cereal.hpp under it).
        if "+lcao" in spec:
            args.append(self.define("CEREAL_INCLUDE_DIR", spec["cereal"].prefix.include))

        # ELPA: FindELPA uses ELPA_DIR (prefix); it has a built-in #3589
        # guard that rejects /usr/include/elpa system hits when ELPA_DIR is
        # set.
        if "+elpa" in spec:
            args.append(self.define("ELPA_DIR", spec["elpa"].prefix))

        # LibRI / LibComm:
        # - LIBRI_DIR + LIBCOMM_DIR are needed by FindLibRI/FindLibComm in
        #   all versions.
        # - ENABLE_LIBCOMM is deprecated on recent develop (CMake unsets it
        #   with WARNING); LibComm is now auto-found via
        #   find_package(LibComm REQUIRED) when ENABLE_LIBRI=ON.
        if "+libri" in spec:
            args.append(self.define("LIBRI_DIR", spec["libri"].prefix))
            args.append(self.define("LIBCOMM_DIR", spec["libcomm"].prefix))
            # Gate never fires on currently shipped versions (develop line is
            # capped at 3.9.0.27); it future-proofs the args for a 3.11.x
            # addition, where CMake finds these transitively.
            if not spec.satisfies("@3.11.0:"):
                args.append(self.define("ENABLE_LIBCOMM", True))

        # LibXC: FindLibxc uses Libxc_DIR (prefix) or pkg-config.
        if "+libxc" in spec:
            args.append(self.define("Libxc_DIR", spec["libxc"].prefix))

        # PEXSI:
        # - PEXSI_DIR is needed in all versions.
        # - Recent develop uses find_package(PEXSI REQUIRED CONFIG), which
        #   reads PEXSIConfig.cmake (includes transitive ParMETIS/SuperLU_DIST
        #   paths). Older versions use a custom FindPEXSI.cmake, which needs
        #   ParMETIS_DIR + SuperLU_DIST_DIR explicitly.
        if "+pexsi" in spec:
            args.append(self.define("PEXSI_DIR", spec["pexsi"].prefix))
            # Gate never fires on currently shipped versions (develop line is
            # capped at 3.9.0.27); it future-proofs the args for a 3.11.x
            # addition, where CMake finds these transitively.
            if not spec.satisfies("@3.11.0:"):
                args.append(self.define("ParMETIS_DIR", spec["parmetis"].prefix))
                args.append(self.define("SuperLU_DIST_DIR", spec["superlu-dist"].prefix))

        # DeePMD: variable-driven (DEFINED DeePMD_DIR enables it; no option).
        if "+deepmd" in spec:
            args.append(self.define("DeePMD_DIR", spec["deepmdkit"].prefix))

        # --- version-branched options (core architecture) ---
        if spec.satisfies("@3.10"):
            # LTS old build system
            args.append(self.define_from_variant("ENABLE_DEEPKS", "deepks"))
            # LTS still has ENABLE_PAW but requires libpaw_interface (no
            # spack package). Force OFF -- PAW is not supported in this build.
            args.append(self.define("ENABLE_PAW", False))
            if "+deepks" in spec:
                self._add_torch_args(args, spec)
                args.append(self.define("libnpy_INCLUDE_DIR", spec["libnpy"].prefix.include))

        elif spec.satisfies("@3.9.0.10:"):
            # develop new build system
            args.append(self.define_from_variant("ENABLE_MLALGO", "mlalgo"))
            # USE_SW exists @3.9.0.10: but x86 doesn't need Sunway.
            args.append(self.define("USE_SW", False))
            # ENABLE_PAW was removed @3.9.0.10: do not pass it.

            if "+mlalgo" in spec:
                self._add_torch_args(args, spec)
                args.append(self.define("libnpy_INCLUDE_DIR", spec["libnpy"].prefix.include))

            # NEP was introduced on the develop line @3.9.0.27
            if "+nep" in spec:
                args.append(self.define("NEP_DIR", spec["nep-cpu"].prefix))

        # CUDA architecture forwarding. ABACUS uses CMAKE_CUDA_ARCHITECTURES
        # (CMake 3.18+ native). CudaPackage provides the multi-valued variant.
        if "+cuda" in spec:
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
                elif Pattern1.search(line):
                    pass
                elif Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(join_path(self.build_directory, "Makefile.system"), "w") as f:
            for i in lineList:
                f.write(i)

        with open(join_path(self.build_directory, "Makefile.system"), "a") as f:
            f.write(system_var)

    def install(self, pkg, spec, prefix):
        install_tree("bin", prefix.bin)
