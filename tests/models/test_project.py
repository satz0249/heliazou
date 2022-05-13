from tests.base import ApiDBTestCase

from zou.app.utils import fields
from zou.app.models.project import Project


class ProjectTestCase(ApiDBTestCase):
    def setUp(self):
        super(ProjectTestCase, self).setUp()
        self.generate_fixture_project_status()
        self.generate_fixture_project()
        self.generate_fixture_project("Agent 327")
        self.generate_fixture_project("Big Buck Bunny")
        self.open_status_id = str(self.open_status.id)

    def test_get_projects(self):
        projects = self.get("data/projects")
        self.assertEqual(len(projects), 3)

    def test_get_project(self):
        project = self.get_first("data/projects?relations=true")
        project_again = self.get("data/projects/%s" % project["id"])
        project["project_status_name"] = "Open"
        self.assertEqual(project, project_again)
        self.get_404("data/projects/%s" % fields.gen_uuid())

    def test_create_project(self):
        data = {
            "name": "Cosmos Landromat 2",
            "description": "Video game trailer.",
        }
        self.project = self.post("data/projects", data)
        self.assertIsNotNone(self.project["id"])
        self.assertEqual(
            self.project["project_status_id"], str(self.open_status_id)
        )

        projects = self.get("data/projects")
        self.assertEqual(len(projects), 4)

    def test_update_project(self):
        project = self.get_first("data/projects")
        data = {"name": "Cosmos Landromat 3"}
        self.put("data/projects/%s" % project["id"], data)
        project_again = self.get("data/projects/%s" % project["id"])
        self.assertEqual(data["name"], project_again["name"])
        self.put_404("data/projects/%s" % fields.gen_uuid(), data)

    def test_delete_project(self):
        projects = self.get("data/projects")
        self.assertEqual(len(projects), 3)
        project = projects[0]
        self.delete("data/projects/%s" % project["id"], 400)
        self.generate_fixture_project_closed_status()
        self.generate_fixture_project_closed()
        self.delete("data/projects/%s" % self.project_closed.id)
        self.assertIsNone(Project.get(self.project_closed.id))

    def test_project_status(self):
        data = {"name": "stalled", "color": "#FFFFFF"}
        self.open_status = self.post("data/project-status", data)
        data = {"name": "close", "color": "#000000"}
        self.close_status = self.post("data/project-status", data)
        data = {
            "name": "Cosmos Landromat 2",
            "description": "Video game trailer.",
            "project_status_id": self.open_status["id"],
        }
        self.project = self.post("data/projects", data)
        self.assertIsNotNone(self.project["id"])
        project_again = self.get("data/projects/%s" % self.project["id"])
        self.assertEqual(
            project_again["project_status_id"], self.open_status["id"]
        )

    def test_get_project_by_name(self):
        project_before = self.get("data/projects")[1]
        project = self.get_first(
            "data/projects?name=%s" % project_before["name"].lower()
        )
        self.assertEqual(project["id"], project_before["id"])
