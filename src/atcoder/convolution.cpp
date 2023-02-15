#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/convolution>

namespace py = pybind11;
using T = long long;

PYBIND11_MODULE(convolution, m) {
    m.def("convolution_998244353", &atcoder::convolution<998244353, T>,
          py::arg("a"), py::arg("b"));
    m.def("convolution_1000000007", &atcoder::convolution<1000000007, T>,
          py::arg("a"), py::arg("b"));
    m.def("convolution_ll", &atcoder::convolution_ll, py::arg("a"),
          py::arg("b"));
}
