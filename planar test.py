import unittest
import networkx as nx


# a stub, needs to be implemented, possibly in another file/module/unit
def is_planar(g):
    return False


class PlanarTestCase(unittest.TestCase):
    def test_one_node(self):
        g = nx.Graph()
        g.add_node(0)
        self.assertTrue(is_planar(g))

    def test_k5(self):
        g = nx.complete_graph(5)
        self.assertFalse(is_planar(g))

    def test_k3_3(self):
        g = nx.complete_bipartite_graph(3,3)
        self.assertFalse(is_planar(g))

    def test_kn(self):
        for n in range(1,4):
            g = nx.complete_graph(n)
            self.assertTrue(is_planar(g))

        for n in range(5,10):
            g = nx.complete_graph(n)
            self.assertFalse(is_planar(g))

    def test_k_n_m(self):
        for n in range (2,5):
            for m in range(2,5)
                if n > 3 or m > 3:
                    self.assertTrue(is_planar(g))
                else:
                    self.assertFalse(is_planar(g))




if __name__ == '__main__':
    unittest.main()
