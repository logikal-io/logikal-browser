from pathlib import Path
from zipfile import ZipFile

from pytest_mock import MockerFixture

from logikal_browser import scenarios
from logikal_browser.chrome import ChromeBrowser, ChromeVersion
from logikal_browser.config import BROWSER_VERSIONS


def test_install(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch('logikal_browser.chrome.tmp_path', return_value=tmp_path)

    browser_zip_path = tmp_path / 'chrome.zip'
    with ZipFile(browser_zip_path, 'w') as browser_zip:
        browser_zip.writestr('chrome-linux64/chrome', data='')

    driver_zip_path = tmp_path / 'chromedriver.zip'
    with ZipFile(driver_zip_path, 'w') as driver_zip:
        driver_zip.writestr('chromedriver-linux64/chromedriver', data='')

    mocker.patch('logikal_browser.chrome.download', side_effect=[
        browser_zip_path,
        driver_zip_path,
    ])
    version = ChromeVersion(version='test-version', install_path=tmp_path / 'install')
    assert version.path.exists()
    assert version.driver_path.exists()


def test_installed_version() -> None:
    browser = ChromeBrowser(version=ChromeVersion(), settings=scenarios.desktop.settings)
    assert browser.capabilities['browserVersion'] == BROWSER_VERSIONS['chrome']
    assert browser.version.name in str(browser.version)
    assert browser.version.name in repr(browser.version)
