# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

import os
import shutil


class Fzvis(Package):
    """Visualization software for building and understanding the effects of compression."""

    homepage = "https://fzframework.org/"
    url = "https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.3.0.tar.gz"
    git = "https://github.com/YuxiaoLi1234/fzvis"

    maintainers("guoxiliu", "robertu94", "YuxiaoLi1234", "hrithikdevaiah-999")

    license("MIT")

    version("main", branch="main")

    # To be updated
    version("0.3.0", sha256="",
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.3.0.tar.gz")
   
    version("0.2.4", sha256="bb7cb0a6b925a3104f049db17ef61ee3576e3a7ceff00b64ebbc66335e48fb44",
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.2.4.tar.gz")

    version("0.2.3", sha256="dea16cbad1b54d376f7f3e70c64703946df313f9165d775659eff43f6a19b9ae",
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.2.3.tar.gz")

    version("0.2.2", sha256="0d3893970ac775ea59cb8a845101f7e987037aa83dd71071df9bd0b42233c91f",
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.2.2.tar.gz")

    version("0.2.1", sha256="7a42bf5d40c1e331d43a0ee1482f6104f0d5d4254e9d2d469362dcde4a7e8fc8", 
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.2.1.tar.gz")

    version("0.2.0", sha256="bd61d0210adcb70b6b2d189905b6585cd7cf3ea9840a59e6fdae14ea5bb3487d", 
        url="https://github.com/YuxiaoLi1234/fzvis/archive/refs/tags/v0.2.0.tar.gz")

    depends_on("python@3.11", type=("build", "run"))
    depends_on("py-numcodecs@0.11", type=("build"))
    depends_on("py-numpy@1.26", type=("build", "run"))
    depends_on("libpressio+python+json+sz+sz3+zfp", type=("run","link"))
    depends_on("npm@8.19", type="run")
    depends_on("node-js@18.12", type="run")
    # depends_on("py-websockets", type="run")
    # depends_on("py-flask", type="run")
    # depends_on("py-flask-cors", type="run")
    # depends_on("py-netcdf4", type="run")
    # depends_on("py-openai@1.95", type="run")

    def install(self, spec, prefix):
        # Build the frontend 
        npm = which("npm")
        npm("ci")
        npm("run", "build")
        shutil.copytree("dist", prefix.usr.libexec.fzvis.ui)
        if os.path.exists(prefix.join("npm-cache")):
            shutil.rmtree(prefix.join("npm-cache"))

        # Build the backend
        # python = which("python3")
        # python("-m", "venv", "fzvenv")
        # exec("source fzvenv/bin/activate")
        python = which("python3")
        python("-m", "ensurepip", "--default-pip")
        python("-m", "pip", "install", "-r" "requirements.txt")

        # Set up executables
        if not os.path.exists(prefix.bin):
            mkdir(prefix.bin)
        ui_script = prefix.bin.join("fzvis-ui")
        with open(ui_script, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('cd {}\n'.format(prefix.usr.libexec.fzvis.ui))
            f.write('python -m http.server 8000\n')
        set_executable(ui_script)
        shutil.copy2("src/server/main.py", prefix.bin.join("fzvis-server"))
