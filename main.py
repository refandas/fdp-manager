import flet
import components.pages.merge
import components.pages.home
import components.routes
import utils.application_setup


def main(page: flet.Page) -> None:
    utils.application_setup.apply(page)

    # Set page routing
    page.on_route_change = lambda route: components.routes.change(route, page)
    page.on_view_pop = lambda view: components.routes.view_pop(view, page)
    page.go(page.route)


flet.app(target=main, assets_dir="assets")
