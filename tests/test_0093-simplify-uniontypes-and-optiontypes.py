# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import sys

import pytest
import numpy

import awkward1

def test_numpyarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    np1 = numpy.arange(2*7*5).reshape(2, 7, 5)
    np2 = numpy.arange(3*7*5).reshape(3, 7, 5)
    ak1 = awkward1.layout.NumpyArray(np1)
    ak2 = awkward1.layout.NumpyArray(np2)

    assert awkward1.tolist(ak1.merge(ak2)) == awkward1.tolist(numpy.concatenate([np1, np2]))
    assert awkward1.tolist(ak1[1:, :-1, ::-1].merge(ak2[1:, :-1, ::-1])) == awkward1.tolist(numpy.concatenate([np1[1:, :-1, ::-1], np2[1:, :-1, ::-1]]))

    for x, y, z in [(numpy.double, numpy.double, numpy.double),
                    (numpy.double, numpy.float,  numpy.double),
                    (numpy.double, numpy.int64,  numpy.double),
                    (numpy.double, numpy.uint64, numpy.double),
                    (numpy.double, numpy.int32,  numpy.double),
                    (numpy.double, numpy.uint32, numpy.double),
                    (numpy.double, numpy.int16,  numpy.double),
                    (numpy.double, numpy.uint16, numpy.double),
                    (numpy.double, numpy.int8,   numpy.double),
                    (numpy.double, numpy.uint8,  numpy.double),
                    (numpy.double, numpy.bool,   numpy.double),
                    (numpy.float,  numpy.double, numpy.double),
                    (numpy.float,  numpy.float,  numpy.double),
                    (numpy.float,  numpy.int64,  numpy.double),
                    (numpy.float,  numpy.uint64, numpy.double),
                    (numpy.float,  numpy.int32,  numpy.double),
                    (numpy.float,  numpy.uint32, numpy.double),
                    (numpy.float,  numpy.int16,  numpy.double),
                    (numpy.float,  numpy.uint16, numpy.double),
                    (numpy.float,  numpy.int8,   numpy.double),
                    (numpy.float,  numpy.uint8,  numpy.double),
                    (numpy.float,  numpy.bool,   numpy.double),
                    (numpy.int64,  numpy.double, numpy.double),
                    (numpy.int64,  numpy.float,  numpy.double),
                    (numpy.int64,  numpy.int64,  numpy.int64),
                    (numpy.int64,  numpy.uint64, numpy.int64),
                    (numpy.int64,  numpy.int32,  numpy.int64),
                    (numpy.int64,  numpy.uint32, numpy.int64),
                    (numpy.int64,  numpy.int16,  numpy.int64),
                    (numpy.int64,  numpy.uint16, numpy.int64),
                    (numpy.int64,  numpy.int8,   numpy.int64),
                    (numpy.int64,  numpy.uint8,  numpy.int64),
                    (numpy.int64,  numpy.bool,   numpy.int64),
                    (numpy.uint64, numpy.double, numpy.double),
                    (numpy.uint64, numpy.float,  numpy.double),
                    (numpy.uint64, numpy.int64,  numpy.int64),
                    (numpy.uint64, numpy.uint64, numpy.uint64),
                    (numpy.uint64, numpy.int32,  numpy.int64),
                    (numpy.uint64, numpy.uint32, numpy.int64),
                    (numpy.uint64, numpy.int16,  numpy.int64),
                    (numpy.uint64, numpy.uint16, numpy.int64),
                    (numpy.uint64, numpy.int8,   numpy.int64),
                    (numpy.uint64, numpy.uint8,  numpy.int64),
                    (numpy.uint64, numpy.bool,   numpy.int64),
                    (numpy.int32,  numpy.double, numpy.double),
                    (numpy.int32,  numpy.float,  numpy.double),
                    (numpy.int32,  numpy.int64,  numpy.int64),
                    (numpy.int32,  numpy.uint64, numpy.int64),
                    (numpy.int32,  numpy.int32,  numpy.int64),
                    (numpy.int32,  numpy.uint32, numpy.int64),
                    (numpy.int32,  numpy.int16,  numpy.int64),
                    (numpy.int32,  numpy.uint16, numpy.int64),
                    (numpy.int32,  numpy.int8,   numpy.int64),
                    (numpy.int32,  numpy.uint8,  numpy.int64),
                    (numpy.int32,  numpy.bool,   numpy.int64),
                    (numpy.uint32, numpy.double, numpy.double),
                    (numpy.uint32, numpy.float,  numpy.double),
                    (numpy.uint32, numpy.int64,  numpy.int64),
                    (numpy.uint32, numpy.uint64, numpy.int64),
                    (numpy.uint32, numpy.int32,  numpy.int64),
                    (numpy.uint32, numpy.uint32, numpy.int64),
                    (numpy.uint32, numpy.int16,  numpy.int64),
                    (numpy.uint32, numpy.uint16, numpy.int64),
                    (numpy.uint32, numpy.int8,   numpy.int64),
                    (numpy.uint32, numpy.uint8,  numpy.int64),
                    (numpy.uint32, numpy.bool,   numpy.int64),
                    (numpy.int16,  numpy.double, numpy.double),
                    (numpy.int16,  numpy.float,  numpy.double),
                    (numpy.int16,  numpy.int64,  numpy.int64),
                    (numpy.int16,  numpy.uint64, numpy.int64),
                    (numpy.int16,  numpy.int32,  numpy.int64),
                    (numpy.int16,  numpy.uint32, numpy.int64),
                    (numpy.int16,  numpy.int16,  numpy.int64),
                    (numpy.int16,  numpy.uint16, numpy.int64),
                    (numpy.int16,  numpy.int8,   numpy.int64),
                    (numpy.int16,  numpy.uint8,  numpy.int64),
                    (numpy.int16,  numpy.bool,   numpy.int64),
                    (numpy.uint16, numpy.double, numpy.double),
                    (numpy.uint16, numpy.float,  numpy.double),
                    (numpy.uint16, numpy.int64,  numpy.int64),
                    (numpy.uint16, numpy.uint64, numpy.int64),
                    (numpy.uint16, numpy.int32,  numpy.int64),
                    (numpy.uint16, numpy.uint32, numpy.int64),
                    (numpy.uint16, numpy.int16,  numpy.int64),
                    (numpy.uint16, numpy.uint16, numpy.int64),
                    (numpy.uint16, numpy.int8,   numpy.int64),
                    (numpy.uint16, numpy.uint8,  numpy.int64),
                    (numpy.uint16, numpy.bool,   numpy.int64),
                    (numpy.int8,   numpy.double, numpy.double),
                    (numpy.int8,   numpy.float,  numpy.double),
                    (numpy.int8,   numpy.int64,  numpy.int64),
                    (numpy.int8,   numpy.uint64, numpy.int64),
                    (numpy.int8,   numpy.int32,  numpy.int64),
                    (numpy.int8,   numpy.uint32, numpy.int64),
                    (numpy.int8,   numpy.int16,  numpy.int64),
                    (numpy.int8,   numpy.uint16, numpy.int64),
                    (numpy.int8,   numpy.int8,   numpy.int64),
                    (numpy.int8,   numpy.uint8,  numpy.int64),
                    (numpy.int8,   numpy.bool,   numpy.int64),
                    (numpy.uint8,  numpy.double, numpy.double),
                    (numpy.uint8,  numpy.float,  numpy.double),
                    (numpy.uint8,  numpy.int64,  numpy.int64),
                    (numpy.uint8,  numpy.uint64, numpy.int64),
                    (numpy.uint8,  numpy.int32,  numpy.int64),
                    (numpy.uint8,  numpy.uint32, numpy.int64),
                    (numpy.uint8,  numpy.int16,  numpy.int64),
                    (numpy.uint8,  numpy.uint16, numpy.int64),
                    (numpy.uint8,  numpy.int8,   numpy.int64),
                    (numpy.uint8,  numpy.uint8,  numpy.int64),
                    (numpy.uint8,  numpy.bool,   numpy.int64),
                    (numpy.bool,   numpy.double, numpy.double),
                    (numpy.bool,   numpy.float,  numpy.double),
                    (numpy.bool,   numpy.int64,  numpy.int64),
                    (numpy.bool,   numpy.uint64, numpy.int64),
                    (numpy.bool,   numpy.int32,  numpy.int64),
                    (numpy.bool,   numpy.uint32, numpy.int64),
                    (numpy.bool,   numpy.int16,  numpy.int64),
                    (numpy.bool,   numpy.uint16, numpy.int64),
                    (numpy.bool,   numpy.int8,   numpy.int64),
                    (numpy.bool,   numpy.uint8,  numpy.int64),
                    (numpy.bool,   numpy.bool,   numpy.bool)]:
        one = awkward1.layout.NumpyArray(numpy.array([1, 2, 3], dtype=x))
        two = awkward1.layout.NumpyArray(numpy.array([4, 5], dtype=y))
        three = one.merge(two)
        assert numpy.asarray(three).dtype == numpy.dtype(z)
        assert awkward1.tolist(three) == awkward1.tolist(numpy.concatenate([numpy.asarray(one), numpy.asarray(two)]))
        assert awkward1.tolist(one.merge(emptyarray)) == awkward1.tolist(one)
        assert awkward1.tolist(emptyarray.merge(one)) == awkward1.tolist(one)

def test_regulararray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    np1 = numpy.arange(2*7*5).reshape(2, 7, 5)
    np2 = numpy.arange(3*7*5).reshape(3, 7, 5)
    ak1 = awkward1.Array(np1, checkvalid=True).layout
    ak2 = awkward1.Array(np2, checkvalid=True).layout

    assert awkward1.tolist(ak1.merge(ak2)) == awkward1.tolist(numpy.concatenate([np1, np2]))
    assert awkward1.tolist(ak1.merge(emptyarray)) == awkward1.tolist(ak1)
    assert awkward1.tolist(emptyarray.merge(ak1)) == awkward1.tolist(ak1)

def test_listarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    content1 = awkward1.layout.NumpyArray(numpy.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    content2 = awkward1.layout.NumpyArray(numpy.array([1, 2, 3, 4, 5, 6, 7]))

    for (dtype1, Index1, ListArray1), (dtype2, Index2, ListArray2) in [
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32),    (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32)),
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32),    (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32)),
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32),    (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32), (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32), (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32), (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64),    (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64),    (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64),    (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64))]:
        starts1 = Index1(numpy.array([0, 3, 3], dtype=dtype1))
        stops1  = Index1(numpy.array([3, 3, 5], dtype=dtype1))
        starts2 = Index2(numpy.array([2, 99, 0], dtype=dtype2))
        stops2  = Index2(numpy.array([6, 99, 3], dtype=dtype2))
        array1 = ListArray1(starts1, stops1, content1)
        array2 = ListArray2(starts2, stops2, content2)
        assert awkward1.tolist(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert awkward1.tolist(array2) == [[3, 4, 5, 6], [], [1, 2, 3]]

        assert awkward1.tolist(array1.merge(array2)) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [3, 4, 5, 6], [], [1, 2, 3]]
        assert awkward1.tolist(array2.merge(array1)) == [[3, 4, 5, 6], [], [1, 2, 3], [1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert awkward1.tolist(array1.merge(emptyarray)) == awkward1.tolist(array1)
        assert awkward1.tolist(emptyarray.merge(array1)) == awkward1.tolist(array1)

    regulararray = awkward1.layout.RegularArray(content2, 2)
    assert awkward1.tolist(regulararray) == [[1, 2], [3, 4], [5, 6]]
    assert awkward1.tolist(regulararray.merge(emptyarray)) == awkward1.tolist(regulararray)
    assert awkward1.tolist(emptyarray.merge(regulararray)) == awkward1.tolist(regulararray)

    for (dtype1, Index1, ListArray1) in [
            (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32),
            (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32),
            (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64)]:
        starts1 = Index1(numpy.array([0, 3, 3], dtype=dtype1))
        stops1  = Index1(numpy.array([3, 3, 5], dtype=dtype1))
        array1 = ListArray1(starts1, stops1, content1)

        assert awkward1.tolist(array1.merge(regulararray)) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [1, 2], [3, 4], [5, 6]]
        assert awkward1.tolist(regulararray.merge(array1)) == [[1, 2], [3, 4], [5, 6], [1.1, 2.2, 3.3], [], [4.4, 5.5]]

def test_listoffsetarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    content1 = awkward1.layout.NumpyArray(numpy.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    content2 = awkward1.layout.NumpyArray(numpy.array([1, 2, 3, 4, 5, 6, 7]))

    for (dtype1, Index1, ListOffsetArray1), (dtype2, Index2, ListOffsetArray2) in [
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32),    (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32)),
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32),    (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32)),
            ((numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32),    (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32), (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32), (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32)),
            ((numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32), (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64),    (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListOffsetArray32)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64),    (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListOffsetArrayU32)),
            ((numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64),    (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListOffsetArray64))]:
        offsets1 = Index1(numpy.array([0, 3, 3, 5], dtype=dtype1))
        offsets2 = Index2(numpy.array([1, 3, 3, 3, 5], dtype=dtype2))
        array1 = ListOffsetArray1(offsets1, content1)
        array2 = ListOffsetArray2(offsets2, content2)
        assert awkward1.tolist(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert awkward1.tolist(array2) == [[2, 3], [], [], [4, 5]]

        assert awkward1.tolist(array1.merge(array2)) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [2, 3], [], [], [4, 5]]
        assert awkward1.tolist(array2.merge(array1)) == [[2, 3], [], [], [4, 5], [1.1, 2.2, 3.3], [], [4.4, 5.5]]
        assert awkward1.tolist(array1.merge(emptyarray)) == awkward1.tolist(array1)
        assert awkward1.tolist(emptyarray.merge(array1)) == awkward1.tolist(array1)

    regulararray = awkward1.layout.RegularArray(content2, 2)
    assert awkward1.tolist(regulararray) == [[1, 2], [3, 4], [5, 6]]

    for (dtype1, Index1, ListArray1) in [
            (numpy.int32, awkward1.layout.Index32, awkward1.layout.ListArray32),
            (numpy.uint32, awkward1.layout.IndexU32, awkward1.layout.ListArrayU32),
            (numpy.int64, awkward1.layout.Index64, awkward1.layout.ListArray64)]:
        starts1 = Index1(numpy.array([0, 3, 3], dtype=dtype1))
        stops1  = Index1(numpy.array([3, 3, 5], dtype=dtype1))
        array1 = ListArray1(starts1, stops1, content1)

        assert awkward1.tolist(array1.merge(regulararray)) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [1, 2], [3, 4], [5, 6]]
        assert awkward1.tolist(regulararray.merge(array1)) == [[1, 2], [3, 4], [5, 6], [1.1, 2.2, 3.3], [], [4.4, 5.5]]

def test_recordarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    arrayr1 = awkward1.Array([{"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}], checkvalid=True).layout
    arrayr2 = awkward1.Array([{"x": 2.2, "y": [2.2, 2.2]}, {"x": 1.1, "y": [1.1, 1.1]}, {"x": 0.0, "y": [0.0, 0.0]}], checkvalid=True).layout
    arrayr3 = awkward1.Array([{"x": 0, "y": 0.0}, {"x": 1, "y": 1.1}, {"x": 2, "y": 2.2}], checkvalid=True).layout
    arrayr4 = awkward1.Array([{"y": [], "x": 0}, {"y": [1, 1], "x": 1}, {"y": [2, 2], "x": 2}], checkvalid=True).layout
    arrayr5 = awkward1.Array([{"x": 0, "y": [], "z": 0}, {"x": 1, "y": [1, 1], "z": 1}, {"x": 2, "y": [2, 2], "z": 2}], checkvalid=True).layout
    arrayr6 = awkward1.Array([{"z": 0, "x": 0, "y": []}, {"z": 1, "x": 1, "y": [1, 1]}, {"z": 2, "x": 2, "y": [2, 2]}], checkvalid=True).layout
    arrayr7 = awkward1.Array([{"x": 0}, {"x": 1}, {"x": 2}], checkvalid=True).layout

    arrayt1 = awkward1.Array([(0, []), (1, [1.1]), (2, [2, 2])], checkvalid=True).layout
    arrayt2 = awkward1.Array([(2.2, [2.2, 2.2]), (1.1, [1.1, 1.1]), (0.0, [0.0, 0.0])], checkvalid=True).layout
    arrayt3 = awkward1.Array([(0, 0.0), (1, 1.1), (2, 2.2)], checkvalid=True).layout
    arrayt4 = awkward1.Array([([], 0), ([1.1], 1), ([2.2, 2.2], 2)], checkvalid=True).layout
    arrayt5 = awkward1.Array([(0, [], 0), (1, [1], 1), (2, [2, 2], 2)], checkvalid=True).layout
    arrayt6 = awkward1.Array([(0, 0, []), (1, 1, [1]), (2, 2, [2, 2])], checkvalid=True).layout
    arrayt7 = awkward1.Array([(0,), (1,), (2,)], checkvalid=True).layout

    assert arrayr1.mergeable(arrayr2)
    assert arrayr2.mergeable(arrayr1)
    assert not arrayr1.mergeable(arrayr3)
    assert arrayr1.mergeable(arrayr4)
    assert arrayr4.mergeable(arrayr1)
    assert not arrayr1.mergeable(arrayr5)
    assert not arrayr1.mergeable(arrayr6)
    assert arrayr5.mergeable(arrayr6)
    assert arrayr6.mergeable(arrayr5)
    assert not arrayr1.mergeable(arrayr7)

    assert arrayt1.mergeable(arrayt2)
    assert arrayt2.mergeable(arrayt1)
    assert not arrayt1.mergeable(arrayt3)
    assert not arrayt1.mergeable(arrayt4)
    assert not arrayt1.mergeable(arrayt5)
    assert not arrayt1.mergeable(arrayt6)
    assert not arrayt5.mergeable(arrayt6)
    assert not arrayt1.mergeable(arrayt7)

    assert awkward1.tolist(arrayr1.merge(arrayr2)) == [{"x": 0.0, "y": []}, {"x": 1.0, "y": [1.0, 1.0]}, {"x": 2.0, "y": [2.0, 2.0]}, {"x": 2.2, "y": [2.2, 2.2]}, {"x": 1.1, "y": [1.1, 1.1]}, {"x": 0.0, "y": [0.0, 0.0]}]
    assert awkward1.tolist(arrayr2.merge(arrayr1)) == [{"x": 2.2, "y": [2.2, 2.2]}, {"x": 1.1, "y": [1.1, 1.1]}, {"x": 0.0, "y": [0.0, 0.0]}, {"x": 0.0, "y": []}, {"x": 1.0, "y": [1.0, 1.0]}, {"x": 2.0, "y": [2.0, 2.0]}]

    assert awkward1.tolist(arrayr1.merge(arrayr4)) == [{"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}, {"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}]
    assert awkward1.tolist(arrayr4.merge(arrayr1)) == [{"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}, {"x": 0, "y": []}, {"x": 1, "y": [1, 1]}, {"x": 2, "y": [2, 2]}]

    assert awkward1.tolist(arrayr5.merge(arrayr6)) == [{"x": 0, "y": [], "z": 0}, {"x": 1, "y": [1, 1], "z": 1}, {"x": 2, "y": [2, 2], "z": 2}, {"x": 0, "y": [], "z": 0}, {"x": 1, "y": [1, 1], "z": 1}, {"x": 2, "y": [2, 2], "z": 2}]
    assert awkward1.tolist(arrayr6.merge(arrayr5)) == [{"x": 0, "y": [], "z": 0}, {"x": 1, "y": [1, 1], "z": 1}, {"x": 2, "y": [2, 2], "z": 2}, {"x": 0, "y": [], "z": 0}, {"x": 1, "y": [1, 1], "z": 1}, {"x": 2, "y": [2, 2], "z": 2}]

    assert awkward1.tolist(arrayt1.merge(arrayt2)) == [(0.0, []), (1.0, [1.1]), (2.0, [2.0, 2.0]), (2.2, [2.2, 2.2]), (1.1, [1.1, 1.1]), (0.0, [0.0, 0.0])]
    assert awkward1.tolist(arrayt2.merge(arrayt1)) == [(2.2, [2.2, 2.2]), (1.1, [1.1, 1.1]), (0.0, [0.0, 0.0]), (0.0, []), (1.0, [1.1]), (2.0, [2.0, 2.0])]

    assert awkward1.tolist(arrayr1.merge(emptyarray)) == awkward1.tolist(arrayr1)
    assert awkward1.tolist(arrayr2.merge(emptyarray)) == awkward1.tolist(arrayr2)
    assert awkward1.tolist(arrayr3.merge(emptyarray)) == awkward1.tolist(arrayr3)
    assert awkward1.tolist(arrayr4.merge(emptyarray)) == awkward1.tolist(arrayr4)
    assert awkward1.tolist(arrayr5.merge(emptyarray)) == awkward1.tolist(arrayr5)
    assert awkward1.tolist(arrayr6.merge(emptyarray)) == awkward1.tolist(arrayr6)
    assert awkward1.tolist(arrayr7.merge(emptyarray)) == awkward1.tolist(arrayr7)

    assert awkward1.tolist(emptyarray.merge(arrayr1)) == awkward1.tolist(arrayr1)
    assert awkward1.tolist(emptyarray.merge(arrayr2)) == awkward1.tolist(arrayr2)
    assert awkward1.tolist(emptyarray.merge(arrayr3)) == awkward1.tolist(arrayr3)
    assert awkward1.tolist(emptyarray.merge(arrayr4)) == awkward1.tolist(arrayr4)
    assert awkward1.tolist(emptyarray.merge(arrayr5)) == awkward1.tolist(arrayr5)
    assert awkward1.tolist(emptyarray.merge(arrayr6)) == awkward1.tolist(arrayr6)
    assert awkward1.tolist(emptyarray.merge(arrayr7)) == awkward1.tolist(arrayr7)

    assert awkward1.tolist(arrayt1.merge(emptyarray)) == awkward1.tolist(arrayt1)
    assert awkward1.tolist(arrayt2.merge(emptyarray)) == awkward1.tolist(arrayt2)
    assert awkward1.tolist(arrayt3.merge(emptyarray)) == awkward1.tolist(arrayt3)
    assert awkward1.tolist(arrayt4.merge(emptyarray)) == awkward1.tolist(arrayt4)
    assert awkward1.tolist(arrayt5.merge(emptyarray)) == awkward1.tolist(arrayt5)
    assert awkward1.tolist(arrayt6.merge(emptyarray)) == awkward1.tolist(arrayt6)
    assert awkward1.tolist(arrayt7.merge(emptyarray)) == awkward1.tolist(arrayt7)

    assert awkward1.tolist(emptyarray.merge(arrayt1)) == awkward1.tolist(arrayt1)
    assert awkward1.tolist(emptyarray.merge(arrayt2)) == awkward1.tolist(arrayt2)
    assert awkward1.tolist(emptyarray.merge(arrayt3)) == awkward1.tolist(arrayt3)
    assert awkward1.tolist(emptyarray.merge(arrayt4)) == awkward1.tolist(arrayt4)
    assert awkward1.tolist(emptyarray.merge(arrayt5)) == awkward1.tolist(arrayt5)
    assert awkward1.tolist(emptyarray.merge(arrayt6)) == awkward1.tolist(arrayt6)
    assert awkward1.tolist(emptyarray.merge(arrayt7)) == awkward1.tolist(arrayt7)

def test_indexedarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    content1 = awkward1.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]], checkvalid=True).layout
    content2 = awkward1.Array([[1, 2], [], [3, 4]], checkvalid=True).layout
    index1 = awkward1.layout.Index64(numpy.array([2, 0, -1, 0, 1, 2], dtype=numpy.int64))
    indexedarray1 = awkward1.layout.IndexedOptionArray64(index1, content1)
    assert awkward1.tolist(indexedarray1) == [[4.4, 5.5], [1.1, 2.2, 3.3], None, [1.1, 2.2, 3.3], [], [4.4, 5.5]]

    assert awkward1.tolist(indexedarray1.merge(content2)) == [[4.4, 5.5], [1.1, 2.2, 3.3], None, [1.1, 2.2, 3.3], [], [4.4, 5.5], [1.0, 2.0], [], [3.0, 4.0]]
    assert awkward1.tolist(content2.merge(indexedarray1)) == [[1.0, 2.0], [], [3.0, 4.0], [4.4, 5.5], [1.1, 2.2, 3.3], None, [1.1, 2.2, 3.3], [], [4.4, 5.5]]
    assert awkward1.tolist(indexedarray1.merge(indexedarray1)) == [[4.4, 5.5], [1.1, 2.2, 3.3], None, [1.1, 2.2, 3.3], [], [4.4, 5.5], [4.4, 5.5], [1.1, 2.2, 3.3], None, [1.1, 2.2, 3.3], [], [4.4, 5.5]]

def test_unionarray_merge():
    emptyarray = awkward1.layout.EmptyArray()

    one = awkward1.Array([0.0, 1.1, 2.2, [], [1], [2, 2]], checkvalid=True).layout
    two = awkward1.Array([{"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}], checkvalid=True).layout
    three = awkward1.Array(["one", "two", "three"], checkvalid=True).layout

    assert awkward1.tolist(one.merge(two)) == [0.0, 1.1, 2.2, [], [1], [2, 2], {"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}]
    assert awkward1.tolist(two.merge(one)) == [{"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}, 0.0, 1.1, 2.2, [], [1], [2, 2]]

    assert awkward1.tolist(one.merge(emptyarray)) == [0.0, 1.1, 2.2, [], [1], [2, 2]]
    assert awkward1.tolist(emptyarray.merge(one)) == [0.0, 1.1, 2.2, [], [1], [2, 2]]

    assert awkward1.tolist(one.merge(three)) == [0.0, 1.1, 2.2, [], [1], [2, 2], "one", "two", "three"]
    assert awkward1.tolist(two.merge(three)) == [{"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}, "one", "two", "three"]
    assert awkward1.tolist(three.merge(one)) == ["one", "two", "three", 0.0, 1.1, 2.2, [], [1], [2, 2]]
    assert awkward1.tolist(three.merge(two)) == ["one", "two", "three", {"x": 1, "y": 1.1}, 999, 123, {"x": 2, "y": 2.2}]

def test_merge_parameters():
    one = awkward1.Array([[121, 117, 99, 107, 121], [115, 116, 117, 102, 102]], checkvalid=True).layout
    two = awkward1.Array(["good", "stuff"], checkvalid=True).layout

    assert awkward1.tolist(one.merge(two)) == [[121, 117, 99, 107, 121], [115, 116, 117, 102, 102], "good", "stuff"]
    assert awkward1.tolist(two.merge(one)) == ["good", "stuff", [121, 117, 99, 107, 121], [115, 116, 117, 102, 102]]

def test_bytemask():
    array = awkward1.Array(["one", "two", None, "three", None, None, "four"], checkvalid=True).layout
    assert numpy.asarray(array.bytemask()).tolist() == [0, 0, 1, 0, 1, 1, 0]

    index2 = awkward1.layout.Index64(numpy.array([2, 2, 1, 5, 0], dtype=numpy.int64))
    array2 = awkward1.layout.IndexedArray64(index2, array)
    assert numpy.asarray(array2.bytemask()).tolist() == [0, 0, 0, 0, 0]

def test_indexedarray_simplify():
    array = awkward1.Array(["one", "two", None, "three", None, None, "four", "five"], checkvalid=True).layout
    assert numpy.asarray(array.index).tolist() == [0, 1, -1, 2, -1, -1, 3, 4]

    index2 = awkward1.layout.Index64(numpy.array([2, 2, 1, 6, 5], dtype=numpy.int64))
    array2 = awkward1.layout.IndexedArray64(index2, array)
    assert awkward1.tolist(array2.simplify()) == awkward1.tolist(array2) == [None, None, "two", "four", None]

def test_indexedarray_simplify_more():
    content = awkward1.layout.NumpyArray(numpy.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]))

    index1_32 = awkward1.layout.Index32(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.int32))
    index1_U32 = awkward1.layout.IndexU32(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.uint32))
    index1_64 = awkward1.layout.Index64(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.int64))
    index2_32 = awkward1.layout.Index32(numpy.array([0, 2, 4, 6], dtype=numpy.int32))
    index2_U32 = awkward1.layout.IndexU32(numpy.array([0, 2, 4, 6], dtype=numpy.uint32))
    index2_64 = awkward1.layout.Index64(numpy.array([0, 2, 4, 6], dtype=numpy.int64))

    array = awkward1.layout.IndexedArray32(index2_32, awkward1.layout.IndexedArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray32(index2_32, awkward1.layout.IndexedArrayU32(index1_U32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray32(index2_32, awkward1.layout.IndexedArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArrayU32(index2_U32, awkward1.layout.IndexedArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArrayU32(index2_U32, awkward1.layout.IndexedArrayU32(index1_U32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArrayU32(index2_U32, awkward1.layout.IndexedArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray64(index2_64, awkward1.layout.IndexedArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray64(index2_64, awkward1.layout.IndexedArrayU32(index1_U32, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray64(index2_64, awkward1.layout.IndexedArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, 4.4, 2.2, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, 4.4, 2.2, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    index1_32 = awkward1.layout.Index32(numpy.array([6, 5, -1, 3, -1, 1, 0], dtype=numpy.int32))
    index1_64 = awkward1.layout.Index64(numpy.array([6, 5, -1, 3, -1, 1, 0], dtype=numpy.int64))
    index2_32 = awkward1.layout.Index32(numpy.array([0, 2, 4, 6], dtype=numpy.int32))
    index2_U32 = awkward1.layout.IndexU32(numpy.array([0, 2, 4, 6], dtype=numpy.uint32))
    index2_64 = awkward1.layout.Index64(numpy.array([0, 2, 4, 6], dtype=numpy.int64))

    array = awkward1.layout.IndexedArray32(index2_32, awkward1.layout.IndexedOptionArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray32(index2_32, awkward1.layout.IndexedOptionArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArrayU32(index2_U32, awkward1.layout.IndexedOptionArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArrayU32(index2_U32, awkward1.layout.IndexedOptionArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray64(index2_64, awkward1.layout.IndexedOptionArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedArray64(index2_64, awkward1.layout.IndexedOptionArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, None, 0.0]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, 0.0]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    index1_32 = awkward1.layout.Index32(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.int32))
    index1_U32 = awkward1.layout.IndexU32(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.uint32))
    index1_64 = awkward1.layout.Index64(numpy.array([6, 5, 4, 3, 2, 1, 0], dtype=numpy.int64))
    index2_32 = awkward1.layout.Index32(numpy.array([0, -1, 4, -1], dtype=numpy.int32))
    index2_64 = awkward1.layout.Index64(numpy.array([0, -1, 4, -1], dtype=numpy.int64))

    array = awkward1.layout.IndexedOptionArray32(index2_32, awkward1.layout.IndexedArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray32(index2_32, awkward1.layout.IndexedArrayU32(index1_U32, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray32(index2_32, awkward1.layout.IndexedArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray64(index2_64, awkward1.layout.IndexedArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray64(index2_64, awkward1.layout.IndexedArrayU32(index1_U32, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray64(index2_64, awkward1.layout.IndexedArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, 2.2, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, 2.2, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    index1_32 = awkward1.layout.Index32(numpy.array([6, 5, -1, 3, -1, 1, 0], dtype=numpy.int32))
    index1_64 = awkward1.layout.Index64(numpy.array([6, 5, -1, 3, -1, 1, 0], dtype=numpy.int64))
    index2_32 = awkward1.layout.Index32(numpy.array([0, -1, 4, -1], dtype=numpy.int32))
    index2_64 = awkward1.layout.Index64(numpy.array([0, -1, 4, -1], dtype=numpy.int64))

    array = awkward1.layout.IndexedOptionArray32(index2_32, awkward1.layout.IndexedOptionArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, None, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray32(index2_32, awkward1.layout.IndexedOptionArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, None, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray64(index2_64, awkward1.layout.IndexedOptionArray32(index1_32, content))
    assert awkward1.tolist(array) == [6.6, None, None, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

    array = awkward1.layout.IndexedOptionArray64(index2_64, awkward1.layout.IndexedOptionArray64(index1_64, content))
    assert awkward1.tolist(array) == [6.6, None, None, None]
    assert awkward1.tolist(array.simplify()) == [6.6, None, None, None]
    assert isinstance(array.simplify(), awkward1.layout.IndexedOptionArray64)
    assert isinstance(array.simplify().content, awkward1.layout.NumpyArray)

def test_unionarray_simplify_one():
    one = awkward1.Array([5, 4, 3, 2, 1], checkvalid=True).layout
    two = awkward1.Array([[], [1], [2, 2], [3, 3, 3]], checkvalid=True).layout
    three = awkward1.Array([1.1, 2.2, 3.3], checkvalid=True).layout
    tags  =  awkward1.layout.Index8(numpy.array([0, 0, 1, 2, 1, 0, 2, 1, 1, 0, 2, 0], dtype=numpy.int8))
    index = awkward1.layout.Index64(numpy.array([0, 1, 0, 0, 1, 2, 1, 2, 3, 3, 2, 4], dtype=numpy.int64))
    array = awkward1.layout.UnionArray8_64(tags, index, [one, two, three])

    assert awkward1.tolist(array) == [5, 4, [], 1.1, [1], 3, 2.2, [2, 2], [3, 3, 3], 2, 3.3, 1]
    assert awkward1.tolist(array.simplify()) == [5.0, 4.0, [], 1.1, [1], 3.0, 2.2, [2, 2], [3, 3, 3], 2.0, 3.3, 1.0]
    assert len(array.contents) == 3
    assert len(array.simplify().contents) == 2

def test_unionarray_simplify():
    one = awkward1.Array([5, 4, 3, 2, 1], checkvalid=True).layout
    two = awkward1.Array([[], [1], [2, 2], [3, 3, 3]], checkvalid=True).layout
    three = awkward1.Array([1.1, 2.2, 3.3], checkvalid=True).layout

    tags2  =  awkward1.layout.Index8(numpy.array([0, 1, 0, 1, 0, 0, 1], dtype=numpy.int8))
    index2 = awkward1.layout.Index32(numpy.array([0, 0, 1, 1, 2, 3, 2], dtype=numpy.int32))
    inner = awkward1.layout.UnionArray8_32(tags2, index2, [two, three])
    tags1  =  awkward1.layout.Index8(numpy.array([0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0], dtype=numpy.int8))
    index1 = awkward1.layout.Index64(numpy.array([0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4], dtype=numpy.int64))
    outer = awkward1.layout.UnionArray8_64(tags1, index1, [one, inner])
    assert awkward1.tolist(outer) == [5, 4, [], 1.1, [1], 3, 2.2, [2, 2], [3, 3, 3], 2, 3.3, 1]

    assert awkward1.tolist(outer.simplify()) == [5.0, 4.0, [], 1.1, [1], 3.0, 2.2, [2, 2], [3, 3, 3], 2.0, 3.3, 1.0]
    assert isinstance(outer.content(1), awkward1.layout.UnionArray8_32)
    assert isinstance(outer.simplify().content(0), awkward1.layout.NumpyArray)
    assert isinstance(outer.simplify().content(1), awkward1.layout.ListOffsetArray64)
    assert len(outer.simplify().contents) == 2

    tags2  =  awkward1.layout.Index8(numpy.array([0, 1, 0, 1, 0, 0, 1], dtype=numpy.int8))
    index2 = awkward1.layout.Index64(numpy.array([0, 0, 1, 1, 2, 3, 2], dtype=numpy.int64))
    inner = awkward1.layout.UnionArray8_64(tags2, index2, [two, three])
    tags1  =  awkward1.layout.Index8(numpy.array([1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], dtype=numpy.int8))
    index1 = awkward1.layout.Index32(numpy.array([0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4], dtype=numpy.int32))
    outer = awkward1.layout.UnionArray8_32(tags1, index1, [inner, one])
    assert awkward1.tolist(outer) == [5, 4, [], 1.1, [1], 3, 2.2, [2, 2], [3, 3, 3], 2, 3.3, 1]

def test_concatenate():
    one = awkward1.Array([1.1, 2.2, 3.3, 4.4, 5.5], checkvalid=True)
    two = awkward1.Array([[], [1], [2, 2], [3, 3, 3]], checkvalid=True)
    three = awkward1.Array([True, False, False, True, True], checkvalid=True)

    assert awkward1.tolist(awkward1.concatenate([one, two, three])) == [1.1, 2.2, 3.3, 4.4, 5.5, [], [1], [2, 2], [3, 3, 3], 1.0, 0.0, 0.0, 1.0, 1.0]
    assert isinstance(awkward1.concatenate([one, two, three]).layout, awkward1.layout.UnionArray8_64)
    assert len(awkward1.concatenate([one, two, three]).layout.contents) == 2

def test_where():
    condition = awkward1.Array([True, False, True, False, True], checkvalid=True)
    one = awkward1.Array([1.1, 2.2, 3.3, 4.4, 5.5], checkvalid=True)
    two = awkward1.Array([False, False, False, True, True], checkvalid=True)
    three = awkward1.Array([[], [1], [2, 2], [3, 3, 3], [4, 4, 4, 4]], checkvalid=True)

    assert awkward1.tolist(awkward1.where(condition, one, two)) == [1.1, 0.0, 3.3, 1.0, 5.5]
    assert awkward1.tolist(awkward1.where(condition, one, three)) == [1.1, [1], 3.3, [3, 3, 3], 5.5]
