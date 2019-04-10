from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import JSONParser

from urllib.parse import urlparse, urlunparse, urljoin
import requests
import io
from pprint import pprint

from .proceed_code import execute_code
from .linters import linter_stream
from .serializers import PythonTaskSerializer, PythonTaskSuperSerializer, PythonTestResultsSerializer, ExecutedPythonCodeSerializer
from .models import PythonTasks, PythonTestResults
from .python_code_test_framework import PythonTestsAPI


def index(request):
    return render(request, "index.html")


class GetPythonTasks(generics.ListAPIView):
    """
    json value of all tasks
    """
    queryset = PythonTasks.objects.all()
    serializer_class = PythonTaskSerializer


class GetPythonTask(generics.RetrieveAPIView):
    """
    json value of all tasks
    """
    serializer_class = PythonTaskSerializer

    def get_object(self):
        test_id = self.request.query_params.get('test_id')
        queryset = PythonTasks.objects.all()
        obj = get_object_or_404(queryset, pk=test_id)
        return obj


class GetPythonTasksWithAnswers(generics.ListAPIView):
    """
    json value of all tasks with answers
    """
    queryset = PythonTasks.objects.all()
    serializer_class = PythonTaskSuperSerializer

class GetPythonTaskWithAnswer(generics.RetrieveAPIView):
    """
    json value of task with answer
    """
    serializer_class = PythonTaskSuperSerializer

    def get_object(self):
        test_id = self.request.query_params.get('test_id')
        queryset = PythonTasks.objects.all()
        obj = get_object_or_404(queryset, pk=test_id)
        return obj


class GetPythonTestResults(generics.RetrieveAPIView):
    """
    Returns json with results of previous test results from database. If there is no record, blank string will be returned.
    """
    serializer_class = PythonTestResultsSerializer

    def get_object(self):
        queryset = PythonTestResults.objects.all()
        params = self.request.query_params
        user_id, test_id = params.get('user_id'), params.get('test_id')
        if user_id:
            current_user = user_id
        else:
            current_user = self.request.user
        if current_user is not None:
            obj = get_object_or_404(queryset, test_id=test_id, user_id=current_user)
        return obj

class UpdatePythonTestResults(generics.UpdateAPIView):
    queryset = PythonTestResults.objects.all()
    serializer_class = PythonTestResultsSerializer

    def get_object(self):
        user_id = self.request.data.get('user_id')
        test_id = self.request.data.get('test_id')
        queryset = PythonTestResults.objects.all()
        obj = get_object_or_404(queryset, test_id=test_id, user_id=user_id)
        return obj

    def partial_update(self, request):
        queryset = self.get_object()
        serialized = PythonTestResultsSerializer(queryset, data=request.data, partial=True)
        serialized.save()
        return Response(serialized.data)


class AddPythonTestResults(generics.CreateAPIView):
    queryset = PythonTestResults.objects.all()
    serializer_class = PythonTestResultsSerializer


class ExecutePythonCode(APIView):
    """
    Executes code from frontend and return json value with result of implementation.
    """
    def get(self, request):
        code = request.GET.get('user_code', '')
        result_stdout = execute_code(code)
        result_flake8 = linter_stream(code)
        return Response({'stdout': result_stdout, 'flake8': result_flake8})


class CheckUserCodeAndProvideResult(APIView):
    """
    Executes provided code, returns console log and result, if the test passed or not.
    """
    def get(self, request):
        test_api = PythonTestsAPI(request)
        previous_result = test_api.test_results(PythonTestResultsSerializer)
        response = dict()
        if previous_result.get('user_result'):
            response.update({'test_result': "The task has been completed successfully."})
            return Response(response)
        task = test_api.get_task_with_answer(PythonTaskSuperSerializer)
        right_code = task.get('right_code')
        executed_right_code = test_api.execute_python_code(ExecutedPythonCodeSerializer, code=right_code)
        executed_user_code = test_api.execute_python_code(ExecutedPythonCodeSerializer)
        test_result = (executed_right_code == executed_user_code)
        pprint(executed_user_code)
        if previous_result:
            test_api.update_test_result(user_result=test_result)
        else:
            test_api.add_new_test_result(user_result=test_result)
        response.update(executed_user_code)
        if test_result:
            response.update({'test_result': 'The test has been passed successfully!'})
        else:
            response.update({'test_result': 'Please try again.'})
        return Response(response)


