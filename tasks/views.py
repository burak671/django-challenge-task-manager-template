from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request: HttpRequest) -> HttpResponse:
    # Veritabanındaki tüm görevleri çekiyoruz
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Create Task", "submit_label": "Create"})

def task_edit(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Edit Task", "submit_label": "Save"})

def task_delete(request: HttpRequest, task_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")