from fiberspot import example_script
import fiberspot
import numpy as np


class Test_Core:
    def test_execute_example(self,):
        arguments = example_script.arguments
        result = fiberspot.get_local_fiber_volume_content(arguments=arguments)

        box = arguments["specimen"]["box"]
        box_shape = (box[3] - box[1], box[2] - box[0])
        for fvc_key, fvc in result["fiber_volume_content"].items():
            assert np.allclose(fvc.shape, box_shape)
