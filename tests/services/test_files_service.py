import pytest

from tests.base import ApiDBTestCase

from zou.app import app
from zou.app.services import files_service, preview_files_service
from zou.app.models.software import Software
from zou.app.services.exception import (
    EntryAlreadyExistsException,
    OutputFileNotFoundException,
    PreviewFileNotFoundException,
    SoftwareNotFoundException,
    WorkingFileNotFoundException,
)


class FileServiceTestCase(ApiDBTestCase):
    def setUp(self):
        super(FileServiceTestCase, self).setUp()

        self.generate_fixture_project_status()
        self.generate_fixture_project()
        self.generate_fixture_asset_type()
        self.generate_fixture_asset()
        self.generate_fixture_sequence()
        self.generate_fixture_shot()
        self.generate_fixture_department()
        self.generate_fixture_task_type()
        self.generate_fixture_task_status()
        self.generate_fixture_task_status_wip()
        self.generate_fixture_task_status_to_review()
        self.generate_fixture_person()
        self.generate_fixture_assigner()
        self.generate_fixture_task()
        self.generate_fixture_shot_task()
        self.generate_fixture_file_status()
        self.generate_fixture_software()
        self.generate_fixture_working_file()
        self.generate_fixture_output_type()
        self.generate_fixture_output_file()

    def test_get_default_status(self):
        file_status = files_service.get_default_status()
        self.assertEqual(
            file_status["name"], app.config["DEFAULT_FILE_STATUS"]
        )

    def test_get_working_file(self):
        working_file = files_service.get_working_file(self.working_file.id)
        self.assertEqual(working_file["id"], str(self.working_file.id))
        self.assertRaises(
            WorkingFileNotFoundException,
            files_service.get_working_file,
            "unknown",
        )

    def test_get_output_file(self):
        output_file = files_service.get_output_file(self.output_file.id)
        self.assertEqual(output_file["id"], str(self.output_file.id))
        self.assertRaises(
            OutputFileNotFoundException,
            files_service.get_output_file,
            "unknown",
        )

    def test_get_software(self):
        software = files_service.get_software(self.software.id)
        self.assertEqual(software["id"], str(self.software.id))
        self.assertRaises(
            SoftwareNotFoundException, files_service.get_software, "unknown"
        )

    def test_get_or_create_software(self):
        self.assertIsNone(Software.get_by(name="Maya"))
        software = files_service.get_or_create_software("Maya", "may", ".ma")
        self.assertIsNotNone(Software.get_by(name="Maya"))
        software_again = files_service.get_or_create_software(
            "Maya", "may", ".ma"
        )
        self.assertEqual(software["id"], software_again["id"])

    def test_get_working_files_for_task(self):
        self.generate_fixture_working_file(name="main", revision=2)
        self.generate_fixture_working_file(name="main", revision=3)
        self.generate_fixture_working_file(name="main", revision=4)
        self.generate_fixture_working_file(name="main", revision=5)
        working_files = files_service.get_working_files_for_task(self.task.id)
        self.assertEqual(len(working_files), 5)
        self.assertEqual(working_files[0]["revision"], 5)

    def test_get_last_working_files_for_task(self):
        self.generate_fixture_working_file(name="main", revision=2)
        self.generate_fixture_working_file(name="main", revision=3)
        self.generate_fixture_working_file(name="main", revision=4)
        self.generate_fixture_working_file(name="main", revision=5)
        self.generate_fixture_working_file(name="hotfix", revision=1)
        self.generate_fixture_working_file(name="hotfix", revision=2)
        self.generate_fixture_working_file(name="hotfix", revision=3)
        working_files = files_service.get_last_working_files_for_task(
            self.task.id
        )
        self.assertEqual(working_files["main"]["revision"], 5)
        self.assertEqual(working_files["hotfix"]["revision"], 3)

    def get_next_working_revision(self):
        self.generate_fixture_working_file(name="main", revision=2)
        self.generate_fixture_working_file(name="main", revision=3)
        self.generate_fixture_working_file(name="main", revision=4)
        self.generate_fixture_working_file(name="main", revision=5)
        revision = files_service.get_next_working_revision(
            self.task.id, "main"
        )
        self.assertEqual(revision)

    def test_create_new_working_revision(self):
        self.working_file.delete()
        working_file = files_service.create_new_working_revision(
            self.task.id, self.person.id, self.software.id, "main", "/path"
        )
        self.assertEqual(working_file["revision"], 1)
        working_files = files_service.get_working_files_for_task(self.task.id)
        working_file = files_service.create_new_working_revision(
            self.task.id, self.person.id, self.software.id, "main", "/path"
        )
        working_files = files_service.get_working_files_for_task(self.task.id)
        self.assertEqual(working_file["revision"], 2)
        self.assertEqual(len(working_files), 2)

        with pytest.raises(EntryAlreadyExistsException):
            working_file = files_service.create_new_working_revision(
                self.task.id,
                self.person.id,
                self.software.id,
                "main",
                "/path",
                revision=2,
            )

    def test_get_next_output_file_revision(self):
        revision = files_service.get_next_output_file_revision(
            self.asset.id, self.output_type.id, self.task_type.id
        )

        self.assertEqual(revision, 2)

    def test_create_new_output_revision(self):
        self.output_file.delete()
        output_file = files_service.create_new_output_revision(
            self.asset.id,
            self.working_file.id,
            self.output_type.id,
            self.person.id,
            self.task_type.id,
        )
        self.assertEqual(output_file["revision"], 1)
        output_file = files_service.create_new_output_revision(
            self.asset.id,
            self.working_file.id,
            self.output_type.id,
            self.person.id,
            self.task_type.id,
        )
        self.assertEqual(output_file["revision"], 2)
        output_file = files_service.get_last_output_revision(
            self.asset.id, self.output_type.id, self.task_type.id
        )
        self.assertEqual(output_file["revision"], 2)

        with pytest.raises(EntryAlreadyExistsException):
            output_file = files_service.create_new_output_revision(
                self.asset.id,
                self.working_file.id,
                self.output_type.id,
                self.person.id,
                self.task_type.id,
                revision=1,
            )

    def test_get_last_output_files_for_entity(self):
        geometry = self.output_type
        cache = self.generate_fixture_output_type(
            name="Cache", short_name="cch"
        )

        self.generate_fixture_output_file(geometry, 2)
        self.generate_fixture_output_file(geometry, 3)
        self.generate_fixture_output_file(geometry, 4)
        geometry_file = self.generate_fixture_output_file(geometry, 5)
        self.generate_fixture_output_file(cache, 1)
        self.generate_fixture_output_file(cache, 2)
        cache_file = self.generate_fixture_output_file(cache, 3)

        last_output_files = files_service.get_last_output_files_for_entity(
            self.asset.id
        )

        # test last geometry file revision
        last_file = [
            f
            for f in last_output_files
            if (
                f["output_type_id"] == str(geometry.id)
                and f["name"] == geometry_file.name
            )
        ][0]
        self.assertEqual(last_file["revision"], 5)

        # test last cache file revision
        last_file = [
            f
            for f in last_output_files
            if (
                f["output_type_id"] == str(cache.id)
                and f["name"] == cache_file.name
            )
        ][0]
        self.assertEqual(last_file["revision"], 3)

    def test_get_output_files_for_output_type_and_entity(self):
        geometry = self.output_type
        self.generate_fixture_output_file(geometry, 1, representation="obj")
        self.generate_fixture_output_file(geometry, 2, representation="obj")
        self.generate_fixture_output_file(geometry, 3, representation="obj")
        self.generate_fixture_output_file(geometry, 4, representation="obj")

        self.generate_fixture_output_file(geometry, 1, representation="max")
        self.generate_fixture_output_file(geometry, 2, representation="max")
        self.generate_fixture_output_file(geometry, 3, representation="max")

        output_files = (
            files_service.get_output_files_for_output_type_and_entity(
                self.asset.id, geometry.id
            )
        )
        self.assertEqual(len(output_files), 8)

        output_files = (
            files_service.get_output_files_for_output_type_and_entity(
                str(self.asset.id), geometry.id, representation="obj"
            )
        )
        self.assertEqual(len(output_files), 4)

        output_files = (
            files_service.get_output_files_for_output_type_and_entity(
                str(self.asset.id), geometry.id, representation="max"
            )
        )
        self.assertEqual(len(output_files), 3)

    def test_get_output_files_for_output_type_and_scene_asset_instance(self):
        self.generate_fixture_asset()
        self.generate_fixture_scene()
        scene_id = str(self.scene.id)
        asset_instance = self.generate_fixture_scene_asset_instance()
        geometry = self.output_type
        self.generate_fixture_output_file(
            geometry,
            1,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )
        self.generate_fixture_output_file(
            geometry,
            4,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )

        self.generate_fixture_output_file(
            geometry,
            1,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=scene_id,
        )

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, scene_id, geometry.id
            )
        )
        self.assertEqual(len(output_files), 7)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, scene_id, geometry.id, representation="obj"
            )
        )
        self.assertEqual(len(output_files), 4)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, scene_id, geometry.id, representation="max"
            )
        )
        self.assertEqual(len(output_files), 3)

    def test_get_output_files_for_output_type_and_shot_asset_instance(self):
        self.generate_fixture_asset()
        self.generate_fixture_scene()

        scene_id = str(self.scene.id)
        shot_id = str(self.shot.id)
        asset_instance = self.generate_fixture_scene_asset_instance()
        self.generate_fixture_shot_asset_instance(
            self.shot, self.asset_instance
        )
        geometry = self.output_type
        self.generate_fixture_output_file(
            geometry,
            1,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )
        self.generate_fixture_output_file(
            geometry,
            4,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )

        self.generate_fixture_output_file(
            geometry,
            1,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=shot_id,
        )

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, shot_id, geometry.id
            )
        )
        self.assertEqual(len(output_files), 7)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, shot_id, geometry.id, representation="obj"
            )
        )
        self.assertEqual(len(output_files), 4)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, shot_id, geometry.id, representation="max"
            )
        )
        self.assertEqual(len(output_files), 3)

    def test_get_output_files_for_output_type_and_asset_asset_instance(self):
        self.generate_fixture_asset_types()
        self.generate_fixture_asset()
        self.generate_fixture_asset_character()
        asset_character_id = str(self.asset_character.id)
        asset_instance = self.generate_fixture_asset_asset_instance()
        geometry = self.output_type
        self.generate_fixture_output_file(
            geometry,
            1,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )
        self.generate_fixture_output_file(
            geometry,
            4,
            representation="obj",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )

        self.generate_fixture_output_file(
            geometry,
            1,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )
        self.generate_fixture_output_file(
            geometry,
            2,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )
        self.generate_fixture_output_file(
            geometry,
            3,
            representation="max",
            asset_instance=asset_instance,
            temporal_entity_id=asset_character_id,
        )

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id, asset_character_id, geometry.id
            )
        )
        self.assertEqual(len(output_files), 7)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id,
                asset_character_id,
                geometry.id,
                representation="obj",
            )
        )
        self.assertEqual(len(output_files), 4)

        output_files = (
            files_service.get_output_files_for_output_type_and_asset_instance(
                asset_instance.id,
                asset_character_id,
                geometry.id,
                representation="max",
            )
        )
        self.assertEqual(len(output_files), 3)

    def test_get_project_from_preview_file(self):
        project_id = str(self.project.id)
        self.generate_fixture_preview_file()
        project = preview_files_service.get_project_from_preview_file(
            self.preview_file.id
        )
        self.assertEqual(project["id"], project_id)

    def test_remove_preview_file(self):
        self.generate_fixture_preview_file()
        preview_file_id = self.preview_file.id
        files_service.remove_preview_file(preview_file_id)
        self.assertRaises(
            PreviewFileNotFoundException,
            files_service.get_preview_file,
            preview_file_id,
        )

    def test_get_preview_files_for_project(self):
        project_id = str(self.project.id)
        self.generate_fixture_project_standard()
        project_2_id = str(self.project_standard.id)
        self.generate_fixture_preview_file()
        preview_files = files_service.get_preview_files_for_project(project_id)
        self.assertEqual(len(preview_files), 1)
        preview_files = files_service.get_preview_files_for_project(
            project_2_id
        )
        self.assertEqual(len(preview_files), 0)
