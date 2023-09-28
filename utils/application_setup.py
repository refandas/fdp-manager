import flet
import utils.constants


def apply(page: flet.Page):
    page.title = utils.constants.APPLICATION_NAME
    page.theme_mode = flet.ThemeMode.DARK
    page.window_height = utils.constants.APPLICATION_WINDOW_HEIGHT
    page.window_width = utils.constants.APPLICATION_WINDOW_WIDTH
