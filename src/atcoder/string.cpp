#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <atcoder/string>

namespace py = pybind11;

PYBIND11_MODULE(string, m) {
    m.doc() = "atcoder/string";
    m.def(
        "suffix_array",
        [](const std::vector<int>& s, int upper) -> std::vector<int> {
            return atcoder::suffix_array(s, upper);
        },
        py::arg("s"), py::arg("upper"));
    m.def(
        "suffix_array",
        [](const std::vector<long long>& s) -> std::vector<int> {
            return atcoder::suffix_array(s);
        },
        py::arg("s"));
    m.def(
        "suffix_array",
        [](const std::string& s) -> std::vector<int> {
            return atcoder::suffix_array(s);
        },
        py::arg("s"));

    m.def(
        "lcp_array",
        [](const std::vector<long long>& s, const std::vector<int>& sa)
            -> std::vector<int> { return atcoder::lcp_array(s, sa); },
        py::arg("s"), py::arg("sa"));
    m.def(
        "lcp_array",
        [](const std::string& s, const std::vector<int>& sa)
            -> std::vector<int> { return atcoder::lcp_array(s, sa); },
        py::arg("s"), py::arg("sa"));

    m.def(
        "z_algorithm",
        [](const std::vector<long long>& s) -> std::vector<int> {
            return atcoder::z_algorithm(s);
        },
        py::arg("s"));
    m.def(
        "z_algorithm",
        [](const std::string& s) -> std::vector<int> {
            return atcoder::z_algorithm(s);
        },
        py::arg("s"));
}

/*
テンプレート関数と非テンプレート関数をオーバーロードできなかったのでラムダ式でラップして回避
*/
