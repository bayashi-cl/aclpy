#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/twosat>

namespace py = pybind11;

PYBIND11_MODULE(twosat, m) {
    m.doc() = "atcoder/twosat";
    py::class_<atcoder::two_sat>(m, "two_sat")
        .def(py::init<int>(), py::arg("n") = 0)
        .def("add_clause", &atcoder::two_sat::add_clause, py::arg("i"),
             py::arg("f"), py::arg("j"), py::arg("g"))
        .def("satisfiable", &atcoder::two_sat::satisfiable)
        .def("answer", &atcoder::two_sat::answer);
}
