import requests

url = 'https://yinyang.codes:5005/addproblem/'

data1 = {
    'text': 'test',
    'title': 'Sort the Array',
    'description': 'Given an array of integers nums, sort the array in ascending order and return it',
    'category': 'Sorting',
    'code': 'def sort(numbers):\\n\\treturn sorted(numbers)',
    'input_arrays': [
        {'input': [3, 1, 4, 1, 5, 9], 'output': [1, 1, 3, 4, 5, 9]},
        {'input': [1, 2, 3, 4, 5], 'output': [1, 2, 3, 4, 5]},
        # Add more test cases as needed
    ],


}


data2 = [
    {
        'text': 'test',
        'title': 'Fizz Buzz',
        'description': 'FizzBuzz is a classic programming problem often used in interviews to test basic programming skills. The problem is typically stated as follows: '
                       '\\nGiven a range of numbers, print each number in the range. However, for multiples of 3, print "Fizz" instead of the number. For multiples of 5, print "Buzz" instead of the number. For numbers that are multiples of both 3 and 5, print "FizzBuzz".'
                       '\\nFor example, if the range is from 1 to 15, the output should be:\\n'
                       '1\\n'
                       '2\\n'
                       'Fizz\\n'
                       '4\\n'
                       'Buzz\\n'
                       'Fizz\\n'
                       '7\\n'
                       '8\\n'
                       'Fizz\\n'
                       'Buzz\\n'
                       '11\\n'
                       'Fizz\\n'
                       '13\\n'
                       '14\\n'
                       'FizzBuzz\\n',

        'category': 'FizzBuzzing',
        'code': 'def fizz_buzz(n):\\n\\tresult = []\\n\\tfor i in range(1, n + 1):\\n\\t\\tif i % 3 == 0 and i % 5 == 0:\\n\\t\\t\\tresult.append("FizzBuzz")\\n\\t\\telif i % 3 == 0:\\n\\t\\t\\tresult.append("Fizz")\\n\\t\\telif i % 5 == 0:\\n\\t\\t\\tresult.append("Buzz")\\n\\t\\telse:\\n\\t\\t\\tresult.append(str(i))\\n\\treturn result',
        'input_arrays': [
            {'input': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
             'output': ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14',
                        'FizzBuzz']},
            {'input': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             'output': ['16', '17', 'Fizz', '19', 'Buzz', 'Fizz', '22', '23', 'Fizz', 'Buzz', '26', 'Fizz', '28', '29',
                        'FizzBuzz']},
            # Add more test cases as needed
        ],

    }
]

response = requests.get("http://localhost:5000/api/endpoint")

import pytest
import requests
#
# # Fixture to set up and tear down the Flask app and PostgreSQL container
# @pytest.fixture(scope="session")
# def setup_teardown():
#     # Set up the test environment (e.g., start Flask app and PostgreSQL container)
#     # Ensure the environment is torn down after the tests are finished
#     # You can use Docker Compose or other tools to manage the test environment
#     # For simplicity, let's assume Flask app and PostgreSQL container are already running
#
#     yield
#
#     # Tear down the test environment (e.g., stop Flask app and PostgreSQL container)
#     # Clean up any resources used during testing
#
# # Test cases
# def test_get_endpoint(setup_teardown):
#     # Make a request to the API endpoint you want to test
#     response = requests.get("http://localhost:5000/api/endpoint")
#
#     # Validate the response
#     assert response.status_code == 200
#     # Add more assertions to validate the response content, headers, etc.
#
# def test_post_endpoint(setup_teardown):
#     # Make a request to the API endpoint you want to test
#     payload = {"key": "value"}
#     response = requests.post("http://localhost:5000/api/endpoint", json=payload)
#
#     # Validate the response
#     assert response.status_code == 201
#     # Add more assertions to validate the response content, headers, etc.
#
#
#
#
