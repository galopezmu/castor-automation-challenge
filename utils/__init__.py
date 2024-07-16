"""Utils module."""

import tempfile

import allure


def attach_screenshot(screenshot_bytes, name: str):
    """Attach an image to the report.

    Parameters
    ----------
    screenshot_bytes : bytes
        Screenshot bytes
    name : str
        Image name

    """
    with tempfile.TemporaryFile(suffix=".png") as tmp_image:
        tmp_image.write(screenshot_bytes)
        allure.attach.file(
            source=tmp_image.name, attachment_type=allure.attachment_type.PNG, name=name
        )
