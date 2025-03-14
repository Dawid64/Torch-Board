from torchboard.base.trackable_variables import make_trackable_type, track
import pytest


def test_trackables():
    """ Simple test """
    TrackableInt = make_trackable_type(int)
    a = TrackableInt(2)
    b = a ** 2 - 3 * a + 3

    assert a == 2
    assert b == 1

    a.change_value(5)
    assert b == 13

    with pytest.raises(TypeError):
        c = {}
        c[b] = 2  # trackable variables are not hashable

    TrackableStr = make_trackable_type(str)
    s1 = TrackableStr("Hello")
    s2 = s1 + " World"
    assert s2 == "Hello World"
    s1.change_value("Hi")
    assert s2 == "Hi World"


def test_track():
    a = track(2)
    b = 3
    assert a + b == 5
    c = a + b
    a.change_value(10)
    assert c == 13
