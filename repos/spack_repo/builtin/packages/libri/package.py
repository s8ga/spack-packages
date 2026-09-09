# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Libri(Package):
    """LibRI is a header-only library for resolution-of-identity (RI)
    methods, used by ABACUS for hybrid functional (EXX) calculations."""

    homepage = "https://github.com/abacusmodeling/LibRI"
    url = "https://github.com/abacusmodeling/LibRI/archive/refs/tags/v0.2.1.1.tar.gz"

    maintainers("s8ga")

    license("GPL-3.0-only", checked_by="s8ga")

    version("0.2.1.1", sha256="cd33fd5428400ea696b82c9132878c07bf785847b3f56b1979e25a3a5fc0b311")
    version("0.2.1.0", sha256="66a5540daba36effdad6ce2fe5e8368b96ddd4a7e148af90894ef21dc20ff29f")
    version("0.2.0.0", sha256="1fbdcf1ae35fb24b93cc766b0ef89509c81c111fa3797b009d7a2c99f691d332")

    depends_on("cxx", type="build")

    # LibRI headers #include <Comm/...> from LibComm.
    depends_on("libcomm")

    sanity_check_is_file = [join_path("include", "RI", "version.h")]

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
