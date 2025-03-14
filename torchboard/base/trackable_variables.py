import operator
from typing import TypeVar
T = TypeVar('T')


def track(variable: T) -> T:
    """ Change passed variable into trackable """
    return make_trackable_type(variable.__class__)(variable)


def make_trackable_type(base_cls: type[T]) -> type:
    class_name = f"Trackable{base_cls.__name__.capitalize()}"

    class _Trackable(base_cls):

        def __new__(cls, value=None, expr=None, deps=None):
            """
            Our custom constructor logic in __new__.
            """
            if expr is not None:
                initial_val = expr()
            else:
                initial_val = value if value is not None else base_cls()

            obj = super().__new__(cls, initial_val)

            obj._base_value = None if expr else initial_val
            obj._expr = expr
            obj._deps = deps or ()
            return obj

        def __init__(self, value=None, expr=None, deps=None):
            # In most cases not called
            self._expr: None
            self._base_value: None
            self._deps: tuple

        def _get_current_value(self):
            if self._expr is not None:
                return self._expr()
            else:
                return self._base_value

        def change_value(self, new_value):
            if self._expr is not None:
                raise ValueError("Cannot change_value() on a derived object.")
            self._base_value = new_value

        def __repr__(self):
            if self._expr is not None:
                return f"<Derived {class_name} value={self._get_current_value()}>"
            else:
                return f"<Base {class_name} value={self._base_value}>"

        def __eq__(self, other):
            if isinstance(other, _Trackable):
                return self._get_current_value() == other._get_current_value()
            else:
                return self._get_current_value() == other

        def __add__(self, other):
            return _make_derived_op(self, other, operator.add, _Trackable)

        def __radd__(self, other):
            return _make_derived_op(other, self, operator.add, _Trackable)

        def __sub__(self, other):
            return _make_derived_op(self, other, operator.sub, _Trackable)

        def __rsub__(self, other):
            return _make_derived_op(other, self, operator.sub, _Trackable)

        def __mul__(self, other):
            return _make_derived_op(self, other, operator.mul, _Trackable)

        def __rmul__(self, other):
            return _make_derived_op(other, self, operator.mul, _Trackable)

        def __truediv__(self, other):
            return _make_derived_op(self, other, operator.truediv, _Trackable)

        def __rtruediv__(self, other):
            return _make_derived_op(other, self, operator.truediv, _Trackable)

        def __floordiv__(self, other):
            return _make_derived_op(self, other, operator.floordiv, _Trackable)

        def __rfloordiv__(self, other):
            return _make_derived_op(other, self, operator.floordiv, _Trackable)

        def __mod__(self, other):
            return _make_derived_op(self, other, operator.mod, _Trackable)

        def __rmod__(self, other):
            return _make_derived_op(other, self, operator.mod, _Trackable)

        def __pow__(self, other):
            return _make_derived_op(self, other, operator.pow, _Trackable)

        def __rpow__(self, other):
            return _make_derived_op(other, self, operator.pow, _Trackable)

        def __and__(self, other):
            return _make_derived_op(self, other, operator.and_, _Trackable)

        def __rand__(self, other):
            return _make_derived_op(other, self, operator.and_, _Trackable)

        def __or__(self, other):
            return _make_derived_op(self, other, operator.or_, _Trackable)

        def __ror__(self, other):
            return _make_derived_op(other, self, operator.or_, _Trackable)

        def __xor__(self, other):
            return _make_derived_op(self, other, operator.xor, _Trackable)

        def __rxor__(self, other):
            return _make_derived_op(other, self, operator.xor, _Trackable)

        def __lshift__(self, other):
            return _make_derived_op(self, other, operator.lshift, _Trackable)

        def __rlshift__(self, other):
            return _make_derived_op(other, self, operator.lshift, _Trackable)

        def __rshift__(self, other):
            return _make_derived_op(self, other, operator.rshift, _Trackable)

        def __rrshift__(self, other):
            return _make_derived_op(other, self, operator.rshift, _Trackable)

        def __neg__(self):
            def expr():
                return operator.neg(self._get_current_value())
            return _Trackable(expr=expr, deps=(self,))

        def __pos__(self):
            def expr():
                return operator.pos(self._get_current_value())
            return _Trackable(expr=expr, deps=(self,))

        def __invert__(self):
            def expr():
                return operator.invert(self._get_current_value())
            return _Trackable(expr=expr, deps=(self,))

    _Trackable.__name__ = class_name
    return _Trackable


def _wrap_if_needed(x, trackable_cls):
    """
    If x is not already a trackable object, wrap it as a base trackable.
    """
    if isinstance(x, trackable_cls):
        return x
    return trackable_cls(value=x)


def _make_derived_op(a, b, op_func, trackable_cls):
    A = _wrap_if_needed(a, trackable_cls)
    B = _wrap_if_needed(b, trackable_cls)

    def expr():
        return op_func(A._get_current_value(), B._get_current_value())
    return trackable_cls(expr=expr, deps=(A, B))
