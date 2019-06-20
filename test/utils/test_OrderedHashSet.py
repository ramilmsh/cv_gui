from test.BaseTest import BaseTest

from src.utils.OrderedHashSet import OrderedHashSet


class OrderedHashSetTest(BaseTest):
    
    def setUp(self):
        pass

    def test_init(self):
        a = OrderedHashSet()
        self.assertIsInstance(a, OrderedHashSet, "should be an instance of ordered has set")

    def test_append(self):
        a = OrderedHashSet()
        a.append(1)
        a.append(2)
        a.append(3)

        self.assertEqual(len(a), 3, "should contain 3 elements")

    def test_order(self):
        a = OrderedHashSet()
        self.assertEqual(a.append(1), 0, "should return 0")
        self.assertEqual(a.append(2), 1, "should return 1")
        self.assertEqual(a.append(3), 2, "should return 2")
    
    def test_iteration(self):
        a = OrderedHashSet()
        a.append(1)
        a.append(2)
        a.append(3)
        c = 1
        for i in a:
            self.assertEqual(a[i], c)
            c += 1
        
        del a[0]
        c = 2
        for i in a:
            self.assertEqual(a[i], c)
            c += 1