import unittest, sql2mermaid as s
SQL="CREATE TABLE users (id int PRIMARY KEY,\n name text);\nCREATE TABLE posts (id int PRIMARY KEY,\n user_id int REFERENCES users(id));"
class T(unittest.TestCase):
    def test(self):
        o=s.render(SQL); self.assertIn("erDiagram",o); self.assertIn("int id PK",o); self.assertIn("users ||--o{ posts",o)
unittest.main()
