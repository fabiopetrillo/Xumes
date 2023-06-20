from unittest import TestCase

from xumes.training_module.entity_manager import Object, DelegateList, DelegateTuple, DelegateSet, DelegateDict


class TestObject(TestCase):

    def test_list_object(self):
        o = Object({"a": 1, "__type__": "Test"})
        li = DelegateList([o])
        li = li.update([o, o])
        self.assertEqual([o, o], li)

    def test_tuple_object(self):
        o = Object({"a": 1, "__type__": "Test"})
        t = DelegateTuple((0,))
        t = t.update((o, o))
        self.assertEqual((o, o), t)

    def test_set_object(self):
        o = Object({"a": 1, "__type__": "Test"})
        o2 = Object({"a": 2, "__type__": "Test"})
        s = DelegateSet({o})
        s = s.update({o, o2})
        self.assertEqual({o, o2}, s)
        self.assertNotEqual({o}, s)

    def test_dict_object(self):
        o = Object({"a": 1, "__type__": "Test"})
        o2 = Object({"a": 2, "__type__": "Test"})
        d = DelegateDict({1: o})
        d = d.update({1: o, 2: o2})
        self.assertEqual({1: o, 2: o2}, d)
        self.assertNotEqual({1: o}, d)

