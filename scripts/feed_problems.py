import requests

url = 'http://172.20.0.3:80/addproblem'

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

    # 'goldstandardcode': 'sorted()',
    # "input_boolean": self.input_boolean,
    # "input_string": self.input_string,

}

# data2 = {
#     'text': 'test',
#     'title': 'Sort the Linear List',
#     'description': 'Given an list of integers nums, sort the array in ascending order and return it',
#     'category': 'Sorting',
#     'code': 'def sort(numbers):\\n\\treturn "Hello World"'
# }
#

datas = [data1]

for data in datas:
    response = requests.post(url, json=data)
    print(response)