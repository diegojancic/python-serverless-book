from django.test import TestCase
from django.urls import reverse

from todo.models import ToDoItem


class TodoModelTestCase(TestCase):

    def test_str(self):
        item = ToDoItem(text="Create a test", completed=True)
        self.assertEqual(item.__str__(), "Create a test")

    def test_list_view(self):
        # Create an item in the database
        ToDoItem.objects.create(text="Test the views", completed=False)

        # Call the view
        url = reverse("todo:list")
        response = self.client.get(url)

        # Test the response contains the correct text
        self.assertTemplateUsed("todo/index.html")
        self.assertContains(response, "Test the views")

    def test_create_view(self):
        url = reverse("todo:create")
        response = self.client.post(url, {"text": "New item POSTed!"})

        # Validate the user was redirected to the list page
        self.assertRedirects(response, reverse("todo:list"))

        # Validate the item was saved in the DB
        items_in_db = ToDoItem.objects.all()

        self.assertEqual(1, len(items_in_db), "There should be only 1 item")
        self.assertEqual("New item POSTed!", items_in_db[0].text)
