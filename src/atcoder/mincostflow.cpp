#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/mincostflow>

namespace py = pybind11;
using Cap = long long;
using Cost = long long;

PYBIND11_MODULE(mincostflow, m) {
    m.doc() = "atcoder/mincostflow";
    py::class_<atcoder::mcf_graph<Cap, Cost>> mcf(m, "mcf_graph");
    mcf.def(py::init<int>(), py::arg("n") = 0)
        .def("add_edge", &atcoder::mcf_graph<Cap, Cost>::add_edge,
             py::arg("from_"), py::arg("to"), py::arg("cap"), py::arg("cost"))
        .def("get_edge", &atcoder::mcf_graph<Cap, Cost>::get_edge, py::arg("i"))
        .def("edges", &atcoder::mcf_graph<Cap, Cost>::edges)
        .def("flow",
             py::overload_cast<int, int>(&atcoder::mcf_graph<Cap, Cost>::flow),
             py::arg("s"), py::arg("t"))
        .def("flow",
             py::overload_cast<int, int, Cap>(
                 &atcoder::mcf_graph<Cap, Cost>::flow),
             py::arg("s"), py::arg("t"), py::arg("flow_limit"))
        .def("slope",
             py::overload_cast<int, int>(&atcoder::mcf_graph<Cap, Cost>::slope),
             py::arg("s"), py::arg("t"))
        .def("slope",
             py::overload_cast<int, int, Cap>(
                 &atcoder::mcf_graph<Cap, Cost>::slope),
             py::arg("s"), py::arg("t"), py::arg("flow_limit"));

    py::class_<atcoder::mcf_graph<Cap, Cost>::edge>(mcf, "edge")
        .def(py::init<>())
        .def_readwrite("from_", &atcoder::mcf_graph<Cap, Cost>::edge::from)
        .def_readwrite("to", &atcoder::mcf_graph<Cap, Cost>::edge::to)
        .def_readwrite("cap", &atcoder::mcf_graph<Cap, Cost>::edge::cap)
        .def_readwrite("flow", &atcoder::mcf_graph<Cap, Cost>::edge::flow)
        .def_readwrite("cost", &atcoder::mcf_graph<Cap, Cost>::edge::cost);
}
