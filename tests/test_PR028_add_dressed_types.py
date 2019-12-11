# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

import sys
import itertools
import collections

import pytest
import numpy

import awkward1
import awkward1.behavior.string

py27 = (sys.version_info[0] < 3)

def test_fromnumpy():
    a = numpy.arange(2*3*5).reshape((2, 3, 5))
    b = awkward1.fromnumpy(a)
    assert awkward1.tolist(a) == awkward1.tolist(b)

def test_highlevel():
    a = awkward1.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]])
    assert repr(a) == "<Array [[1.1, 2.2, 3.3], ... [7.7, 8.8, 9.9]] type='5 * var * float64'>"
    assert str(a) == "[[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]"

    b = awkward1.Array(numpy.arange(100, dtype=numpy.int32))
    assert repr(b) == "<Array [0, 1, 2, 3, 4, ... 95, 96, 97, 98, 99] type='100 * int32'>"
    assert str(b) == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ... 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]"

    c = awkward1.Array('[{"one": 3.14, "two": [1.1, 2.2]}, {"one": 99.9, "two": [-3.1415926]}]')
    assert repr(c) == "<Array [{one: 3.14, two: [1.1, ... -3.14]}] type=\"2 * {'one': float64, 'two': va...\">"
    assert str(c) == "[{one: 3.14, two: [1.1, 2.2]}, {one: 99.9, two: [-3.14]}]"

class Dummy(awkward1.highlevel.Array):
    pass

def test_dress():
    dressed0 = awkward1.layout.DressedType(awkward1.layout.PrimitiveType("float64"), Dummy, one=1, two=2)
    assert repr(dressed0) in ("dress[float64, 'tests.test_PR028_add_dressed_types.Dummy', one=1, two=2]", "dress[float64, 'tests.test_PR028_add_dressed_types.Dummy', two=2, one=1]")

    pyclass = awkward1.behavior.string.CharBehavior
    inner = awkward1.layout.PrimitiveType("uint8")

    baseline = sys.getrefcount(pyclass)
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline, 2)
    dressed1 = awkward1.layout.DressedType(inner, pyclass, encoding="utf-8")
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 1, 2)
    dressed2 = awkward1.layout.DressedType(inner, pyclass, encoding="utf-8")
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 2, 2)
    dressed3 = awkward1.layout.DressedType(inner, pyclass)
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 3, 2)

    assert repr(dressed1) == "utf8"
    assert repr(dressed3) == "char"
    assert dressed1 == dressed2
    assert dressed1 != dressed3

    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 3, 2)
    del dressed1
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 2, 2)
    del dressed2
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline + 1, 2)
    del dressed3
    assert (sys.getrefcount(pyclass), sys.getrefcount(inner)) == (baseline, 2)

def test_string1():
    a = awkward1.Array(numpy.array([ord(x) for x in "hey there"], dtype=numpy.uint8))
    a.__class__ = awkward1.behavior.string.CharBehavior
    assert str(a) == str(b"hey there")
    assert repr(a) == repr(b"hey there")

def test_string2():
    content = awkward1.layout.NumpyArray(numpy.array([ord(x) for x in "heythere"], dtype=numpy.uint8))
    listoffsetarray = awkward1.layout.ListOffsetArray64(awkward1.layout.Index64(numpy.array([0, 3, 3, 8])), content)
    a = awkward1.Array(listoffsetarray)

    assert isinstance(a, awkward1.Array)
    assert not isinstance(a, awkward1.behavior.string.StringBehavior)
    assert awkward1.tolist(a) == [[104, 101, 121], [], [116, 104, 101, 114, 101]]

    assert repr(a.type) == "3 * var * uint8"
    assert repr(a[0].type) == "3 * uint8"
    assert repr(a[1].type) == "0 * uint8"
    assert repr(a[2].type) == "5 * uint8"

    assert repr(a) == "<Array [[104, 101, 121], ... 101, 114, 101]] type='3 * var * uint8'>"
    assert str(a) == "[[104, 101, 121], [], [116, 104, 101, 114, 101]]"
    assert repr(a[0]) == "<Array [104, 101, 121] type='3 * uint8'>"
    assert repr(a[1]) == "<Array [] type='0 * uint8'>"
    assert repr(a[2]) == "<Array [116, 104, 101, 114, 101] type='5 * uint8'>"

    a.type = awkward1.layout.ArrayType(awkward1.string, 3)

    assert isinstance(a, awkward1.Array)
    assert isinstance(a, awkward1.behavior.string.StringBehavior)
    assert awkward1.tolist(a) == ['hey', '', 'there']

    assert repr(a.type) == "3 * string"
    assert repr(a[0].type) == "3 * utf8"
    assert repr(a[1].type) == "0 * utf8"
    assert repr(a[2].type) == "5 * utf8"

    if py27:
        assert repr(a) == "<Array [u'hey', u'', u'there'] type='3 * string'>"
        assert repr(a[0]) == "u'hey'"
        assert repr(a[1]) == "u''"
        assert repr(a[2]) == "u'there'"
    else:
        assert repr(a) == "<Array ['hey', '', 'there'] type='3 * string'>"
        assert repr(a[0]) == "'hey'"
        assert repr(a[1]) == "''"
        assert repr(a[2]) == "'there'"

def test_accepts():
    content = awkward1.layout.NumpyArray(numpy.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype=numpy.float64))
    listoffsetarray = awkward1.layout.ListOffsetArray64(awkward1.layout.Index64(numpy.array([0, 3, 3, 5])), content)

    dressed1 = awkward1.layout.DressedType(awkward1.layout.ListType(awkward1.layout.PrimitiveType("float64")), Dummy)
    listoffsetarray.type = dressed1

    dressed2 = awkward1.layout.DressedType(awkward1.layout.PrimitiveType("float64"), Dummy)
    with pytest.raises(ValueError):
        listoffsetarray.type = dressed2

class D(awkward1.highlevel.Array):
    @staticmethod
    def typestr(baretype, parameters):
        return "D[{0}]".format(baretype)

def test_type_propagation():
    array = awkward1.Array([[{"one": 1, "two": [1.0, 1.1]}, {"one": 2, "two": [2.0]}, {"one": 3, "two": [3.0, 3.1, 3.2]}], [], [{"one": 4, "two": []}, {"one": 5, "two": [5.0, 5.1, 5.2, 5.3]}]])
    assert awkward1.tolist(array) == [[{"one": 1, "two": [1.0, 1.1]}, {"one": 2, "two": [2.0]}, {"one": 3, "two": [3.0, 3.1, 3.2]}], [], [{"one": 4, "two": []}, {"one": 5, "two": [5.0, 5.1, 5.2, 5.3]}]]
    assert repr(array.type) in ("3 * var * {'one': int64, 'two': var * float64}", "3 * var * {'two': var * float64, 'one': int64}")

    dfloat64 = awkward1.layout.DressedType(awkward1.layout.PrimitiveType("float64"), D)
    dvarfloat64 = awkward1.layout.DressedType(awkward1.layout.ListType(dfloat64), D)
    dint64 = awkward1.layout.DressedType(awkward1.layout.PrimitiveType("int64"), D)
    drec = awkward1.layout.DressedType(awkward1.layout.RecordType(collections.OrderedDict([("one", dint64), ("two", dvarfloat64)])), D)
    dvarrec = awkward1.layout.DressedType(awkward1.layout.ListType(drec), D)

    array.layout.type = awkward1.layout.ArrayType(dvarrec, 3)
    assert array.layout.type == awkward1.layout.ArrayType(dvarrec, 3)
    assert array.layout.content.type == awkward1.layout.ArrayType(drec, 5)
    assert array.layout.content.field("one").type == awkward1.layout.ArrayType(dint64, 5)
    assert array.layout.content.field("two").type == awkward1.layout.ArrayType(dvarfloat64, 5)
    assert array.layout.content.field("two").content.type == awkward1.layout.ArrayType(dfloat64, 10)

    assert array.layout[-1].type == awkward1.layout.ArrayType(drec, 2)
    assert array.layout[-1]["one"].type == awkward1.layout.ArrayType(dint64, 2)
    assert array.layout[-1]["two"].type == awkward1.layout.ArrayType(dvarfloat64, 2)
    assert array.layout[-1]["two"][1].type == awkward1.layout.ArrayType(dfloat64, 4)
    assert array.layout[-1, "one"].type == awkward1.layout.ArrayType(dint64, 2)
    assert array.layout[-1, "two"].type == awkward1.layout.ArrayType(dvarfloat64, 2)
    assert array.layout[-1, "two", 1].type == awkward1.layout.ArrayType(dfloat64, 4)
    assert array.layout["one", -1].type == awkward1.layout.ArrayType(dint64, 2)
    assert array.layout["two", -1].type == awkward1.layout.ArrayType(dvarfloat64, 2)
    assert array.layout["two", -1, 1].type == awkward1.layout.ArrayType(dfloat64, 4)

    assert array.layout[1:].type == awkward1.layout.ArrayType(dvarrec, 2)
    assert array.layout[1:, "one"].type == awkward1.layout.ArrayType(awkward1.layout.ListType(dint64), 2)
    assert array.layout["one", 1:].type == awkward1.layout.ArrayType(awkward1.layout.ListType(dint64), 2)

    assert array.layout[[2, 1]].type == awkward1.layout.ArrayType(dvarrec, 2)
    assert array.layout[[2, 1], "one"].type == awkward1.layout.ArrayType(awkward1.layout.ListType(dint64), 2)

    array2 = awkward1.layout.NumpyArray(numpy.arange(2*3*5, dtype=numpy.int64).reshape(2, 3, 5))
    array2.type = awkward1.layout.ArrayType(awkward1.layout.RegularType(awkward1.layout.RegularType(dint64, 5), 3), 2)

    assert repr(array2.baretype) == "2 * 3 * 5 * int64"
    assert repr(array2.type) == "2 * 3 * 5 * D[int64]"
    assert repr(array2[0].type) == "3 * 5 * D[int64]"
    assert repr(array2[0, 0].type) == "5 * D[int64]"
    assert array2[-1, -1, -1] == 29