from test.BaseTest import BaseTest

from src.camera.BaseCamera import BaseCamera


class BaseCameraTest(BaseTest):
    
    def setUp(self):
        pass

    def test_generic_name_assignment(self):
        self.assertEqual(BaseCamera().name, "GenericCamera")
    
    def test_provided_name_assignment(self):
        self.assertEqual(BaseCamera("name").name, "name")
