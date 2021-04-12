from unittest import TestCase
from laterna_magica.nodes import MetaBuilder, DataType, Node
from .helper import PassthroughNode


class NodeTest(TestCase):

    def test_initial_outputs_creation(self):
        meta = MetaBuilder()\
            .with_output(DataType.STRING)\
            .with_output(DataType.FLOAT)\
            .build()

        node = Node(meta)

        self.assertEqual(len(node.outputs), 2)
        self.assertEqual(node.outputs[0].data_type, DataType.STRING)
        self.assertEqual(node.outputs[1].data_type, DataType.FLOAT)

    def test_nodes_observe_each_other(self):
        node_1 = PassthroughNode()
        node_2 = PassthroughNode()
        node_2.attach_to(node_1.outputs[0], 0)

        node_1.inputs[0].value = 0.5
        node_1.inputs[0].value = 8

        self.assertListEqual(node_2.results, [(0, 0.5), (0, 8)])
