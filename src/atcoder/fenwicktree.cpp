#include <pybind11/pybind11.h>
#include <atcoder/fenwicktree>

namespace py = pybind11;

PYBIND11_MODULE(fenwicktree, m) {
    m.doc() = "atcoder/fenwicktree";
    py::class_<atcoder::fenwick_tree<long long>>(m, "fenwick_tree")
        .def(py::init<int>(), py::arg("n") = 0)
        .def("add", &atcoder::fenwick_tree<long long>::add, py::arg("p"),
             py::arg("x"))
        .def(
            "sum",
            py::overload_cast<int, int>(&atcoder::fenwick_tree<long long>::sum),
            py::arg("l"), py::arg("r"));
}
