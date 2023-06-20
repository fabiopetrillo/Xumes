from unittest import TestCase

from xumes.training_module.entity_manager import EntityObject, EntityListAdapter,EntityTupleAdapter, EntitySetAdapter, EntityDictAdapter



class TestObject(TestCase):

    def test_list_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        li = EntityListAdapter([o])
        li = li.update([o, o])
        self.assertEqual([o, o], li)

    def test_tuple_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        t = EntityTupleAdapter((0,))
        t = t.update((o, o))
        self.assertEqual((o, o), t)

    def test_set_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        o2 = EntityObject({"a": 2, "__type__": "Test"})
        s = EntitySetAdapter({o})
        s = s.update({o, o2})
        self.assertEqual({o, o2}, s)
        self.assertNotEqual({o}, s)

    def test_dict_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        o2 = EntityObject({"a": 2, "__type__": "Test"})
        d = EntityDictAdapter({1: o})
        d = d.update({1: o, 2: o2})
        self.assertEqual({1: o, 2: o2}, d)
        self.assertNotEqual({1: o}, d)

