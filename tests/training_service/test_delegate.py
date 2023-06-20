from unittest import TestCase

from xumes.training_module.entity_manager import DelegateBool, DelegateInt, DelegateFloat, DelegateComplex, DelegateStr, \
    DelegateList, DelegateTuple, DelegateSet, DelegateDict


class TestDelegate(TestCase):
    def test_bool(self):
        b = DelegateBool(True)
        c = DelegateBool(False)
        self.assertTrue(b)
        self.assertFalse(c)
        b = b.update(False)
        c = c.update(True)
        self.assertFalse(b)
        self.assertTrue(c)

    def test_int(self):
        a = DelegateInt(1)
        a = a.update(2)
        a += 1
        self.assertEqual(a, 3)

    def test_float(self):
        a = DelegateFloat(1.0)
        a = a.update(2.0)
        a += 1.0
        self.assertEqual(a, 3.0)

    def test_complex(self):
        a = DelegateComplex(1+1j)
        a = a.update(2+2j)
        a += 1+1j
        self.assertEqual(a, 3+3j)

    def test_str(self):
        a = DelegateStr("a")
        a = a.update("b")
        a += "c"
        self.assertEqual(a, "bc")

    def test_list(self):
        li = DelegateList([1, 2, 3])
        li.append(4)
        self.assertEqual([1, 2, 3, 4], li)
        li = li.update([1, 2, 3, 4, 5])
        self.assertEqual([1, 2, 3, 4, 5], li)

    def test_tuple(self):
        t = DelegateTuple((1, 2, 3))
        t = t.update((1, 2, 3, 4))
        self.assertEqual((1, 2, 3, 4), t)

    def test_set(self):
        s = DelegateSet({1, 2, 3})
        s = s.update({1, 2, 3, 4})
        self.assertEqual({1, 2, 3, 4}, s)

    def test_dict(self):
        d = DelegateDict({1: 1, 2: 2, 3: 3})
        d = d.update({1: 1, 2: 2, 3: 3, 4: 4})
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4}, d)
