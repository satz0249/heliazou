from tests.base import ApiDBTestCase

from zou.app.services import scenes_service


class SceneTestCase(ApiDBTestCase):
    def setUp(self):
        super(SceneTestCase, self).setUp()
        self.generate_shot_suite()
        self.project_id = str(self.project.id)
        self.serialized_shot = self.shot.serialize(obj_type="Shot")
        self.serialized_scene = self.scene.serialize(obj_type="Scene")
        self.scene_id = str(self.scene.id)
        self.serialized_sequence = self.sequence.serialize(obj_type="Sequence")
        self.sequence_id = str(self.sequence.id)
        self.generate_fixture_shot("S02")
        self.serialized_shot_02 = self.shot.serialize(obj_type="Shot")
        scene_02 = self.generate_fixture_scene("SC02")
        self.scene_02_id = str(scene_02.id)
        self.generate_fixture_scene("SC03")
        self.generate_fixture_scene("SC04")
        self.generate_assigned_task()

        self.generate_fixture_sequence("S02")
        self.generate_fixture_sequence("S03")
        self.generate_fixture_sequence("S04")

    def test_get_project_scenes(self):
        scenes = self.get("data/projects/%s/scenes" % self.project.id)
        self.assertEqual(len(scenes), 4)
        self.assertDictEqual(scenes[0], self.serialized_scene)
        self.get("data/projects/123/scenes", 404)

    def test_get_sequence_scenes(self):
        scenes = self.get("data/sequences/%s/scenes" % self.sequence_id)
        self.assertEqual(len(scenes), 4)
        self.assertDictEqual(scenes[0], self.serialized_scene)

    def test_get_scene(self):
        scene = self.get("data/scenes/%s" % self.scene.id)
        self.assertEqual(scene["id"], str(self.scene.id))
        self.assertEqual(scene["name"], self.scene.name)
        self.assertEqual(
            scene["sequence_name"], self.serialized_sequence["name"]
        )
        self.assertEqual(
            scene["sequence_id"], str(self.serialized_sequence["id"])
        )
        self.assertEqual(scene["episode_name"], self.episode.name)
        self.assertEqual(scene["episode_id"], str(self.episode.id))
        self.assertEqual(scene["project_name"], self.project.name)

    def test_get_scene_by_name(self):
        scenes = self.get("data/scenes/all?name=%s" % self.scene.name)
        self.assertEqual(scenes[0]["id"], str(self.scene.id))

    def test_create_scene(self):
        scene_name = "NSC01"
        project_id = str(self.project.id)
        sequence_id = str(self.sequence.id)
        data = {"name": scene_name, "sequence_id": sequence_id}
        scene = self.post("data/projects/%s/scenes" % project_id, data)
        scene = self.get("data/scenes/%s" % scene["id"])
        self.assertEqual(scene["name"], scene_name)
        self.assertEqual(scene["parent_id"], sequence_id)

    def test_get_remove_scene(self):
        self.get("data/scenes/%s" % self.scene.id, 200)
        self.delete("data/scenes/%s" % self.scene.id)
        self.get("data/scenes/%s" % self.scene.id, 404)

    def test_get_scene_tasks(self):
        self.generate_fixture_scene_task()
        tasks = self.get("data/scenes/%s/tasks" % self.scene.id)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], str(self.scene_task.id))

    def test_get_scene_task_types(self):
        self.generate_fixture_scene_task()
        task_type_id = str(self.scene_task.task_type_id)
        task_types = self.get("data/scenes/%s/task-types" % self.scene.id)
        self.assertEqual(len(task_types), 1)
        self.assertEqual(task_types[0]["id"], task_type_id)

    def test_get_scene_shots(self):
        scenes_service.add_shot_to_scene(
            self.serialized_scene, self.serialized_shot
        )
        scenes_service.add_shot_to_scene(
            self.serialized_scene, self.serialized_shot_02
        )
        shots = self.get("data/scenes/%s/shots" % self.serialized_scene["id"])
        self.assertEqual(len(shots), 2)
        self.assertEqual(shots[0]["id"], self.serialized_shot["id"])
        self.assertEqual(shots[1]["id"], self.serialized_shot_02["id"])

    def test_add_shot_to_scene(self):
        path = "data/scenes/%s/shots" % self.serialized_scene["id"]
        self.post(path, {"shot_id": self.serialized_shot["id"]})
        self.post(path, {"shot_id": self.serialized_shot_02["id"]})
        shots = self.get(path)
        self.assertEqual(len(shots), 2)
        self.assertEqual(shots[0]["id"], self.serialized_shot["id"])
        self.assertEqual(shots[1]["id"], self.serialized_shot_02["id"])

    def test_remove_shot_from_scene(self):
        scenes_service.add_shot_to_scene(
            self.serialized_scene, self.serialized_shot
        )
        scenes_service.add_shot_to_scene(
            self.serialized_scene, self.serialized_shot_02
        )
        self.delete(
            "data/scenes/%s/shots/%s"
            % (self.serialized_scene["id"], self.serialized_shot["id"])
        )
        shots = self.get("data/scenes/%s/shots" % self.serialized_scene["id"])
        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0]["id"], self.serialized_shot_02["id"])

    def test_get_scenes_by_project_and_name(self):
        self.get("data/scenes/all?project_id=undefined&name=SC01", 400)
        scenes = self.get(
            "data/scenes/all?project_id=%s&name=SC02" % self.project_id
        )
        self.assertEqual(scenes[0]["id"], str(self.scene_02_id))

        self.generate_fixture_user_cg_artist()
        self.log_in_cg_artist()
        scenes = self.get(
            "data/scenes/all?project_id=%s&name=SC01" % self.project_id, 403
        )
