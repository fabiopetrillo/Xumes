from unittest import TestCase

from xumes.game_module.state_observable import GameStateObservable, State


class TestGameStateObservable(TestCase):

    # Test for build-in types
    def test_int(self):
        s = GameStateObservable(1, name="s")
        self.assertEqual(1, s.state().state)

    def test_float(self):
        s = GameStateObservable(1.0, name="s")
        self.assertEqual(1.0, s.state().state)

    def test_complex(self):
        s = GameStateObservable(1j, name="s")
        self.assertEqual(1j, s.state().state)

    def test_bool(self):
        s = GameStateObservable(True, name="s")
        self.assertEqual(True, s.state().state)

    def test_str(self):
        s = GameStateObservable("a", name="s")
        self.assertEqual("a", s.state().state)

    def test_list(self):
        s = GameStateObservable([1, 2], name="s")
        self.assertEqual([1, 2], s.state().state)

    def test_tuple(self):
        s = GameStateObservable((1, 2), name="s")
        self.assertEqual((1, 2), s.state().state)

    def test_dict(self):
        s = GameStateObservable({"a": 1}, name="s")
        self.assertEqual({"a": 1}, s.state().state)

    def test_set(self):
        s = GameStateObservable({1, 2}, name="s")
        self.assertEqual({1, 2}, s.state().state)

    def test_frozenset(self):
        s = GameStateObservable(frozenset({1, 2}), name="s")
        self.assertEqual(frozenset({1, 2}), s.state().state)

    def test_none(self):
        s = GameStateObservable(None, name="s")
        self.assertEqual(None, s.state().state)

    # Test for custom types

    def test_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = GameStateObservable([A(1), A(2)], name="s", state=["a"])
        self.assertEqual([{"a": 1, "__type__": "A"}, {"a": 2, "__type__": "A"}], s.state().state)

    def test_tuple_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = GameStateObservable((A(1), A(2)), name="s", state=["a"])
        self.assertEqual(({"a": 1, "__type__": "A"}, {"a": 2, "__type__": "A"}), s.state().state)

    def test_dict_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = GameStateObservable({"a": A(1), "b": A(2)}, name="s", state=["a"])
        self.assertEqual({"a": {"a": 1, "__type__": "A"}, "b": {"a": 2, "__type__": "A"}}, s.state().state)

    def test_obj_with_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_dict_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A({"a": B(1), "b": B(2)}), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({'__type__': 'A',
                          'a': {'a': {'__type__': 'B', 'b': 1}, 'b': {'__type__': 'B', 'b': 2}}},
                         s.state().state)

    def test_obj_with_tuple_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A((B(1), B(2))), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": ({"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}), "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = GameStateObservable(A(1), name="s", state=State(
            "a",
        ))
        self.assertEqual({"a": 1, "__type__": "A"}, s.state().state)
        s.a = 2
        self.assertEqual({"a": 2, "__type__": "A"}, s.state().state)

    def test_obj_with_attr_change_with_list(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = GameStateObservable(A([1, 2]), name="s", state=State(
            "a",
        ))
        self.assertEqual({"a": [1, 2], "__type__": "A"}, s.state().state)
        s.a = [3, 4]
        self.assertEqual({"a": [3, 4], "__type__": "A"}, s.state().state)

    def test_obj_with_attr_change_with_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a = [B(3), B(4)]
        self.assertEqual({"a": [{"b": 3, "__type__": "B"}, {"b": 4, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change_with_list_of_obj_with_attr_change(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a[0].b = 3
        self.assertEqual({"a": [{"b": 3, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change_with_list_of_obj_with_attr_change_with_list(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = GameStateObservable(A([B([1, 2]), B([3, 4])]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": [1, 2], "__type__": "B"}, {"b": [3, 4], "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a[0].b = [5, 6]
        self.assertEqual({"a": [{"b": [5, 6], "__type__": "B"}, {"b": [3, 4], "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_shortest_state(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, b):
                self.b = b

        class C:
            def __init__(self, c):
                self.c = c

        a = A(B(1), C(2))

        s = GameStateObservable(a, name="s", state=[State("b"), State("c")])
        f = s._find_state([State("b")])
        self.assertEqual([State("b")], f)

    def test_shortest_state2(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("d"), State("e")])
        self.assertEqual([State("b", [State("d"), State("e")])], f)

    def test_shortest_state2_1(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("b", ["d", "e"])])
        self.assertEqual([State("b", [State("d"), State("e")])], f)

    def test_shortest_state3(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("b", ["d", "e"]), State("c")])
        self.assertEqual([State("b", ["d", "e"]), State("c")], f)

    def test_shortest_state4(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("e")])
        self.assertEqual([State("b", ["e"])], f)

    def test_shortest_state5(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("c")])
        self.assertEqual([State("c")], f)

    def test_shortest_state6(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]), State("c")])
        f = s._find_state([State("f")])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state7(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]), State("c")])
        f = s._find_state([State("e", State("f"))])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state8(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]),
                                                    State("c", ["d", State("e", State("f"))])])
        f = s._find_state([State("d")])
        self.assertEqual([State("b", ["d"]), State("c", ["d"])], f)

    def test_shortest_state9(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]),
                                                    State("c", ["d", State("e", State("f"))])])
        f = s._find_state([State("e", State("f"))])
        self.assertEqual([State("b", State("e", State("f"))), State("c", State("e", State("f")))], f)

    def test_shortest_state10(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("d")])
        self.assertEqual([State("b", "d"), State("c", State("e", State("d")))], f)

    def test_shortest_state11(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("e", State("d"))])
        self.assertEqual([State("c", State("e", State("d")))], f)

    def test_shortest_state12(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("f")])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state_error(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_error2(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c
        a = A(1, 2)
        s = GameStateObservable(a, name="s",
                                state=None)
        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_error3(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c
        a = A(1, 2)
        s = GameStateObservable(a, name="s",
                                state=["b", State("c", attributes=None)])

        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_no_ends(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c
        a = A(1, 2)
        s = GameStateObservable(a, name="s",
                                state=["b", State("c", attributes=None)])

        self.assertEquals(s._state, s._find_state([]))

    def test_game_state_observable(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"), methods_to_observe="test2")]), State("c",
                                                                                                                    [
                                                                                                                        State(
                                                                                                                            "e",
                                                                                                                            State(
                                                                                                                                "d",
                                                                                                                                methods_to_observe="test1"),
                                                                                                                            methods_to_observe="test2")])])
        self.assertEqual(
            {"test1": [State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])],
             "test2": [State("b", [State("e", State("f"), methods_to_observe="test2")]),
                       State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])]},
            s._methods_to_observe)

    def test_game_state_observable2(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c
                self.d = 5

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e
                self.f = 6

        class C:
            def __init__(self, c):
                self.c = c
                self.d = 7

        class D:
            def __init__(self, d):
                self.d = d
                self.e = 8

        class E:
            def __init__(self, e):
                self.e = e
                self.f = 9

        a = A(B(D(1), E(2)), C(3))
        s = GameStateObservable(a, name="s",
                                state=[State("b", ["d", State("e", State("f"), methods_to_observe="test2")]), State("c",
                                                                                                                    [
                                                                                                                        State(
                                                                                                                            "e",
                                                                                                                            State(
                                                                                                                                "d",
                                                                                                                                methods_to_observe="test1"),
                                                                                                                            methods_to_observe="test2")])])
        self.assertEqual(
            {"test1": [State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])],
             "test2": [State("b", [State("e", State("f"), methods_to_observe="test2")]),
                       State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])]},
            s._methods_to_observe)
