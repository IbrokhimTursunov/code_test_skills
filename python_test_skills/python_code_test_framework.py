import io
from urllib.parse import urlparse, urlunparse, urljoin

import requests
from rest_framework.parsers import JSONParser

def get_params(request, parameters):
    if request.method == 'GET':
        request_method = request.GET
    elif request.method == 'PUT':
        request_method = request.PUT
    elif request.method == 'POST':
        request_method = request.POST
    else:
        request_method = None
    result = dict()
    for p in parameters:
        if p == 'user_id':
            user_id = request_method.get(p)
            if user_id is None:
                user_id = request.user.id
            result[p] = user_id
        else:
            result[p] = request_method.get(p)
    return result


class PythonTestsAPI:

    def __init__(self, request):
        self.django_request = request._request
        absolute_url = self.django_request.build_absolute_uri()
        parsed_url = urlparse(absolute_url)
        self.base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

    def extract_data(self, response, serializer):
        json_value = response._content
        stream = io.BytesIO(json_value)
        data = JSONParser().parse(stream)
        serializer = serializer(data=data)
        serializer.is_valid()
        return serializer.data

    def test_results(self, serializer):
        url = urljoin(self.base_url, 'python_test_skills/test_results')
        params = get_params(self.django_request, ['user_id', 'test_id'])
        response = requests.get(url, params=params)
        return self.extract_data(response, serializer)

    def update_test_result(self, user_result=False):
        url = urljoin(self.base_url, 'python_test_skills/update_test_result')
        data = get_params(self.django_request, ['user_id', 'test_id', 'user_code'])
        data['user_result'] = user_result
        requests.put(url, data=data)
        return None

    def add_new_test_result(self, user_result=False):
        url = urljoin(self.base_url, 'python_test_skills/add_test_result')
        data = get_params(self.django_request, ['user_id', 'test_id', 'user_code'])
        data['user_result'] = user_result
        requests.post(url, data=data)
        return None

    def get_task_with_answer(self, serializer):
        url = urljoin(self.base_url, 'python_test_skills/task_with_answer')
        params = get_params(self.django_request, ['test_id'])
        response = requests.get(url, params=params)
        return self.extract_data(response, serializer)

    def execute_python_code(self, serializer, code=None):
        if code is None:
            params = get_params(self.django_request, ['user_code'])
        else:
            params = {'user_code': code}
        url = urljoin(self.base_url, 'python_test_skills/execute_python_code')
        response = requests.get(url, params=params)
        return self.extract_data(response, serializer)
