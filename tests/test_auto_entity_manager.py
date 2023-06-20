from unittest import TestCase

from xumes.training_module import JsonGameElementStateConverter
from xumes.training_module.entity_manager import AutoEntityManager


class TestAutoEntityManager(TestCase):

    def test_bool(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", True))
        self.assertTrue(entity_manager.a)

    def test_int(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", 1))
        self.assertEqual(entity_manager.a, 1)

    def test_float(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", 1.0))
        self.assertEqual(entity_manager.a, 1.0)

    def test_complex(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", 1+1j))
        self.assertEqual(entity_manager.a, 1+1j)

    def test_str(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", "a"))
        self.assertEqual(entity_manager.a, "a")

    def test_list(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", [1, 2, 3]))
        self.assertEqual(entity_manager.a, [1, 2, 3])

    def test_tuple(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", (1, 2, 3)))
        self.assertEqual(entity_manager.a, (1, 2, 3))

    def test_set(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", {1, 2, 3}))
        self.assertEqual(entity_manager.a, {1, 2, 3})

    def test_dict(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", {1: 1, 2: 2, 3: 3}))
        self.assertEqual(entity_manager.a, {1: 1, 2: 2, 3: 3})

    def test_list_of_list(self):
        entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        entity_manager.convert(("a", [[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(entity_manager.a, [[1, 2, 3], [4, 5, 6]])

