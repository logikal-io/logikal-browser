from pathlib import Path
from zipfile import ZipFile

from pytest_mock import MockerFixture

from logikal_browser import scenarios
from logikal_browser.config import BROWSER_VERSIONS
from logikal_browser.edge import EdgeBrowser, EdgeVersion


def test_install(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch('logikal_browser.edge.tmp_path', return_value=tmp_path)

    driver_zip_path = tmp_path / 'edgedriver.zip'
    with ZipFile(driver_zip_path, 'w') as driver_zip:
        driver_zip.writestr('msedgedriver', data='')

    mocker.patch('logikal_browser.edge.download', side_effect=[tmp_path, driver_zip_path])
    mocker.patch('logikal_browser.edge.run')

    browser = tmp_path / 'edge/opt/microsoft/msedge/microsoft-edge'
    browser.parent.mkdir(parents=True)
    browser.touch()

    version = EdgeVersion(version='test-version', install_path=tmp_path / 'install')
    assert version.path.exists()
    assert version.driver_path.exists()


def test_installed_version() -> None:
    browser = EdgeBrowser(version=EdgeVersion(), settings=scenarios.desktop.settings)
    assert browser.capabilities['browserVersion'] == BROWSER_VERSIONS['edge']
