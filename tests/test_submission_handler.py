import time
import unittest
import aiohttp
import asyncio


async def submit_and_check_status(session, payload, url):

    # Submit job and get token
    async with session.post((url + 'submissions/?base64_encoded=false&wait=false'), json=payload) as response:
        submission_response = await response.json()
        token = submission_response.get('token')

        # Assert the status code is 201 (Created)
        print(f"\nsubmit job response \n {submission_response} ")

        assert response.status == 201, f"Expected status code 201, but got {response.status}"

    base64_encoded = False
    timeout = 30
    start_time = time.time()

    while True:
        async with session.get(f'{url}/submissions/{token}?base64_encoded={base64_encoded}') as response:
            submission_status = await response.json()
            print(submission_status)
            if submission_status['status']['id'] != 1:  # Assuming 'id' 1 means 'In Queue'
                break
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for submission status to change")
            await asyncio.sleep(1)

    return submission_status


class TestPythonSubmission(unittest.IsolatedAsyncioTestCase):
    test_case_1 = {
        "source_code": "print(\"hello world\")",
        "language_id": 71,  # 50 for C, 73 rust, 55 common lisp
        # "stdin": "world"
    }

    async def asyncSetUp(self):
        self.session = aiohttp.ClientSession()
        # judge0 external ip judge0_url = 'http://155.138.214.97:2358/'
        # self.url = 'http://192.168.0.220:2358/'  internal
        self.url = 'http://155.138.214.97:2358/'

    async def tearDown(self):
        await self.session.close()

    async def test_python_submission(self):

        try:
            response = await submit_and_check_status(session=self.session, url=self.url, payload=self.test_case_1)
            print(f"test python submission: \n {response}")
        except TimeoutError as e:
            self.fail(f"Timeout error occurred: {str(e)}")
