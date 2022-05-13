from tests.base import ApiDBTestCase


class ShotCsvExportTestCase(ApiDBTestCase):
    def setUp(self):
        super(ShotCsvExportTestCase, self).setUp()

        self.generate_fixture_project_status()
        self.generate_fixture_project()
        self.generate_fixture_asset_type()
        self.generate_fixture_department()
        self.generate_fixture_task_type()
        self.generate_fixture_task_status()
        self.generate_fixture_asset()
        self.generate_fixture_episode()
        self.generate_fixture_sequence()
        self.generate_fixture_shot()
        self.generate_fixture_person()
        self.generate_fixture_assigner()
        self.generate_fixture_shot_task()

    def test_export(self):
        csv_shots = self.get_raw(
            "/export/csv/projects/%s/shots.csv" % self.project.id
        )
        expected_result = """Project;Episode;Sequence;Name;Description;Time Spent;Nb Frames;Frame In;Frame Out;FPS;Animation\r
Cosmos Landromat;E01;S01;P01;Description Shot 01;0.00;0;0;100;25;opn\r\n"""
        self.assertEqual(csv_shots, expected_result)

    def test_export_with_metadata(self):
        self.generate_fixture_metadata_descriptor("Shot")
        self.shot.update(
            {
                "data": {
                    "frame_in": "0",
                    "frame_out": "100",
                    "fps": "25",
                    "contractor": "Contractor 1",
                }
            }
        )
        csv_shots = self.get_raw(
            "/export/csv/projects/%s/shots.csv" % self.project.id
        )
        expected_result = """Project;Episode;Sequence;Name;Description;Time Spent;Nb Frames;Frame In;Frame Out;FPS;Contractor;Animation\r
Cosmos Landromat;E01;S01;P01;Description Shot 01;0.00;0;0;100;25;Contractor 1;opn\r\n"""
        self.assertEqual(csv_shots, expected_result)
