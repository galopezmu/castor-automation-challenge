"""Test selenium module."""

import allure
import pytest
import utils
from hamcrest import assert_that, has_item, has_items
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


@allure.suite("Mejora script Selenium")
class TestSelenium:
    """Castor test selenium."""

    # Create locators
    TXT_TASK_NAME = (By.CSS_SELECTOR, "#todo-input")
    TXT_TASKS_LIST = (By.CSS_SELECTOR, "[data-testid='todo-item-label']")

    # Create constans for the test
    TASKS = (
        "Analyze Data with Pandas",
        "Develop a RESTful API with Flask",
        "Automate Office Tasks with Python",
        "Web Scraping with BeautifulSoup and Requests",
        "Develop a Basic Chat Bot",
    )

    @pytest.fixture(scope="class")
    def webdriver(self):
        """Webdriver fixture.

        Yields
        ------
        WebDriver
            webdriver instance

        """
        driver: WebDriver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://todomvc.com/examples/react/dist/")
        yield driver
        driver.close()

    def create_task(self, wait: WebDriverWait, task_name: str):
        """Create a new task.

        Parameters
        ----------
        wait : WebDriverWait
            Webdriver wait instance
        task_name : str
            Task name

        """
        # Adding a new task
        task_input: WebElement = wait.until(
            ec.presence_of_element_located(self.TXT_TASK_NAME)
        )
        task_input.send_keys(task_name)
        task_input.send_keys(Keys.RETURN)

    def get_all_tasks(self, wait: WebDriverWait) -> list[str]:
        """Get all created tasks.

        Parameters
        ----------
        wait : WebDriverWait
            Webdriver wait instance

        Returns
        -------
        list[str]
            Tasks list

        """
        # Get all tasks
        task_list: list[WebElement] = wait.until(
            ec.presence_of_all_elements_located(self.TXT_TASKS_LIST)
        )

        return [task.text for task in task_list]

    @allure.title("Crear una nueva tarea")
    def test_task_selenium(self, webdriver):
        """Create a task with selenium."""
        # Create variables
        task_name = "Complete the challenge"

        # Add webdriverwait to wait correctly the elements
        wait = WebDriverWait(webdriver, timeout=10)
        utils.attach_screenshot(webdriver.get_screenshot_as_png(), "First screenshot")

        # Create new task
        self.create_task(wait=wait, task_name=task_name)

        utils.attach_screenshot(webdriver.get_screenshot_as_png(), "Second screenshot")

        # Assert task
        assert_that(self.get_all_tasks(wait=wait), has_item(task_name))

    @allure.title("Crear multiples tareas")
    def test_tasks_selenium(self, webdriver):
        """Create a task with selenium."""
        # Add webdriverwait to wait correctly the elements
        wait = WebDriverWait(webdriver, timeout=10)
        utils.attach_screenshot(webdriver.get_screenshot_as_png(), "First screenshot")

        # Adding new tasks
        for task in self.TASKS:
            self.create_task(wait=wait, task_name=task)

        utils.attach_screenshot(webdriver.get_screenshot_as_png(), "Second screenshot")

        # Assert task
        assert_that(self.get_all_tasks(wait=wait), has_items(*self.TASKS))
