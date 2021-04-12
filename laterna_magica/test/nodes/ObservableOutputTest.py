from unittest import TestCase
from laterna_magica.nodes import ObservableOutput, DataType
from .helper import TestObserver


class ObservableOutputTest(TestCase):

    def test_output_can_be_observed(self):
        output = ObservableOutput(DataType.FLOAT)
        test_observer = TestObserver()
        output.register(test_observer)

        output.value = 5
        output.value = 7

        self.assertListEqual(test_observer.results, [(output, 5), (output, 7)])

    def test_register_and_unregister_observers(self):
        output = ObservableOutput(DataType.STRING)
        test_observer_1 = TestObserver()
        test_observer_2 = TestObserver()
        output.register(test_observer_1)
        output.register(test_observer_2)

        output.value = 'abc'
        output.unregister(test_observer_1)
        output.value = 'test'

        self.assertListEqual(test_observer_1.results, [(output, 'abc')])
        self.assertListEqual(test_observer_2.results, [(output, 'abc'), (output, 'test')])

