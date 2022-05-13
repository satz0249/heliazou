from tests.base import ApiDBTestCase


class AssetInstanceInShotTestCase(ApiDBTestCase):
    def setUp(self):
        super(AssetInstanceInShotTestCase, self).setUp()

        self.generate_shot_suite()
        self.generate_fixture_asset()
        self.generate_fixture_asset_types()
        self.generate_fixture_asset_character()
        self.scene_id = str(self.scene.id)
        self.shot_id = str(self.shot.id)
        self.asset_id = str(self.asset.id)
        self.asset_name = str(self.asset.name)
        self.asset_type_name = str(self.asset_type.name)
        self.asset_character_id = str(self.asset_character.id)

        self.generate_fixture_asset_character("Lama")
        self.asset_character_2_id = str(self.asset_character.id)

    def new_instance(self, target_type, target_id, asset_id):
        data = {"asset_id": asset_id}
        return self.post(
            "/data/%s/%s/asset-instances" % (target_type, target_id), data
        )

    def new_scene_asset_instance(self, scene_id, asset_id):
        data = {"asset_id": asset_id}
        return self.post("/data/scenes/%s/asset-instances" % scene_id, data)

    def new_shot_asset_instance(self, shot_id, asset_instance_id):
        data = {"asset_instance_id": asset_instance_id}
        return self.post("/data/shots/%s/asset-instances" % shot_id, data)

    def new_asset_asset_instance(self, asset_id, asset_to_instantiate_id):
        data = {"asset_to_instantiate_id": asset_to_instantiate_id}
        return self.post(
            "/data/assets/%s/asset-asset-instances" % asset_id, data
        )

    def test_add_instance_to_scene(self):
        instances = self.get("/data/scenes/%s/asset-instances" % self.scene_id)
        self.assertEqual(instances, {})
        self.new_scene_asset_instance(self.scene.id, self.asset_id)
        self.new_scene_asset_instance(self.scene.id, self.asset_id)
        self.new_scene_asset_instance(self.scene.id, self.asset_character_id)

        instances = self.get("/data/scenes/%s/asset-instances" % self.scene_id)
        self.assertEqual(len(instances[self.asset_id]), 2)
        self.assertEqual(len(instances[self.asset_character_id]), 1)
        self.assertEqual(instances[self.asset_id][0]["number"], 1)
        self.assertEqual(instances[self.asset_id][1]["number"], 2)
        self.assertEqual(instances[self.asset_id][1]["name"], "Tree_0002")
        self.assertEqual(instances[self.asset_character_id][0]["number"], 1)

    def test_get_scene_asset_instances_for_asset(self):
        instances = self.get(
            "/data/assets/%s/scene-asset-instances" % self.asset_id
        )
        self.assertEqual(instances, {})
        self.new_scene_asset_instance(self.scene_id, self.asset_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_character_id)

        instances = self.get(
            "/data/assets/%s/scene-asset-instances" % self.asset_id
        )
        self.assertEqual(len(instances[self.scene_id]), 2)

    def test_get_scene_camera_instances_for_asset(self):
        self.generate_fixture_asset_camera()
        self.asset_camera_id = self.asset_camera.id
        instances = self.get(
            "/data/scenes/%s/camera-instances" % self.scene_id
        )
        self.assertEqual(instances, {})
        self.new_scene_asset_instance(self.scene_id, self.asset_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_character_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_camera_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_camera_id)
        self.new_scene_asset_instance(self.scene_id, self.asset_camera_id)
        instances = self.get(
            "/data/scenes/%s/camera-instances" % self.scene_id
        )
        self.assertEqual(len(instances[str(self.asset_camera_id)]), 3)
        self.assertTrue(self.asset_id not in instances)

    def test_add_instance_to_shot(self):
        instances = self.get("/data/shots/%s/asset-instances" % self.shot_id)
        self.assertEqual(instances, {})

        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])
        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])
        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_character_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])

        instances = self.get("/data/shots/%s/asset-instances" % self.shot_id)
        self.assertEqual(len(instances[self.asset_id]), 2)
        self.assertEqual(len(instances[self.asset_character_id]), 1)
        self.assertEqual(instances[self.asset_id][0]["number"], 1)
        self.assertEqual(instances[self.asset_id][1]["number"], 2)
        self.assertEqual(instances[self.asset_id][1]["name"], "Tree_0002")
        self.assertEqual(instances[self.asset_character_id][0]["number"], 1)

        self.delete(
            "/data/shots/%s/asset-instances/%s"
            % (self.shot_id, asset_instance["id"])
        )
        instances = self.get("/data/shots/%s/asset-instances" % self.shot_id)
        self.assertTrue(self.asset_character_id not in instances)

    def test_get_shot_asset_instances_for_asset(self):
        instances = self.get(
            "/data/assets/%s/shot-asset-instances" % self.asset_id
        )
        self.assertEqual(instances, {})
        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])
        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])
        asset_instance = self.new_scene_asset_instance(
            self.scene_id, self.asset_character_id
        )
        self.new_shot_asset_instance(self.shot_id, asset_instance["id"])

        instances = self.get(
            "/data/assets/%s/shot-asset-instances" % self.asset_id
        )
        self.assertEqual(len(instances[self.shot_id]), 2)

    def test_get_asset_asset_instances_for_asset(self):
        instances = self.get(
            "/data/assets/%s/asset-asset-instances" % self.asset_id
        )
        self.assertEqual(instances, {})

        self.new_asset_asset_instance(self.asset_id, self.asset_character_id)
        self.new_asset_asset_instance(self.asset_id, self.asset_character_id)
        self.new_asset_asset_instance(self.asset_id, self.asset_character_2_id)

        instances = self.get(
            "/data/assets/%s/asset-asset-instances" % self.asset_id
        )
        self.assertEqual(len(instances[self.asset_character_id]), 2)
        self.assertEqual(len(instances[self.asset_character_2_id]), 1)
        self.assertEqual(instances[self.asset_character_id][0]["number"], 1)
        self.assertEqual(instances[self.asset_character_id][1]["number"], 2)
        self.assertEqual(
            instances[self.asset_character_id][1]["name"], "Rabbit_0002"
        )
        self.assertEqual(instances[self.asset_character_2_id][0]["number"], 1)
