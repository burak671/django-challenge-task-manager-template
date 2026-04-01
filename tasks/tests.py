from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_string_representation_returns_title(self) -> None:
        task = Task.objects.create(title="Read docs")

        self.assertEqual(str(task), "Read docs")

    def test_default_ordering_is_newest_first(self) -> None:
        older = Task.objects.create(title="Older task")
        newer = Task.objects.create(title="Newer task")

        tasks = list(Task.objects.all())

        self.assertEqual(tasks, [newer, older])


class TaskListViewTests(TestCase):
    def test_list_reads_from_database(self) -> None:
        Task.objects.create(title="Read docs")
        Task.objects.create(title="Write tests")

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Read docs")
        self.assertContains(response, "Write tests")

    def test_list_shows_empty_state_when_no_tasks(self) -> None:
        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks yet.")

    def test_list_displays_completed_label_for_finished_tasks(self) -> None:
        Task.objects.create(title="Done task", is_completed=True)

        response = self.client.get(reverse("task_list"))

        self.assertContains(response, "(completed)")

    def test_list_renders_newest_task_first(self) -> None:
        Task.objects.create(title="First task")
        Task.objects.create(title="Second task")

        response = self.client.get(reverse("task_list"))
        content = response.content.decode()

        self.assertLess(content.index("Second task"), content.index("First task"))


class TaskCreateViewTests(TestCase):
    def test_create_get_renders_form(self) -> None:
        response = self.client.get(reverse("task_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")
        self.assertEqual(response.context["page_title"], "Create Task")
        self.assertEqual(response.context["submit_label"], "Create")

    def test_create_valid_task(self) -> None:
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Implement feature",
                "description": "Make task CRUD work",
                "is_completed": "on",
            },
        )

        self.assertRedirects(response, reverse("task_list"))
        task = Task.objects.get()
        self.assertEqual(task.title, "Implement feature")
        self.assertEqual(task.description, "Make task CRUD work")
        self.assertTrue(task.is_completed)

    def test_create_defaults_is_completed_to_false_when_checkbox_missing(self) -> None:
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Unchecked task",
                "description": "No checkbox submitted",
            },
        )

        self.assertRedirects(response, reverse("task_list"))
        task = Task.objects.get()
        self.assertFalse(task.is_completed)

    def test_create_invalid_task_shows_errors(self) -> None:
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "",
                "description": "Missing title",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "title", "This field is required."
        )
        self.assertEqual(Task.objects.count(), 0)


class TaskEditViewTests(TestCase):
    def test_edit_get_prefills_existing_task(self) -> None:
        task = Task.objects.create(
            title="Existing title",
            description="Existing description",
            is_completed=True,
        )

        response = self.client.get(reverse("task_edit", args=[task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")
        self.assertEqual(response.context["page_title"], "Edit Task")
        self.assertEqual(response.context["submit_label"], "Save")
        form = response.context["form"]
        self.assertEqual(form.instance.id, task.id)
        self.assertEqual(form.instance.title, "Existing title")
        self.assertEqual(form.instance.description, "Existing description")
        self.assertTrue(form.instance.is_completed)

    def test_edit_valid_task(self) -> None:
        task = Task.objects.create(title="Old title")

        response = self.client.post(
            reverse("task_edit", args=[task.id]),
            {
                "title": "New title",
                "description": "Updated",
                "is_completed": "on",
            },
        )

        self.assertRedirects(response, reverse("task_list"))
        task.refresh_from_db()
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "Updated")
        self.assertTrue(task.is_completed)

    def test_edit_invalid_task_shows_errors_and_does_not_change_task(self) -> None:
        task = Task.objects.create(
            title="Current title", description="Current description"
        )

        response = self.client.post(
            reverse("task_edit", args=[task.id]),
            {
                "title": "",
                "description": "Should not be saved",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "title", "This field is required."
        )
        task.refresh_from_db()
        self.assertEqual(task.title, "Current title")
        self.assertEqual(task.description, "Current description")

    def test_edit_invalid_id_returns_404(self) -> None:
        response = self.client.post(
            reverse("task_edit", args=[99999]),
            {
                "title": "Does not matter",
                "description": "",
            },
        )

        self.assertEqual(response.status_code, 404)


class TaskDeleteViewTests(TestCase):
    def test_delete_valid_task(self) -> None:
        task = Task.objects.create(title="Delete me")

        response = self.client.post(reverse("task_delete", args=[task.id]))

        self.assertRedirects(response, reverse("task_list"))
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_with_get_is_not_allowed(self) -> None:
        task = Task.objects.create(title="Do not delete with get")

        response = self.client.get(reverse("task_delete", args=[task.id]))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.headers["Allow"], "POST")
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_delete_invalid_id_returns_404(self) -> None:
        response = self.client.post(reverse("task_delete", args=[99999]))

        self.assertEqual(response.status_code, 404)
