from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import TaskForm

SAMPLE_TASKS = [
    {
        "id": 1,
        "title": "Read Django docs",
        "description": "Understand models, views, and templates",
        "is_completed": False,
    },
    {
        "id": 2,
        "title": "Practice CRUD",
        "description": "Implement create, edit, delete, and list",
        "is_completed": True,
    },
]


def _get_sample_task(task_id: int) -> dict[str, object]:
    for task in SAMPLE_TASKS:
        if task["id"] == task_id:
            return task
    raise Http404("Task not found")


def task_list(request: HttpRequest) -> HttpResponse:
    # TODO(student): replace SAMPLE_TASKS with Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": SAMPLE_TASKS})


def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # TODO(student): validate and save a Task instance using the form
        return redirect("task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "page_title": "Create Task", "submit_label": "Create"},
    )


def task_edit(request: HttpRequest, task_id: int) -> HttpResponse:
    task = _get_sample_task(task_id)

    if request.method == "POST":
        # TODO(student): load Task from DB, validate, and persist updates
        return redirect("task_list")
    else:
        form = TaskForm(initial=task)

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "page_title": "Edit Task", "submit_label": "Save"},
    )


def task_delete(request: HttpRequest, task_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Keep 404 behavior for invalid IDs in the starter template.
    _get_sample_task(task_id)
    # TODO(student): delete the Task from the database
    return redirect("task_list")
