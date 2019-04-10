"""python_test_skills application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from python_test_skills import views


urlpatterns = [
    path('', views.index),
    path('tasks', views.GetPythonTasks.as_view()),
    path('task', views.GetPythonTask.as_view()),
    path('task_with_answer', views.GetPythonTaskWithAnswer.as_view()),
    path('execute_python_code', views.ExecutePythonCode.as_view()),
    path('test_results', views.GetPythonTestResults.as_view()),
    path('update_test_result', views.UpdatePythonTestResults.as_view()),
    path('add_test_result', views.AddPythonTestResults.as_view()),
    path('proceed_test', views.CheckUserCodeAndProvideResult.as_view())
]