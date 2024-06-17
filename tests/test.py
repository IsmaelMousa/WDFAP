import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(first=True, second=True)


if __name__ == "__main__":
    unittest.main()
