import json
import unittest
from main import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_serve_documentation(self):
        response = self.app.get('/api/')
        self.assertEqual(response.status_code, 200)

    # @unittest.skip
    def test_add_problem(self):
        # Data to be sent in the POST request
        problem_data = {
            "title": "FizzBuzz",
            "description": "Write a program that prints the numbers from 1 to 100. But for multiples of three, print 'Fizz' instead of the number and for the multiples of five, print 'Buzz'. For numbers which are multiples of both three and five, print 'FizzBuzz'.",
            "category": "Algorithm",
            "difficulty": "Easy",
            "solutions": [
                {
                    "language": "python",
                    "file_path": "/solutions/python/fizzbuzz.py"
                }
                # You can add more solutions here if needed
            ],
            "test_cases": [
                {
                    "inputs": {"param1": 1, "param2": 15},
                    "expected_outputs": {
                        "result": [
                            "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14",
                            "FizzBuzz"
                        ]
                    }
                },
                {
                    "inputs": {"param1": 1, "param2": 5},
                    "expected_outputs": {
                        "result": [
                            "1", "2", "Fizz", "4", "Buzz"
                        ]
                    }
                },
                {
                    "inputs": {"param1": 9, "param2": 15},
                    "expected_outputs": {
                        "result": [
                            "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"
                        ]
                    }
                }
            ]
        }

        # Send POST request to the `/addproblem` endpoint
        response = self.app.post('/addproblem',
                                 data=json.dumps(problem_data),
                                 content_type='application/json')

        print("response")
        print(response.data.decode())

        # Check that the status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Check the response data
        response_json = json.loads(response.data)
        self.assertIn("response", response_json)
        self.assertEqual(response_json["response"], "Added")
        self.assertIn("problem_id", response_json)
        self.assertIsInstance(response_json["problem_id"], int)

    def test_get_problems_page(self):
        response = self.app.get('/getproblems/')

        response_data = response.data.decode()

        # Pretty-print the JSON response
        try:
            response_json = json.loads(response_data)
            pretty_response = json.dumps(response_json, indent=4)
            print("Response:")
            print(pretty_response)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON response:")
            print(response_data)

        # Check that the response is a list
        response_json = response.get_json()
        self.assertIsInstance(response_json, list)

        # Ensure that there are problems in the list
        self.assertGreater(len(response_json), 0, "Expected at least one problem in the response")

        # Check specific fields for the first problem as an example
        first_problem = response_json[0]
        self.assertIn('id', first_problem)
        self.assertIn('title', first_problem)
        self.assertIn('category', first_problem)
        self.assertIn('difficulty', first_problem)

        self.assertEqual(response.status_code, 200)


    def test_get_solution(self):
        payload = {
            'problem_id': 2,
            'language': 'python'
        }
        response = self.app.post('/getsolution/', json=payload)

        print("response")
        print(response.data.decode())

        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        response_json = response.get_json()
        self.assertIn('id', response_json)
        self.assertIn('problem_id', response_json)
        self.assertIn('language', response_json)
        self.assertIn('file_content', response_json)

        # Additional assertions to verify the content
        self.assertEqual(response_json['problem_id'], 2)
        self.assertEqual(response_json['language'], 'python')
        self.assertTrue(len(response_json['file_content']) > 0)  # Ensure file content is not empty


    def test_get_test_cases(self):
        payload = {
            'problem_id': 1
        }
        response = self.app.post('/gettestcase/', json=payload)

        print("response")
        print(response.data.decode())

        self.assertEqual(response.status_code, 200)


    def test_get_problem(self):
        # Assuming the problem with id=1 exists in the test database
        response = self.app.get('/getproblem/1')
        print("response")
        print(response.data.decode())

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        response_json = response.get_json()
        self.assertEqual(response_json['id'], 1)
        self.assertIn('title', response_json)
        self.assertIn('description', response_json)
        self.assertIn('category', response_json)
        self.assertIn('difficulty', response_json)

        # Check solutions field
        if 'solutions' in response_json:
            for solution in response_json['solutions']:
                self.assertIn('id', solution)
                self.assertIn('language', solution)
                self.assertIn('file_content', solution)
                # Check that file_content is not empty; adjust according to your test setup
                self.assertTrue(len(solution['file_content']) > 0 or solution['file_content'] == "File not found")
        else:
            self.fail("Solutions field is missing in the response")

            # Check that test cases are included
        self.assertIn('test_cases', response_json)
        for test_case in response_json['test_cases']:
            self.assertIn('id', test_case)
            self.assertIn('inputs', test_case)
            self.assertIn('expected_outputs', test_case)


    @unittest.skip
    def test_submit(self):
        pass
