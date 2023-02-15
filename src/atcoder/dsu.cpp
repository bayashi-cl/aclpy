#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/dsu>

namespace py = pybind11;

PYBIND11_MODULE(dsu, m) {
    m.doc() = "atcoder/dsu";
    py::class_<atcoder::dsu>(m, "dsu")
        .def(py::init<int>(), py::arg("n") = 0)
        .def("mearge", &atcoder::dsu::merge, py::arg("a"), py::arg("b"))
        .def("same", &atcoder::dsu::same, py::arg("a"), py::arg("b"))
        .def("leader", &atcoder::dsu::leader, py::arg("a"))
        .def("size", &atcoder::dsu::size, py::arg("a"))
        .def("groups", &atcoder::dsu::groups);
}
