from tests.source.shotgun.base import ShotgunTestCase


class ImportShotgunPersonTestCase(ShotgunTestCase):
    def setUp(self):
        super(ImportShotgunPersonTestCase, self).setUp()

    def test_import_persons(self):
        self.persons = self.load_fixture("persons")
        self.assertEqual(len(self.persons), 2)

        self.persons = self.get("data/persons")
        self.assertEqual(len(self.persons), 3)
        self.assertEqual(self.persons[0]["active"], True)

    def test_import_persons_twice(self):
        self.persons = self.load_fixture("persons")
        self.persons = self.load_fixture("persons")
        self.assertEqual(len(self.persons), 2)

        self.persons = self.get("data/persons")
        self.assertEqual(len(self.persons), 3)

    def test_import_person(self):
        sg_person = {
            "email": "james.doe@gmail.com",
            "firstname": "James",
            "lastname": "Doe",
            "login": "jamie",
            "id": 3,
            "sg_status_list": "dis",
            "type": "HumanUser",
        }

        api_path = "/import/shotgun/persons"
        self.persons = self.post(api_path, [sg_person], 200)
        self.assertEqual(len(self.persons), 1)

        self.persons = self.get("data/persons")
        self.assertEqual(len(self.persons), 2)

        person = self.persons[1]
        self.assertEqual(person["first_name"], sg_person["firstname"])
        self.assertEqual(person["last_name"], sg_person["lastname"])
        self.assertEqual(person["shotgun_id"], sg_person["id"])
        self.assertEqual(person["desktop_login"], sg_person["login"])
        self.assertEqual(person["active"], False)
        self.assertEqual(person["role"], "user")

    def test_import_admin(self):
        sg_person = {
            "email": "james.doe@gmail.com",
            "firstname": "James",
            "lastname": "Doe",
            "login": "jamie",
            "id": 3,
            "sg_status_list": "dis",
            "type": "HumanUser",
            "permission_rule_set": {"name": "Admin"},
        }

        api_path = "/import/shotgun/persons"
        self.persons = self.post(api_path, [sg_person], 200)
        self.assertEqual(len(self.persons), 1)

        self.persons = self.get("data/persons")
        self.assertEqual(len(self.persons), 2)

        person = self.persons[1]
        self.assertEqual(person["role"], "admin")
