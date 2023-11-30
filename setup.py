import os
import sys
import shutil
import logging
import subprocess
from pathlib import Path
import chardet
from setuptools import setup
from setuptools.command.build_ext import build_ext
from typing import Optional, Dict, Tuple


DEFAULT_CYTHON_VENDER = Path.home().joinpath(".cython_vendor")


def runcmd(command: str, *, cwd: Optional[Path] = None, env: Optional[Dict[str, str]] = None, visible: bool = False, fail_exit: bool = False,) -> str:
    """执行命令行命令并返回其stdout的值

    Args:
        command (str): 命令行命令
        cwd (Optional[Path]): 执行命令时的位置.Default: None
        env (Optional[Any]): 执行命令时的环境变量. Default:None
        visible (bool): 命令可见度. Default: False
        fail_exit (bool): 当执行失败时退出程序. Default: False

    Returns:
        str: stdout捕获的字符串
    """
    try:
        if visible:
            logging.info(f"[run cmd] {command}")
        if command.startswith("[") and command.endswith("]"):
            try:
                command_list = eval(command)
            except SyntaxError:
                sys.exit(1)
            except Exception:
                sys.exit(1)
            else:
                res = subprocess.run(
                    command_list, capture_output=True, shell=True, check=True, cwd=cwd, env=env)
        else:
            res = subprocess.run(command, capture_output=True,
                                 shell=True, check=True, cwd=cwd, env=env)
    except subprocess.CalledProcessError as ce:
        if ce.stderr:
            encoding = chardet.detect(ce.stderr).get("encoding")
            content = ce.stderr.decode(encoding).strip()
        else:
            encoding = chardet.detect(ce.stdout).get("encoding")
            content = ce.stdout.decode(encoding).strip()

        if fail_exit:
            sys.exit(1)
        else:
            raise ce
    except Exception as e:
        if fail_exit:
            sys.exit(1)
        else:
            raise e
    else:
        content = ""
        if res.stdout:
            encoding = chardet.detect(res.stdout).get("encoding")
            content = res.stdout.decode(encoding).strip()
        return content


def build_spdlog() -> Tuple[str, Optional[str], Optional[str]]:
    """编译spdlog"""
    logging.info('[build spdlog] start!')
    # 检查系统中是否有相关的工具(git,cmake,make)
    runcmd("git --version", visible=False, fail_exit=True)
    runcmd("make -v", visible=False, fail_exit=True)
    runcmd("cmake --version", visible=False, fail_exit=True)
    logging.info(f'[build spdlog]can install by source')

    url = "https://github.com/gabime/spdlog.git"
    to = DEFAULT_CYTHON_VENDER.joinpath("spdlog")
    logging.info(f'[build spdlog]spdlog will install in {to}')
    if not to.parent.exists():
        to.parent.mkdir(parents=True)
    else:
        if not to.parent.is_dir():
            logging.info(
                f'[build spdlog]{to.parent} exists but not dir,please remove it first')
            raise Exception(f"{to.parent} is not dir")
    inwondows = False

    if not to.is_dir():
        # 不存在则下载后从源码安装
        to_build = to.parent.joinpath("spdlogbuild")
        logging.info(f'[build spdlog]will build in {to_build}')
        if to_build.exists():
            if to_build.is_dir():
                shutil.rmtree(to_build)
            else:
                to_build.unlink(True)
        clone_cmd = f"git clone {url} {str(to_build)}"
        runcmd(clone_cmd, fail_exit=True)
        logging.info(f'[build spdlog]clone source done')

        try:
            logging.info(f'[build spdlog]compiling')
            if sys.platform.startswith('linux') or sys.platform == 'darwin':
                # 非window平台
                runcmd("mkdir build", cwd=to_build)
                runcmd("cmake ..", cwd=to_build.joinpath("build"))
                runcmd("make -j", cwd=to_build.joinpath("build"))
                logging.info(f'[build spdlog]compile done')
            else:
                inwondows = True
            # copy头文件
            shutil.copytree(to_build.joinpath(
                "include"), to.joinpath("include"))
            logging.info(f'[build spdlog]copy header to {to} done')
            # copy库文件
            if not inwondows:
                to.joinpath("lib").mkdir(exist_ok=True)
                shutil.copyfile(to_build.joinpath("build/libspdlog.a"),
                                to.joinpath("lib/libspdlog.a"))
                logging.info(f'[build spdlog]copy lib to {to} done')
        except Exception as e:
            raise e
        finally:
            # 删除编译源文件
            shutil.rmtree(to_build)
            logging.info(f'[build spdlog]remove build dir {to_build} done')
    else:
        logging.info('[build spdlog]already build yet')
    if inwondows:
        return str(to.joinpath("include")), None, None
    return str(to.joinpath("include")), str(to.joinpath("lib")), "spdlog"


# 待编译包对应的编译函数
LIB_CPL = {
    "spdlog": build_spdlog
}


class binary_build_ext(build_ext):
    """覆写build_ext"""

    def build_extension(self, ext):
        logging.info(f'[build_ext]build_extension start')
        # 从环境变量中指定配置
        candidate_3rdpart = ["spdlog"]
        BINARY_VECTOR_INCLUDE_DIR = os.environ.get('BINARY_VECTOR_INCLUDE_DIR')
        BINARY_VECTOR_LIB_DIR = os.environ.get('BINARY_VECTOR_LIB_DIR')
        # 额外的lib,如果有则需要指定它的对应lib_dir和include_dir
        BINARY_VECTOR_EXT_LIB = os.environ.get('BINARY_VECTOR_EXT_LIB')
        add_include_dirs = []
        add_lib_dirs = []
        add_libs = []
        noneed_downloads = []
        if BINARY_VECTOR_EXT_LIB:
            # 通过环境变量控制额外增加的lib
            add_libs = [i.strip()
                        for i in BINARY_VECTOR_EXT_LIB.split(",")]
            logging.info(f'[build_ext]add_ext_libs {add_libs}')
        # 判断是否存在外部依赖库的环境变量
        if BINARY_VECTOR_INCLUDE_DIR:
            # 判断是否存在外部依赖库的环境变量
            add_include_dirs = [i.strip()
                                for i in BINARY_VECTOR_INCLUDE_DIR.split(",")]
            logging.info(f'[build_ext]add_include_dirs {add_include_dirs}')
        if BINARY_VECTOR_LIB_DIR:
            add_lib_dirs = [i.strip()
                            for i in BINARY_VECTOR_LIB_DIR.split(",")]
            logging.info(f'[build_ext]add_lib_dirs {add_lib_dirs}')
        # # [可选]查找系统库,看有没有用到的candidate_3rdpart,建议注释掉还是源码编译
        if sys.platform.startswith('linux'):
            # linux
            sys_lib_base_dirs = ["/usr/include", "/usr/local/include"]
            for sys_lib_base_dir_str in sys_lib_base_dirs:
                sys_lib_base_dir = Path(sys_lib_base_dir_str)
                for libname in candidate_3rdpart:
                    libpath = sys_lib_base_dir.joinpath(libname)
                    if libpath.is_dir():
                        logging.info(f'[build_ext]{libname} use sys lib')
                        noneed_downloads.append(libname)
                    libpath = sys_lib_base_dir.joinpath(libname+".h")
                    if libpath.is_file():
                        logging.info(f'[build_ext]{libname} use sys lib')
                        noneed_downloads.append(libname)
                    libpath = sys_lib_base_dir.joinpath(libname+".hpp")
                    if libpath.is_file():
                        logging.info(f'[build_ext]{libname} use sys lib')
                        noneed_downloads.append(libname)

        # elif sys.platform == 'darwin':
        #     # macos,查看homebrew
        #     sys_lib_base_dir = Path("/usr/local/Cellar")
        #     for libname in candidate_3rdpart:
        #         libpath = sys_lib_base_dir.joinpath(libname)
        #         if libpath.is_dir():
        #             libversionpath = [i for i in libpath.iterdir() if i.is_dir() and not i.name.startswith(".")]
        #             if len(libversionpath) >= 1:
        #                 version = libversionpath[0].name
        #                 noneed_downloads.append(libname)
        #                 logging.info(f'[build_ext]{libname} use sys lib')
        #                 if Path(f"/usr/local/Cellar/{libname}/{version}/include"):
        #                     add_include_dirs.append(
        #                         f"/usr/local/Cellar/{libname}/{version}/include")
        #                 if Path(f"/usr/local/Cellar/{libname}/{version}/lib").is_dir():
        #                     add_lib_dirs.append(
        #                         f"/usr/local/Cellar/{libname}/{version}/lib")

        need_downloads = list(set(candidate_3rdpart)-set(noneed_downloads))
        logging.info(f'[build_ext]{need_downloads} will install by source')
        # 分别编译
        for libname in need_downloads:
            cf = LIB_CPL.get(libname)
            if cf is None:
                logging.error(
                    f'[build_ext]{libname } do not has compile function')
                raise Exception(f"{libname} without compile function")
            include_dir, lib_dir, lib = cf()
            add_include_dirs.append(include_dir)
            if lib_dir:
                add_lib_dirs.append(lib_dir)
            if lib:
                add_libs.append(lib)

        for inc in add_include_dirs:
            self.compiler.add_include_dir(inc)
        for lib_dir in add_lib_dirs:
            self.compiler.add_library_dir(lib_dir)
        for lib in add_libs:
            self.compiler.add_library(lib)
        logging.info(f'[build_ext]setting done')
        # 针对clang:
        if sys.platform == 'darwin':
            ext.extra_compile_args += ["-Wc++11-extensions", "-std=c++11"]

        # distutils: extra_compile_args = -Wc++11-extensions

        super().build_extension(ext)


try:
    from Cython.Build import cythonize
except Exception as e:
    logging.info(f'[build]pure python mode')
    setup()
else:
    logging.info(f'[build]cython mode')
    setup(
        ext_modules=cythonize("binary_vector/**/*.pyx"),
        cmdclass={
            'build_ext': binary_build_ext
        }
    )
