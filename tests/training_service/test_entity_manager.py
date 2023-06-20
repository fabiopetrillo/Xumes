from unittest import TestCase

from xumes.training_module import JsonGameElementStateConverter
from xumes.training_module.entity_manager import AutoEntityObject, AutoEntityManager, Object, choose_delegate, \
    AutoEntityInt


class TestState(TestCase):

    def test_get_attr(self):
        s = AutoEntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b.c, 2)

    def test_set_attr(self):
        s = AutoEntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        s.a = 2
        s.b.c = 3
        self.assertEqual(s.a, 2)
        self.assertEqual(s.b.c, 3)

    def test_set_attr2(self):
        s = AutoEntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        s.a = 2
        s.b = 3
        self.assertEqual(s.a, 2)
        self.assertEqual(s.b, 3)

    def test_bool(self):
        s = AutoEntityObject.build({"a": True, "b": {"c": False, "__type__": "Test2"}, "__type__": "Test"})
        self.assertTrue(s.a)
        self.assertFalse(s.b.c)

    def test_int(self):
        s = AutoEntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b.c, 2)

    def test_float(self):
        s = AutoEntityObject.build({"a": 1.1, "b": {"c": 2.2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1.1)
        self.assertEqual(s.b.c, 2.2)

    def test_complex(self):
        s = AutoEntityObject.build({"a": 1j, "b": {"c": 2j, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1j)
        self.assertEqual(s.b.c, 2j)

    def test_list(self):
        s = AutoEntityObject.build({"a": 1, "b": [1, 2, 3], "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, [1, 2, 3])

    def test_tuple(self):
        s = AutoEntityObject.build({"a": 1, "b": (1, 2, 3), "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, (1, 2, 3))

    def test_str(self):
        s = AutoEntityObject.build({"a": 1, "b": "abc", "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, "abc")

    def test_set(self):
        s = AutoEntityObject.build({"a": 1, "b": {1, 2, 3}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, {1, 2, 3})

    def test_dict(self):
        s = AutoEntityObject.build({"a": 1, "b": {"a": 1, "b": 2}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, {"a": 1, "b": 2})

    def test_no_object_int(self):
        s = AutoEntityInt.build(1)
        self.assertEqual(s, 1)

    def test_no_object_entity_manager(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test", 1))
        self.assertEqual(entity_manager.test, 1)

    def test_entity_manager(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.a, 1)

    def test_entity_manager2(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b.c, 2)

    def test_entity_manager5_dict_inside(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(
            ("test1", {"a": 1, "b": {"c": {"d": 2, "e": 3}, "__type__": "Test3"}, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b.c["e"], 3)

    def test_entity_manager6_list_inside(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": [1, 2, 3], "__type__": "Test3"}, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b.c[2], 3)

    def test_entity_manager8_not_found(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": [1, 2, 3], "__type__": "Test3"}, "__type__": "Test"}))
        self.assertRaises(AttributeError, lambda: entity_manager.test1.c)

    def test_entity_manager9(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(
            ("test1", {"a": 1, "b": {"c": [{"e": 1, "__type__": "Test4"}], "__type__": "Test3"}, "__type__": "Test"}))
        self.assertEqual(1, entity_manager.test1.b.c[0].e)

    def test_append(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [1, 2, 3], "__type__": "Test"}))
        entity_manager.test1.b.append(4)
        self.assertEqual(entity_manager.test1.b, [1, 2, 3, 4])

    def test_insert(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [1, 2, 3], "__type__": "Test"}))
        entity_manager.test1.b.insert(0, 4)
        self.assertEqual(entity_manager.test1.b, [4, 1, 2, 3])

    def test_pop(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [1, 2, 3], "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b.pop(), 3)
        self.assertEqual(entity_manager.test1.b, [1, 2])

    def test_remove(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [1, 2, 3], "__type__": "Test"}))
        entity_manager.test1.b.remove(2)
        self.assertEqual(entity_manager.test1.b, [1, 3])

    def test_clear(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [1, 2, 3], "__type__": "Test"}))
        entity_manager.test1.b.clear()
        self.assertEqual(entity_manager.test1.b, [])

    def test_add(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 1, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b + 1, 2)

    def test_sub(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 1, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b - 1, 0)

    def test_mul(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 2, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b * 2, 4)

    def test_truediv(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 4, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b / 2, 2)

    def test_floordiv(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b // 2, 2)

    def test_mod(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.b % 2, 1)

    def test_add_state_composite(self):
        s = choose_delegate(1)
        self.assertEqual(s + 1, 2)

    def test_update_delegate(self):
        s = choose_delegate(1)
        s = s.update(2)
        self.assertEqual(s, 2)

    def test_update_object(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        entity_manager.test1.update({"b": 6})
        self.assertEqual(entity_manager.test1.b, 6)

    def test_update_object2(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        entity_manager.test1.update({"c": 6})
        self.assertEqual(entity_manager.test1.c, 6)

    def test_update_object3(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        entity_manager.test1.update({"b": 6, "c": 7})
        self.assertEqual(entity_manager.test1.b, 6)
        self.assertEqual(entity_manager.test1.c, 7)

    def test_update_object4(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": 5, "__type__": "Test"}))
        entity_manager.test1.update({"b": 6, "c": 7})
        self.assertEqual(entity_manager.test1.b, 6)
        self.assertEqual(entity_manager.test1.c, 7)

    def test_update_object6(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 5}, "__type__": "Test"}))
        entity_manager.test1.b.update({"c": 6})
        self.assertEqual(entity_manager.test1.b["c"], 6)

    def test_update_object7(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 5, "__type__": "Test2"}, "__type__": "Test"}))
        a = entity_manager.test1.b
        entity_manager.test1.b.update({"c": 6, "__type__": "Test2"})
        self.assertEqual(a.c, 6)

    def test_comm_update_object(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 5, "__type__": "Test2"}, "__type__": "Test"}))
        entity_manager.convert(("test1", {"a": 1, "__type__": "Test"}))
        c = entity_manager.test1.b.c
        self.assertEqual(entity_manager.test1.a, 1)
        self.assertEqual(c, 5)

    def test_comm_update_object2(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": {"c": 5, "__type__": "Test2"}, "__type__": "Test"}))
        b = entity_manager.test1.b
        entity_manager.convert(("test1", {"b": {"c": 6, "__type__": "Test2"}, "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.a, 1)
        self.assertEqual(b.c, 6)

    def test_comm_update_object3(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("test1", {"a": 1, "b": [], "__type__": "Test"}))
        b = entity_manager.test1.b
        entity_manager.convert(("test1", {"b": [1, 2, 3], "__type__": "Test"}))
        self.assertEqual(entity_manager.test1.a, 1)
        self.assertEqual(b, [1, 2, 3])

