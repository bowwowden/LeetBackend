import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import model
import orm
import config
import repository
import services

engine = create_engine(config.get_postgres_uri())
orm.metadata.create_all(engine)
orm.start_mappers()
get_session = sessionmaker(bind=engine)

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    code = "<p> Code </p>"

    return "<b> Hello World! </b> "


@app.route('/submit/', methods=['POST'])
def submit():
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


@app.route('/get-solutions/', methods=['POST'])
def getsolutions():
    return 'Solutions!'


@app.route('/addproblem/', methods=['POST'])
def addproblems():
    session = get_session()

    repo = repository.SqlAlchemyRepository(session)

    # Potentially make an add problem api endpoint
    problem = model.Problem(
        text=request.json["text"],
        title=request.json["title"],
        description=request.json["description"],
        category=request.json["category"],
        code=request.json["code"],
        input_arrays=request.json.get("input_arrays"),
        # input_boolean=request.json.get("input_boolean"),
        # input_string=request.json.get("input_string")
    )

    try:
        services.add_problem(problem, repo, session)
        result = "Added"

    except Exception as e:
        return {"message": str(e)}, 400

    return {"response": result}, 201


@app.route('/getproblems/', methods=['GET', 'POST'])
def getproblems():
    session = get_session()

    repo = repository.SqlAlchemyRepository(session)

    try:
        # For SQLAlchemy repositories, you can use the repo.list() method
        problems = repo.list()

        # Convert the list of problems to a list of dictionaries
        problems_list = [{"id": problem.id,
                          "description": problem.description,
                          "title": problem.title,
                          "category": problem.category,
                          "text": problem.text,
                          "input_arrays": problem.input_arrays
                          } for problem in problems]

        return jsonify(problems_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/getproblem/<int:problem_id>', methods=['GET'])
def getproblem(problem_id):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    try:
        problem = repo.get(problem_id)

        if problem:
            problem_data = {
                "id": problem.id,
                "description": problem.description,
                "title": problem.title,
                "category": problem.category,
                "text": problem.text,
                "code": problem.code,
                "input_arrays": problem.input_arrays
            }
            return jsonify(problem_data), 200
        else:
            return jsonify({"error": "Problem not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9900)
