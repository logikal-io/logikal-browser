from dataclasses import replace
from pathlib import Path

from pytest import mark, raises
from pytest_factoryboy import register
from pytest_logikal.django import LiveURL
from pytest_mock import MockerFixture
from selenium.webdriver.common.by import By

from logikal_browser import Browser, scenarios
from logikal_browser.chrome import ChromeBrowser, ChromeVersion
from logikal_browser.config import BROWSER_VERSIONS
from logikal_browser.edge import EdgeBrowser
from tests.logikal_browser import factories
from tests.logikal_browser.conftest import GetBrowserFixture
from tests.website.models import User

register(factories.UserFactory)


def test_version_error(mocker: MockerFixture) -> None:
    mocker.patch.dict(BROWSER_VERSIONS, clear=True)
    with raises(ValueError, match='browser version must be specified'):
        ChromeVersion()


@mark.parametrize('browser_class', [ChromeBrowser, EdgeBrowser])
def test_check(
    live_url: LiveURL,
    browser_class: type[Browser],
    get_browser: GetBrowserFixture,
) -> None:
    browser = get_browser(browser_class=browser_class)
    browser.get('https://www.sofia.hu/konyv/hamori-zsofia/nincs-ido')
    browser.check('check_nincs-ido')
    browser.get('https://www.sofia.hu/konyv/hamori-zsofia/perennrose')
    browser.check('check_perennrose')
    browser.get(live_url())
    browser.check('check_website')


@mark.parametrize('run', range(5))
def test_flakiness(run: int, live_url: LiveURL, browser: Browser) -> None:
    for cycle in range(5):
        print(f'Run {run} cycle {cycle}')
        browser.get(live_url())
        browser.check('flakiness')


def test_mobile(get_browser: GetBrowserFixture) -> None:
    browser = get_browser(settings=scenarios.mobile_l.settings)
    browser.get('https://www.sofia.hu/konyv/hamori-zsofia/nincs-ido')
    browser.check('mobile')


def test_not_full_page_height(get_browser: GetBrowserFixture) -> None:
    browser = get_browser(settings=replace(scenarios.desktop.settings, full_page_height=False))
    browser.get('https://www.sofia.hu/konyv/hamori-zsofia/nincs-ido')
    browser.check('not_full_page_height')


def test_replace_text(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url())
    header = browser.find_element(By.CSS_SELECTOR, 'h1')
    browser.replace_text(header, 'New Header')
    browser.check('replace_text')


def test_wait_for_element(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url())
    browser.wait_for_element(By.CSS_SELECTOR, 'h1')
    browser.check('wait_for_element')


def test_wait_for_download(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('downloads'))
    browser.check('downloads')
    browser.find_element(By.ID, 'download-words').click()
    browser.wait_for_download('words.txt')
    file_path = browser.download_path / 'words.txt'
    expected_file_path = Path(__file__).parents[1] / 'website/static/downloads/words.txt'
    assert file_path.exists()
    assert file_path.read_text() == expected_file_path.read_text()


def test_login(live_url: LiveURL, browser: Browser, user: User) -> None:
    browser.get(live_url('internal'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_url('internal'))
    browser.check('after_login')


@mark.django_db
def test_login_error(browser: Browser, user: User) -> None:
    with raises(NotImplementedError, match='Only the forced login is implemented'):
        browser.login(user, force=False)


def test_stop_videos(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('video'))
    browser.stop_videos()
    browser.check('video')


def test_stop_slideshows(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('slideshow'))
    browser.stop_slideshows('.hero-slideshow')
    browser.check('slideshow')
