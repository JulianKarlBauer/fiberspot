from fiberspot import example_script
import fiberspot


class Test_Core:
    def test_execute_example(self,):
        fiberspot.get_local_fiber_volume_content(arguments=example_script.arguments)
