from test.BaseTest import BaseTest

from src.camera.AbstractCamera import AbstractCamera


class AbstractCameraTest(BaseTest):
    
    def setUp(self):
        pass

    def test_generic_name_assignment(self):
        self.assertEqual(AbstractCamera().name, "GenericCamera")
    
    def test_provided_name_assignment(self):
        self.assertEqual(AbstractCamera("name").name, "name")
