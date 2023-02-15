import pathlib

from pybind11.setup_helpers import Pybind11Extension, build_ext


def build(setup_kwargs):
    ext_modules = []
    for path in pathlib.Path("src/atcoder").glob("*.cpp"):
        ext_modules.append(
            Pybind11Extension(
                f"atcoder.{path.stem}",
                [str(path)],
                include_dirs=["ac-library"],
                extra_compile_args=["-std=c++14"],
            )
        )

    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmd_class": {"build_ext": build_ext},
            "zip_safe": False,
        }
    )
