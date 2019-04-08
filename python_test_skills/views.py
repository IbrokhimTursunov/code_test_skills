from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from pprint import pprint

from python_test_skills import proceed_code
from python_test_skills.serializers import PythonTaskSerializer, PythonTaskSuperSerializer, PythonTestResultsSerializer
from python_test_skills.models import PythonTasks, PythonTestResults


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
    json value of all tasks
    """
    queryset = PythonTasks.objects.all()
    serializer_class = PythonTaskSuperSerializer


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
    serializer_class = PythonTestResultsSerializer

    def get_object(self):
        queryset = PythonTestResults.objects.all()
        user_id_param = self.request.query_params.get('user_id')
        user_id = user_id_param if user_id_param else self.request.user
        test_id = self.request.query_params.get('test_id')
        obj = get_object_or_404(queryset, test_id=test_id, user_id=user_id)
        return obj


class ExecutePythonCode(APIView):
    """
    Executes code from frontend and return json value with result of implementation.
    """
    def get(self, request):
        code = request.GET.get('code', '')
        result_of_code_execution = proceed_code.execute_code(code)
        return Response({'result of code execution': result_of_code_execution})


class CheckUserCodeAndProvideResult(generics.UpdateAPIView):
    """
    Executes provided code, returns console log and result, if the test passed or not.
    """
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


