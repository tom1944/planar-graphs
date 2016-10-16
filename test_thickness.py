import unittest
import networkx as nx
import thickness


class ThicknessTestCase(unittest.TestCase):
    def test_one_node(self):
        g = nx.Graph()
        g.add_node(0)
        self.assertEqual(thickness.thickness(g),1)

    def test_k_5(self):
        g = nx.complete_graph(5)
        self.assertEqual(thickness.thickness(g),2)

    def test_k_3_3(self):
        g = nx.complete_bipartite_graph(3,3)
        self.assertEqual(thickness.thickness(g),2)

    def test_k_n(self):
        self.assertEqual(thickness.thickness(nx.complete_graph(4)), 1)  # see https://en.wikipedia.org/wiki/Thickness_(graph_theory) , first formula
        self.assertEqual(thickness.thickness(nx.complete_graph(6)), 2)
        self.assertEqual(thickness.thickness(nx.complete_graph(8)), 2)
        self.assertEqual(thickness.thickness(nx.complete_graph(9)), 3)
        self.assertEqual(thickness.thickness(nx.complete_graph(10)), 3)

    # def test_k_n_m(self):
    #     for n in range (2,6):
    #         for m in range(2,6):
    #             g = nx.complete_bipartite_graph(n,m)
    #             if n < 3 or m < 3:
    #                 self.assertEqual(is_planar(g))
    #             else:
    #                 self.assertEqual(is_planar(g))

    def test_almost_k_5(self):
        g = nx.complete_graph(5)
        g.remove_edge(0,1)
        self.assertEqual(thickness.thickness(g), 1)
        g.remove_edge(1,2)
        g.add_edge(1,5)
        g.add_edge(5,2)
        self.assertEqual(thickness.thickness(g), 1)

    def test_almost_k_3_3(self):
        g = nx.Graph()
        for i in range(0,3):  # make a complete bipartite graph with bipartitions {0,1,2} and {3,4,5}
            for j in range(3,6):
                g.add_edge(i,j)
        g.remove_edge(0,3)
        self.assertEqual(thickness.thickness(g), 1)
        g.add_edge(0, 6)
        g.add_edge(6, 2)
        self.assertEqual(thickness.thickness(g), 1)

    def test_wellknown_graphs(self):
        self.assertEqual(thickness.thickness(nx.petersen_graph()), 2)
        # self.assertEqual(is_planar(nx.tutte_graph()))  takes to long
        self.assertEqual(thickness.thickness(nx.wheel_graph(7)), 1)


if __name__ == '__main__':
    unittest.main()
