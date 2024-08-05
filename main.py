import json
import os

from flask import Flask, request, jsonify, send_from_directory
# Configure Flask logging to print to console
import logging
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import model
import orm
import config
import repository
import services

# Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from all origins
app.logger.setLevel(logging.DEBUG)

# SQL Alchemy
engine = create_engine(config.get_postgres_uri())
get_session = sessionmaker(bind=engine)
model.Base.metadata.create_all(engine)


# Define a route for serving Sphinx documentation
@app.route('/api/<path:filename>')
@app.route('/api/', defaults={'filename': 'index.html'})
def serve_documentation(filename):
    directory = 'build/html'  # Adjust this path based on your Sphinx build directory

    # Log the directory and filename being served
    app.logger.debug(f"Serving file '{filename}' from directory '{directory}'")

    return send_from_directory(directory, filename)


@app.route('/addproblem', methods=['POST'])
def addproblem():
    """
    Add a new problem with test cases.

    This endpoint allows users to submit a new problem to the system along with its details
    such as title, description, category, difficulty, and a solution code. It also allows
    for the addition of test cases associated with the problem.

    **Example Request**:

    .. sourcecode:: http

        POST /addproblem HTTP/1.1
        Content-Type: application/json

        {
            "title": "Sample Problem",
            "description": "This is a sample problem description.",
            "category": "Algorithm",
            "difficulty": "Medium",
            "solutions": [
                {
                    "language": "python",
                    "file_path": "/path/to/fizzbuzz.py"
                },
                {
                    "language": "lisp",
                    "file_path": "/path/to/fizzbuzz.lisp"
                }
            ],
            "test_cases": [
                {
                    "inputs": {"param1": 1, "param2": 2},
                    "expected_outputs": {"result": 3}
                },
                {
                    "inputs": {"param1": 3, "param2": 4},
                    "expected_outputs": {"result": 7}
                }
            ]
        }

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        {
            "response": "Added",
            "problem_id": 1,
            "test_cases": [
                {
                    "id": 1,
                    "inputs": {"param1": 1, "param2": 15},
                    "expected_outputs": {"result": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]}
                },
                {
                    "id": 2,
                    "inputs": {"param1": 1, "param2": 5},
                    "expected_outputs": {"result": ["1", "2", "Fizz", "4", "Buzz"]}
                }
            ]
        }

    **Request Parameters**:

    - `title` (string) -- The title of the problem.
    - `description` (string) -- A detailed description of the problem.
    - `category` (string) -- The category of the problem (e.g., Algorithm, Data Structure).
    - `difficulty` (string) -- The difficulty level of the problem (e.g., Easy, Medium, Hard).
    - `solutions` (list) -- A list of solution objects, each containing:
        - `language` (string) -- The programming language of the solution (e.g., python, lisp).
        - `file_path` (string) -- The path to the solution file.
    - `test_cases` (list) -- A list of test cases, each containing `inputs` and `expected_outputs` fields.


    **Returns**:

    - JSON response indicating the success or failure of adding the problem.
    - The response will include the `problem_id` if the problem is successfully added.

    :return: JSON response with the result of the operation.
    :rtype: flask.Response
    """
    session = get_session()

    try:
        data = request.json
        problem = model.Problem(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            difficulty=data['difficulty']
        )
        session.add(problem)
        session.commit()

        solutions = data.get('solutions', [])
        for sol in solutions:
            solution = model.Solution(
                problem_id=problem.id,
                language=sol['language'],
                file_path=sol['file_path']
            )
            session.add(solution)

        session.commit()

        test_cases = data.get('test_cases', [])
        test_cases_list = []
        for tc in test_cases:
            test_case = model.TestCase(
                problem_id=problem.id,
                inputs=tc['inputs'],
                expected_outputs=tc['expected_outputs']
            )
            session.add(test_case)
            session.commit()
            test_cases_list.append({
                'id': test_case.id,
                'inputs': test_case.inputs,
                'expected_outputs': test_case.expected_outputs
            })

        return jsonify({"response": "Added", "problem_id": problem.id, "test_cases": test_cases_list}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@app.route('/getproblem/<int:problem_id>', methods=['GET'])
def getproblem(problem_id):
    """
    Retrieve detailed information about a specific problem, including its solutions, test cases, and submissions.

    This endpoint returns comprehensive details about a problem specified by its ID. It includes problem metadata, solution contents, test cases, and submissions.

    **Example Request**:

        GET /getproblem/1 HTTP/1.1

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "id": 1,
            "title": "FizzBuzz",
            "description": "Write a program that prints the numbers from 1 to 100. For multiples of three, print 'Fizz' instead of the number, for multiples of five, print 'Buzz', and for numbers which are multiples of both three and five, print 'FizzBuzz'.",
            "category": "Algorithm",
            "difficulty": "Easy",
            "solutions": [
                {
                    "id": 1,
                    "language": "python",
                    "file_content": "# Solution code here..."
                }
            ],
            "test_cases": [
                {
                    "id": 1,
                    "problem_id": 1,
                    "inputs": {
                        "param1": 1,
                        "param2": 15
                    },
                    "expected_outputs": {
                        "result": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
                    }
                }
            ],
            "submissions": [
                {
                    "id": 1,
                    "problem_id": 1,
                    "submission_time": "2024-08-01T12:00:00Z",
                    "status": "Accepted"
                }
            ]
        }

    **Request Method**:

    - GET

    **Request Parameters**:

    - `problem_id` (int) -- The unique identifier of the problem to retrieve.

    **Responses**:

    - 200 OK: A JSON object containing:
      - `id` (int) -- The unique identifier of the problem.
      - `title` (str) -- The title of the problem.
      - `description` (str) -- A detailed description of the problem.
      - `category` (str) -- The category under which the problem falls.
      - `difficulty` (str) -- The difficulty level of the problem.
      - `solutions` (list of dicts) -- A list of dictionaries representing solutions to the problem. Each dictionary includes:
        - `id` (int) -- The unique identifier of the solution.
        - `language` (str) -- The programming language of the solution.
        - `file_content` (str) -- The content of the solution file. If the file is not found, the content will be "File not found".
      - `test_cases` (list of dicts) -- A list of test case dictionaries, each representing a test case for the problem.
      - `submissions` (list of dicts) -- A list of submission dictionaries, each representing a submission for the problem.

    - 400 Bad Request: If an error occurs during processing. The response will contain a JSON object with an `error` field describing the issue.

    - 404 Not Found: If the problem with the specified `problem_id` is not found. The response will contain a JSON object with an `error` field indicating "Problem not found."

    **Notes**:

    - If the solution file path is incorrect or the file is missing, the `file_content` will indicate "File not found".
    - The `__json__` method should be defined in the `TestCase` and `Submission` models to serialize the test case and submission data into a dictionary format.

    :return: JSON response with the detailed problem information.
    :rtype: flask.Response
    """

    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    try:
        problem = repo.get(problem_id)

        if problem:
            # Check solution file contents
            solutions_data = []
            for solution in problem.solutions:
                try:
                    with open(solution.file_path, 'r') as file:
                        solution_content = file.read()
                except FileNotFoundError:
                    solution_content = "File not found"

                solutions_data.append({
                    "id": solution.id,
                    "language": solution.language,
                    "file_content": solution_content
                })

            problem_data = {
                "id": problem.id,
                "title": problem.title,
                "description": problem.description,
                "category": problem.category,
                "difficulty": problem.difficulty,
                "solutions": solutions_data,  # Include solution contents
                "test_cases": [tc.__json__() for tc in problem.test_cases],
                "submissions": [s.__json__() for s in problem.submissions]
            }

            return jsonify(problem_data), 200
        else:
            return jsonify({"error": "Problem not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/getsolution/', methods=['POST'])
def getsolution():
    """
    Retrieve the solution file for a given problem and programming language.

    This endpoint returns the content of a solution file based on the provided
    problem ID and programming language. The response includes the solution's
    ID, problem ID, language, and the content of the solution file.

    **Example Request**:

    .. sourcecode:: http

        POST /getsolution/ HTTP/1.1
        Content-Type: application/json

        {
            "problem_id": 1,
            "language": "python"
        }

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "id": 1,
            "problem_id": 1,
            "language": "python",
            "file_content": "def solve(): pass"
        }

    **Request Method**:

    - POST

    **Responses**:

    - 200 OK: A JSON object containing:
      - `id` (int) -- The unique identifier for the solution.
      - `problem_id` (int) -- The ID of the associated problem.
      - `language` (str) -- The programming language of the solution.
      - `file_content` (str) -- The content of the solution file.

    - 400 Bad Request: If the `problem_id` or `language` is missing or if an
      error occurs during processing. The response will contain a JSON object
      with an `error` field describing the issue.

    - 404 Not Found: If the solution file or the solution itself is not found.
      The response will contain a JSON object with an `error` field indicating
      "Solution file not found" or "Solution not found."

    **Notes**:

    - The solution file path is constructed relative to the current working directory.
    - Ensure that the `file_path` field in the `Solution` model does not start with a leading slash to avoid incorrect absolute paths.

    :return: JSON response with the solution details.
    :rtype: flask.Response
    """

    session = get_session()

    try:
        data = request.json
        problem_id = data.get('problem_id')
        language = data.get('language')

        if not problem_id:
            return jsonify({"error": "Problem ID is required"}), 400
        if not language:
            return jsonify({"error": "Language is required"}), 400

        # Fetch the solution based on problem_id and language
        solution = session.query(model.Solution).filter_by(problem_id=problem_id, language=language).first()

        if solution:
            print("\n"
                  "solution file path"
                  "\n")
            print(solution.file_path)
            file_path = solution.file_path
            current_directory = os.getcwd()

            # If the file_path starts with a '/', remove it to prevent incorrect absolute path
            if file_path.startswith('/'):
                file_path = file_path[1:]

            # Ensure the file path is absolute
            absolute_file_path = os.path.join(current_directory, file_path)

            print(f"absolute file path {absolute_file_path}")
            # Read the content of the file
            if os.path.exists(absolute_file_path):
                with open(absolute_file_path, 'r') as file:
                    file_content = file.read()
                return jsonify({
                    "id": solution.id,
                    "problem_id": solution.problem_id,
                    "language": solution.language,
                    "file_content": file_content
                }), 200
            else:
                return jsonify({"error": "Solution file not found"}), 404
        else:
            return jsonify({"error": "Solution not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@app.route('/getproblems/', methods=['GET'])
def getproblemspage():
    """
    Retrieve a list of problems with their basic details.

    This endpoint returns a list of problems, including their ID, title,
    category, and difficulty level. This information is used to display
    problems in a summary view, allowing users to select a problem to view
    more detailed information.

    **Example Request**:

    .. sourcecode:: http

        GET /getproblems HTTP/1.1

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "id": 1,
                "title": "FizzBuzz",
                "category": "Algorithm",
                "difficulty": "Easy"
            },
            {
                "id": 2,
                "title": "Two Sum",
                "category": "Algorithm",
                "difficulty": "Medium"
            }
        ]

    **Request Method**:

    - GET

    **Responses**:

    - 200 OK: A JSON array of problem objects, each containing:
      - `id` (int) -- The unique identifier for the problem.
      - `title` (str) -- The title of the problem.
      - `category` (str) -- The category under which the problem falls.
      - `difficulty` (str) -- The difficulty level of the problem.

    - 400 Bad Request: If an error occurs while retrieving the problems. The response
      will contain a JSON object with an `error` field describing the issue.

    **Notes**:

    - The response excludes detailed information about solutions, test cases, and submissions.

    :return: JSON array of problem summaries.
    :rtype: flask.Response
    """
    session = get_session()
    try:
        # Query only the required fields
        problems = session.query(
            model.Problem.id,
            model.Problem.title,
            model.Problem.category,
            model.Problem.difficulty
        ).all()

        # Convert the results to a list of dictionaries
        problems_list = [
            {
                "id": p.id,
                "title": p.title,
                "category": p.category,
                "difficulty": p.difficulty
            }
            for p in problems
        ]

        return jsonify(problems_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@app.route('/gettestcase/', methods=['POST'])
def gettestcases():
    """
    Retrieve all test cases associated with a given problem ID.

    This endpoint retrieves a list of test cases for a specified problem. Each test case includes
    details such as inputs and expected outputs.

    **Example Request**:

    .. sourcecode:: http

        POST /gettestcase/ HTTP/1.1
        Content-Type: application/json

        {
            "problem_id": 1
        }

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "test_cases": [
                {
                    "id": 1,
                    "problem_id": 1,
                    "inputs": {
                        "param1": 1,
                        "param2": 15
                    },
                    "expected_outputs": {
                        "result": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
                    }
                },
                {
                    "id": 2,
                    "problem_id": 1,
                    "inputs": {
                        "param1": 1,
                        "param2": 5
                    },
                    "expected_outputs": {
                        "result": ["1", "2", "Fizz", "4", "Buzz"]
                    }
                }
            ]
        }

    **Request Parameters**:

    - `problem_id` (int) -- The unique identifier of the problem whose test cases are to be retrieved.

    **Returns**:

    - 200 OK: A JSON response containing a `test_cases` key, which is a list of dictionaries. Each dictionary represents a test case and includes:
      - `id` (int) -- The unique identifier of the test case.
      - `problem_id` (int) -- The ID of the associated problem.
      - `inputs` (dict) -- A dictionary of input parameters for the test case.
      - `expected_outputs` (dict) -- A dictionary of expected outputs for the test case.

    - 400 Bad Request: If the `problem_id` is missing or if an error occurs during processing. The response will contain a JSON object with an `error` field describing the issue.

    - 404 Not Found: If no test cases are found for the specified `problem_id`. The response will contain a JSON object with an `error` field indicating "No test cases found for this problem."

    :return: JSON response with the list of test cases or an error message.
    :rtype: flask.Response
    """
    session = get_session()

    try:
        data = request.json
        problem_id = data.get('problem_id')

        if not problem_id:
            return jsonify({"error": "Problem ID is required"}), 400

        test_cases = session.query(model.TestCase).filter_by(problem_id=problem_id).all()

        if test_cases:
            test_cases_data = [tc.__json__() for tc in test_cases]
            return jsonify({"test_cases": test_cases_data}), 200
        else:
            return jsonify({"error": "No test cases found for this problem"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@app.route('/submit/', methods=['POST'])
def submit():
    """
    Submit code to judge0.

    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "id": 1,
                "name": "problem1"
            }
        ]

    :return: JSON response with pass/fail of all test cases.
    :rtype: flask.Response
    """
    session = get_session()

    repo = repository.SqlAlchemyRepository(session)

    try:
        print("Submit request:")
        print(request.headers)
        # print(request.json)

        result = request.json
        print(result)
        # submit to judge0
        import submission_handler as submission_handler
        submission_response = submission_handler.submit_code({"problem": result})

        print("Submission response")
        print(submission_response)
        output = submission_response["stdout"]
        time = submission_response["time"]

    except Exception as e:
        return {"message": str(e)}, 400

    return {"output": output, "time": time}, 201
