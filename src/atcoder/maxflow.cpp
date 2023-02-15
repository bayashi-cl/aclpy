#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/maxflow>

namespace py = pybind11;
using Cap = long long;

PYBIND11_MODULE(maxflow, m) {
    m.doc() = "atcoder/maxflow";
    py::class_<atcoder::mf_graph<Cap>> mf(m, "mf_graph");
    mf.def(py::init<int>(), py::arg("n") = 0)
        .def("add_edge", &atcoder::mf_graph<Cap>::add_edge, py::arg("from_"),
             py::arg("to"), py::arg("cap"))
        .def("get_edge", &atcoder::mf_graph<Cap>::get_edge, py::arg("i"))
        .def("edges", &atcoder::mf_graph<Cap>::edges)
        .def("change_edge", &atcoder::mf_graph<Cap>::change_edge, py::arg("i"),
             py::arg("new_cap"), py::arg("new_flow"))
        .def("flow", py::overload_cast<int, int>(&atcoder::mf_graph<Cap>::flow),
             py::arg("s"), py::arg("t"))
        .def("flow",
             py::overload_cast<int, int, Cap>(&atcoder::mf_graph<Cap>::flow),
             py::arg("s"), py::arg("t"), py::arg("flow_limit"))
        .def("min_cut", &atcoder::mf_graph<Cap>::min_cut, py::arg("s"));

    py::class_<atcoder::mf_graph<Cap>::edge>(mf, "edge")
        .def(py::init<>())
        .def_readwrite("from_", &atcoder::mf_graph<Cap>::edge::from)
        .def_readwrite("to", &atcoder::mf_graph<Cap>::edge::to)
        .def_readwrite("cap", &atcoder::mf_graph<Cap>::edge::cap)
        .def_readwrite("flow", &atcoder::mf_graph<Cap>::edge::flow);
}
