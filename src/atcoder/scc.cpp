#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/scc>

namespace py = pybind11;

PYBIND11_MODULE(scc, m) {
    m.doc() = "atcoder/scc";
    py::class_<atcoder::scc_graph>(m, "scc_graph")
        .def(py::init<int>(), py::arg("n") = 0)
        .def("add_edge", &atcoder::scc_graph::add_edge, py::arg("from_"),
             py::arg("to"))
        .def("scc", &atcoder::scc_graph::scc);
}
