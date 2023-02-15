#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/math>

namespace py = pybind11;

PYBIND11_MODULE(math, m) {
    m.doc() = "atcoder/math";
    m.def("pow_mod", &atcoder::pow_mod);
    m.def("inv_mod", &atcoder::inv_mod);
    m.def("crt", &atcoder::crt);
    m.def("floor_sum", &atcoder::floor_sum);
}
