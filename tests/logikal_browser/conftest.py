from collections.abc import Iterable
from contextlib import ExitStack
from pathlib import Path
from typing import Protocol

from pytest import fixture

from logikal_browser import Browser, Settings
from logikal_browser.chrome import ChromeBrowser
from logikal_browser.scenarios import desktop


class GetBrowserFixture(Protocol):
    def __call__(
        self,
        settings: Settings = ...,
        browser_class: type[Browser] = ...,
    ) -> Browser:
        ...


@fixture
def get_browser(tmp_path: Path) -> Iterable[GetBrowserFixture]:
    # Manage browser lifecycles using their native context managers
    with ExitStack() as stack:
        def get_browser_wrapper(
            settings: Settings = desktop.settings,
            browser_class: type[Browser] = ChromeBrowser,
        ) -> Browser:
            return stack.enter_context(browser_class(
                settings=settings,
                language='en-us',
                screenshot_path=Path(__file__).parent / 'screenshots/test',
                screenshot_tmp_path=tmp_path,
            ))

        yield get_browser_wrapper


@fixture
def browser(get_browser: GetBrowserFixture) -> Browser:  # pylint: disable=redefined-outer-name
    return get_browser()
