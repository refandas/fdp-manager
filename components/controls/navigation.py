import flet
from enum import Enum


class IndexMenu(Enum):
    HOME = 0
    MERGE = 1
    SPLIT = 2
    REDUCE = 3


class Menu(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.navigation_menu = flet.NavigationRail()

    def navigation_action(self, event: flet.ControlEvent) -> None:
        if event.control.selected_index == IndexMenu.HOME.value:
            self.page.go("/")
        elif event.control.selected_index == IndexMenu.MERGE.value:
            self.page.go("/merge")
        elif event.control.selected_index == IndexMenu.SPLIT.value:
            self.page.go("/split")
        elif event.control.selected_index == IndexMenu.REDUCE.value:
            self.page.go("/reduce")

    def did_mount(self) -> None:
        self.navigation_menu.on_change = lambda event: self.navigation_action(event)

    def build(self) -> flet.NavigationRail:
        self.navigation_menu.destinations = [
            flet.NavigationRailDestination(
                icon=flet.icons.HOME_ROUNDED,
                label="Home",
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.CALL_MERGE_ROUNDED,
                label="Merge PDF",
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.CALL_SPLIT_ROUNDED,
                label="Split PDF"
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.PHOTO_SIZE_SELECT_SMALL_ROUNDED,
                label="Reduce PDF"
            )
        ]
        return self.navigation_menu
