"""Test TodoMVC."""

import random

import allure
from hamcrest import assert_that, empty, has_item, is_not
from pages.todo_mvc_page import TodoMVCPage
from playwright.sync_api import Page


@allure.suite("TodoApp test - Castor")
class TestTodoApp:
    """TodoApp test suite."""

    @allure.title("Agregar Tarea: Verificar que se pueda agregar una nueva tarea")
    def test_create_new_task(self, page: Page):
        """Create new task test.

        Agregar Tarea: Verificar que se pueda agregar una nueva tarea.
        """
        task_name = "Complete the challenge"
        mvc_page = TodoMVCPage(page=page)
        mvc_page.navigate()
        mvc_page.write_task(task_name)

        assert_that(mvc_page.get_task_names(), has_item(task_name))

    @allure.title("Editar Tarea: Verificar que se pueda editar una tarea existente")
    def test_edit_an_existing_task(self, page: Page):
        """Edit an existing task.

        Editar Tarea: Verificar que se pueda editar una tarea existente
        """
        task_name = "Complete the challenge"
        new_task_name = "Edited task"
        mvc_page = TodoMVCPage(page=page)
        mvc_page.navigate()
        mvc_page.write_task(task_name)
        mvc_page.edit_task(task_name, new_task_name)
        assert_that(mvc_page.get_task_names(), has_item(new_task_name))

    @allure.title("Eliminar Tarea: Verificar que se pueda eliminar una tarea.")
    def test_complete_task(self, page: Page):
        """Complete multiple tasks.

        Eliminar Tarea: Verificar que se pueda eliminar una tarea.
        """
        tasks = [
            "Analyze Data with Pandas",
            "Develop a RESTful API with Flask",
            "Automate Office Tasks with Python",
            "Web Scraping with BeautifulSoup and Requests",
            "Develop a Basic Chat Bot",
        ]
        task_to_delete = tasks[random.randint(0, (len(tasks) - 1))]  # noqa: S311
        mvc_page = TodoMVCPage(page=page)
        mvc_page.navigate()
        mvc_page.create_multiple_tasks(tasks=tasks)
        mvc_page.complete_task(task_name=task_to_delete)
        assert_that(mvc_page.get_task_names(), is_not(has_item(task_to_delete)))

    @allure.title(
        "Validación de Campos: Verificar que se muestre un mensaje de error cuando se intenta agregar una tarea vacía"  # noqa: E501
    )
    def test_empty_task(self, page: Page):
        """Test empty task.

        Validación de Campos: Verificar que se muestre un mensaje de error
        cuando se intenta agregar una tarea vacía
        """
        mvc_page = TodoMVCPage(page=page)
        mvc_page.navigate()
        mvc_page.write_task(task="")

        assert_that(mvc_page.get_task_names(), empty())
