from rest_framework import serializers

from python_test_skills import models


class PythonTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PythonTasks
        fields = ('id', 'title', 'description', 'initial_code')


class PythonTaskSuperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PythonTasks
        fields = '__all__'


class PythonTestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PythonTestResults
        fields = '__all__'


class ExecutedPythonCodeSerializer(serializers.Serializer):
    flake8 = serializers.CharField()
    stdout = serializers.CharField()






