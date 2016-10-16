import unittest
import networkx as nx
import planarity_test

def is_planar(g):
    return planarity_test.is_planar(g)


class PlanarityTestCase(unittest.TestCase):
    def test_one_node(self):
        g = nx.Graph()
        g.add_node(0)
        self.assertTrue(is_planar(g))

    def test_k_5(self):
        g = nx.complete_graph(5)
        self.assertFalse(is_planar(g))

    def test_k_3_3(self):
        g = nx.complete_bipartite_graph(3,3)
        self.assertFalse(is_planar(g))

    def test_k_n(self):
        for n in range(1,4):
            g = nx.complete_graph(n)
            self.assertTrue(is_planar(g))

        for n in range(5,10):
            g = nx.complete_graph(n)
            self.assertFalse(is_planar(g))

    def test_k_n_m(self):
        for n in range (2,6):
            for m in range(2,6):
                g = nx.complete_bipartite_graph(n,m)
                if n < 3 or m < 3:
                    self.assertTrue(is_planar(g))
                else:
                    self.assertFalse(is_planar(g))

    def test_almost_k_5(self):
        g = nx.complete_graph(5)
        g.remove_edge(0,1)
        self.assertTrue(is_planar(g))
        g.remove_edge(1,2)
        g.add_edge(1,5)
        g.add_edge(5,2)
        self.assertTrue(is_planar(g))

    def test_almost_k_3_3(self):
        g = nx.Graph()
        for i in range(0,3):  # make a complete bipartite graph with bipartitions {0,1,2} and {3,4,5}
            for j in range(3,6):
                g.add_edge(i,j)
        g.remove_edge(0,3)
        self.assertTrue(is_planar(g))
        g.add_edge(0, 6)
        g.add_edge(6, 2)
        self.assertTrue(is_planar(g))

    def test_wellknown_graphs(self):
        self.assertFalse(is_planar(nx.petersen_graph()))
        #self.assertTrue(is_planar(nx.tutte_graph())) #due to the fact that this is a very large graph which is planar, the algorithm needs waay too much time to compute its planarity
        self.assertTrue(is_planar(nx.complete_graph(4)))
        self.assertTrue(is_planar(nx.wheel_graph(7)))

if __name__ == '__main__':
    unittest.main()
