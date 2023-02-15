#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <atcoder/internal_bit>

// 本家は非型テンプレートとして関数ポインタが必要なのでそのままバインドできない。
// std::functionを使って再実装する。
// std::vector<py::object> を使うのであまり速くはなさそう・・・

namespace atcoder {

template <class S, class F> struct lazysegtree {
  public:
    explicit lazysegtree(const std::function<S(S, S)>& op,
                         const std::function<S()>& e,
                         const std::function<S(F, S)>& mapping,
                         const std::function<F(F, F)>& composition,
                         const std::function<F()>& id,
                         int n)
        : lazysegtree(op, e, mapping, composition, id, std::vector<S>(n, e())) {
    }
    explicit lazysegtree(const std::function<S(S, S)>& op,
                         const std::function<S()>& e,
                         const std::function<S(F, S)>& mapping,
                         const std::function<F(F, F)>& composition,
                         const std::function<F()>& id,
                         const std::vector<S>& v)
        : _n(int(v.size())),
          op(op),
          e(e),
          mapping(mapping),
          composition(composition),
          id(id) {
        log = internal::ceil_pow2(_n);
        size = 1 << log;
        d = std::vector<S>(2 * size, e());
        lz = std::vector<F>(size, id());
        for (int i = 0; i < _n; i++) d[size + i] = v[i];
        for (int i = size - 1; i >= 1; i--) {
            update(i);
        }
    }

    void set(int p, S x) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        d[p] = x;
        for (int i = 1; i <= log; i++) update(p >> i);
    }

    S get(int p) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        return d[p];
    }

    S prod(int l, int r) {
        assert(0 <= l && l <= r && r <= _n);
        if (l == r) return e();

        l += size;
        r += size;

        for (int i = log; i >= 1; i--) {
            if (((l >> i) << i) != l) push(l >> i);
            if (((r >> i) << i) != r) push((r - 1) >> i);
        }

        S sml = e(), smr = e();
        while (l < r) {
            if (l & 1) sml = op(sml, d[l++]);
            if (r & 1) smr = op(d[--r], smr);
            l >>= 1;
            r >>= 1;
        }

        return op(sml, smr);
    }

    S all_prod() { return d[1]; }

    void apply(int p, F f) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        d[p] = mapping(f, d[p]);
        for (int i = 1; i <= log; i++) update(p >> i);
    }
    void apply(int l, int r, F f) {
        assert(0 <= l && l <= r && r <= _n);
        if (l == r) return;

        l += size;
        r += size;

        for (int i = log; i >= 1; i--) {
            if (((l >> i) << i) != l) push(l >> i);
            if (((r >> i) << i) != r) push((r - 1) >> i);
        }

        {
            int l2 = l, r2 = r;
            while (l < r) {
                if (l & 1) all_apply(l++, f);
                if (r & 1) all_apply(--r, f);
                l >>= 1;
                r >>= 1;
            }
            l = l2;
            r = r2;
        }

        for (int i = 1; i <= log; i++) {
            if (((l >> i) << i) != l) update(l >> i);
            if (((r >> i) << i) != r) update((r - 1) >> i);
        }
    }

    int max_right(int l, const std::function<bool(S)>& g) {
        assert(0 <= l && l <= _n);
        assert(g(e()));
        if (l == _n) return _n;
        l += size;
        for (int i = log; i >= 1; i--) push(l >> i);
        S sm = e();
        do {
            while (l % 2 == 0) l >>= 1;
            if (!g(op(sm, d[l]))) {
                while (l < size) {
                    push(l);
                    l = (2 * l);
                    if (g(op(sm, d[l]))) {
                        sm = op(sm, d[l]);
                        l++;
                    }
                }
                return l - size;
            }
            sm = op(sm, d[l]);
            l++;
        } while ((l & -l) != l);
        return _n;
    }

    int min_left(int r, const std::function<bool(S)>& g) {
        assert(0 <= r && r <= _n);
        assert(g(e()));
        if (r == 0) return 0;
        r += size;
        for (int i = log; i >= 1; i--) push((r - 1) >> i);
        S sm = e();
        do {
            r--;
            while (r > 1 && (r % 2)) r >>= 1;
            if (!g(op(d[r], sm))) {
                while (r < size) {
                    push(r);
                    r = (2 * r + 1);
                    if (g(op(d[r], sm))) {
                        sm = op(d[r], sm);
                        r--;
                    }
                }
                return r + 1 - size;
            }
            sm = op(d[r], sm);
        } while ((r & -r) != r);
        return 0;
    }

  private:
    int _n, size, log;
    std::function<S(S, S)> op;
    std::function<S()> e;
    std::function<S(F, S)> mapping;
    std::function<F(F, F)> composition;
    std::function<F()> id;
    std::vector<S> d;
    std::vector<F> lz;

    void update(int k) { d[k] = op(d[2 * k], d[2 * k + 1]); }
    void all_apply(int k, F f) {
        d[k] = mapping(f, d[k]);
        if (k < size) lz[k] = composition(f, lz[k]);
    }
    void push(int k) {
        all_apply(2 * k, lz[k]);
        all_apply(2 * k + 1, lz[k]);
        lz[k] = id();
    }
};

}  // namespace atcoder

namespace py = pybind11;
using S = py::object;
using F = py::object;

PYBIND11_MODULE(lazysegtree, m) {
    m.doc() = "atcoder/lazysegtree";
    py::class_<atcoder::lazysegtree<S, F>>(m, "lazysegtree")
        .def(py::init<const std::function<S(S, S)>&, const std::function<S()>&,
                      const std::function<F(F, S)>&,
                      const std::function<F(F, F)>&, const std::function<F()>&,
                      int>())
        .def(py::init<const std::function<S(S, S)>&, const std::function<S()>&,
                      const std::function<F(F, S)>&,
                      const std::function<F(F, F)>&, const std::function<F()>&,
                      const std::vector<S>&>())
        .def("set", &atcoder::lazysegtree<S, F>::set, py::arg("p"),
             py::arg("x"))
        .def("get", &atcoder::lazysegtree<S, F>::get, py::arg("p"))
        .def("prod", &atcoder::lazysegtree<S, F>::prod, py::arg("l"),
             py::arg("r"))
        .def("all_prod", &atcoder::lazysegtree<S, F>::all_prod)
        .def("apply",
             py::overload_cast<int, F>(&atcoder::lazysegtree<S, F>::apply),
             py::arg("p"), py::arg("x"))
        .def("apply",
             py::overload_cast<int, int, F>(&atcoder::lazysegtree<S, F>::apply),
             py::arg("l"), py::arg("r"), py::arg("x"))
        .def("max_right", &atcoder::lazysegtree<S, F>::max_right, py::arg("l"),
             py::arg("g"))
        .def("min_left", &atcoder::lazysegtree<S, F>::min_left, py::arg("r"),
             py::arg("g"));
}
