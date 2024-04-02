import requests
import time
import config

url = config.judge0_url


def map_language(lang):
    langs = {
        "Python": 71,
        "Rust": 73,
        "Common Lisp": 55
    }
    return langs[lang]


def submit_code(body):
    # source code?
    # language?
    function = body["problem"]["code"]
    language = body["problem"]["language"]
    input = body["problem"]["input"]

    source_code = test_runner(function, language, input)

    myobj = {
        "source_code": source_code,
        "language_id": map_language(language)
    }

    request = requests.post((url + 'submissions/?base64_encoded=false&wait=false'), json=myobj)

    # Parse the JSON response
    response_data = request.json()

    # Extract the token from the response
    token = response_data.get('token')  # Replace 'token' with the actual key in your JSON response

    print(f"token {token}")

    # Sleep for 2 seconds
    time.sleep(2)

    print("After making request, check that hash for submission stdout")

    base64_encoded = False
    # fields = 'stdout,stderr,status_id,language_id'
    # &fields={fields}

    # Send a GET request
    response = requests.get((url + f'/submissions/{token}?base64_encoded={base64_encoded}'))
    print("url: " + (url + f'submissions/{token}?base64_encoded={base64_encoded}'))

    print(response.text)

    print(response.status_code)

    return response.json()


def python_test_runner(function, input):
    # Also, this needs some type of test case info.
    # Problem ID -> Database or Test Runner that runs correct algorithm? Hard choice.

    # Given a function, run it and put it in standard out.
    wrapper_code = \
f"""
{function}

numbers = {input}

print(sort(numbers))

"""

    return wrapper_code


def rust_test_runner(function, input):
    wrapper_code = \
"""
fn main() {
    // Create a vector of numbers
    let mut numbers = vec![5, 2, 8, 1, 7];

    // Sort the vector in ascending order
    numbers.sort();

    // Print the sorted vector
    println!("Sorted Numbers: {:?}", numbers);
}
"""

    return wrapper_code


def common_lisp_test_runner(function):
    wrapper_code = \
"""
(defun main ()
  ;; Create a list of numbers
  (let ((numbers '(5 2 8 1 7)))
    ;; Sort the list in ascending order
    (setf numbers (sort numbers #'<))

    ;; Print the sorted list
    (format t "Sorted Numbers: ~a~%" numbers)))

;; Call the main function
(main)
"""
    return wrapper_code


def test_runner(function, language, input):
    running_code = """print("No edit")"""

    if language == "Python":
        running_code = python_test_runner(function, input)

    else:
        return f"""print("Error, not found {language} {input}")"""

    return running_code

