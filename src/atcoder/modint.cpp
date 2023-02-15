#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <atcoder/modint>

namespace py = pybind11;
using ll = long long;

PYBIND11_MODULE(modint, m) {
    m.doc() = "atcoder/modint";
#define DEFINE_STATIC_MODINT(MOD, NAME)                                     \
    py::class_<atcoder::static_modint<MOD>>(m, NAME)                        \
        .def_static("mod", &atcoder::static_modint<MOD>::mod)               \
        .def_static("raw", &atcoder::static_modint<MOD>::raw, py::arg("v")) \
        .def(py::init<ll>(), py::arg("v") = 0)                              \
        .def("val", &atcoder::static_modint<MOD>::val)                      \
        .def(py::self += py::self)                                          \
        .def(py::self += ll())                                              \
        .def(py::self -= py::self)                                          \
        .def(py::self -= ll())                                              \
        .def(py::self *= py::self)                                          \
        .def(py::self *= ll())                                              \
        .def(py::self /= py::self)                                          \
        .def(py::self /= ll())                                              \
        .def(+py::self)                                                     \
        .def(-py::self)                                                     \
        .def("pow", &atcoder::static_modint<MOD>::pow, py::arg("n"))        \
        .def("inv", &atcoder::static_modint<MOD>::inv)                      \
        .def(py::self + py::self)                                           \
        .def(py::self + ll())                                               \
        .def(ll() + py::self)                                               \
        .def(py::self - py::self)                                           \
        .def(py::self - ll())                                               \
        .def(ll() - py::self) /* clang-format off */                        \
        .def(py::self * py::self)                                           \
        .def(py::self * ll()) /* clang-format on */                         \
        .def(ll() * py::self)                                               \
        .def(py::self / py::self)                                           \
        .def(py::self / ll())                                               \
        .def(ll() / py::self)                                               \
        .def(py::self == py::self)                                          \
        .def(py::self != py::self)
    DEFINE_STATIC_MODINT(998244353, "modint998244353");
    DEFINE_STATIC_MODINT(1000000007, "modint1000000007");
#undef DEFINE_STATIC_MODINT

#define DEFINE_DYNAMIC_MODINT(ID, NAME)                                     \
    py::class_<atcoder::dynamic_modint<ID>>(m, NAME)                        \
        .def_static("mod", &atcoder::dynamic_modint<ID>::mod)               \
        .def_static("set_mod", &atcoder::dynamic_modint<ID>::set_mod,       \
                    py::arg("m"))                                           \
        .def_static("raw", &atcoder::dynamic_modint<ID>::raw, py::arg("v")) \
        .def(py::init<ll>(), py::arg("v") = 0)                              \
        .def("val", &atcoder::dynamic_modint<ID>::val)                      \
        .def(py::self += py::self)                                          \
        .def(py::self += ll())                                              \
        .def(py::self -= py::self)                                          \
        .def(py::self -= ll())                                              \
        .def(py::self *= py::self)                                          \
        .def(py::self *= ll())                                              \
        .def(py::self /= py::self)                                          \
        .def(py::self /= ll())                                              \
        .def(+py::self)                                                     \
        .def(-py::self)                                                     \
        .def("pow", &atcoder::dynamic_modint<ID>::pow, py::arg("n"))        \
        .def("inv", &atcoder::dynamic_modint<ID>::inv)                      \
        .def(py::self + py::self)                                           \
        .def(py::self + ll())                                               \
        .def(ll() + py::self)                                               \
        .def(py::self - py::self)                                           \
        .def(py::self - ll())                                               \
        .def(ll() - py::self) /* clang-format off */                        \
        .def(py::self * py::self)                                           \
        .def(py::self * ll()) /* clang-format on */                         \
        .def(ll() * py::self)                                               \
        .def(py::self / py::self)                                           \
        .def(py::self / ll())                                               \
        .def(ll() / py::self)                                               \
        .def(py::self == py::self)                                          \
        .def(py::self != py::self)
    DEFINE_DYNAMIC_MODINT(-1, "modint");
    DEFINE_DYNAMIC_MODINT(0, "modint0");
    DEFINE_DYNAMIC_MODINT(1, "modint1");
    DEFINE_DYNAMIC_MODINT(2, "modint2");
    DEFINE_DYNAMIC_MODINT(3, "modint3");
    DEFINE_DYNAMIC_MODINT(4, "modint4");
    DEFINE_DYNAMIC_MODINT(5, "modint5");
    DEFINE_DYNAMIC_MODINT(6, "modint6");
    DEFINE_DYNAMIC_MODINT(7, "modint7");
#undef DEFINE_DYNAMIC_MODINT
}
