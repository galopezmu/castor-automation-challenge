"""TodoMVC page module."""

import allure
import utils
from playwright.sync_api import Page


class TodoMVCPage:
    """TodoMVC Page."""

    TXT_TODO_INPUT = "#todo-input"
    TXT_TODO_LIST = "[data-testid='todo-item-label']"
    BTN_DELETE = ".destroy"
    BTN_CLEAR_COMPLETED = ".clear-completed"

    @property
    def title(self):
        """Get page title."""
        return self.page.title()

    def __init__(self, page: Page) -> None:
        """Create a new page instance.

        Parameters
        ----------
        page : Page
            Page to create

        """
        self.page = page
        page.set_viewport_size({"width": 1920, "height": 1080})

    @allure.step("Navegar hasta la página principal")
    def navigate(self):
        """Navigate to the main url."""
        self.page.goto("https://todomvc.com/examples/react/dist/")
        utils.attach_screenshot(self.page.screenshot(type="png"), "Main page")

    @allure.step("Escribir una tarea")
    def write_task(self, task: str):
        """Write a new task.

        Parameters
        ----------
        task : str
            Task to create

        """
        self.page.query_selector(self.TXT_TODO_INPUT).fill(task)
        self.page.keyboard.press("Enter")
        utils.attach_screenshot(self.page.screenshot(type="png"), "Created task")

    @allure.step("Editar una tarea")
    def edit_task(self, task_name: str, new_name: str):
        """Edit an specific task.

        Parameters
        ----------
        task_name : str
            Task to search
        new_name : str
            New name to assign

        """
        self.page.get_by_text(task_name).dblclick()
        self.page.keyboard.press("Control+a")
        self.page.keyboard.type(new_name, delay=100)
        utils.attach_screenshot(self.page.screenshot(type="png"), "Editing task")
        self.page.keyboard.press("Enter")
        utils.attach_screenshot(self.page.screenshot(type="png"), "Edited task")

    @allure.step("Obtener las tareas creadas")
    def get_task_names(self) -> list[str]:
        """Get all created tasks.

        Returns
        -------
        list[str]
            Tasks created

        """
        utils.attach_screenshot(self.page.screenshot(type="png"), "Tasks list")
        tasks = self.page.query_selector_all(self.TXT_TODO_LIST)
        return [task.text_content() for task in tasks]

    @allure.step("Crear multiples tareas")
    def create_multiple_tasks(self, tasks: list[str]):
        """Create multiple tasks.

        Parameters
        ----------
        tasks : list[str]
            Task list

        """
        for task in tasks:
            self.write_task(task=task)

    @allure.step("Completar una tarea")
    def complete_task(self, task_name: str):
        """Complete task by name.

        Parameters
        ----------
        task_name : str
            Task to complete

        """
        self.page.get_by_text(task_name).locator("xpath=..").get_by_role(
            "checkbox"
        ).click()
        self.page.query_selector(self.BTN_CLEAR_COMPLETED).click()
        utils.attach_screenshot(self.page.screenshot(type="png"), "Completed task")
