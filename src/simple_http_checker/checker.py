import logging
from collections.abc import Collection

import requests

logger = logging.getLogger(__name__)


def checkUrls(
    urls: Collection[str], timeout: int = 5
) -> dict[str, str]:
    """
    Veryfies a list of URLs and return the status for each.

    Args:
        urls: a list of string that contain the urls you wish to check.
        timeout: The maximum time in seconds to wait for a reply from the url. Default = 5 seconds.

    Returns:
        A dictionaty tha maps the url with its status returned.
    """

    logger.info(
        f"Starting check for {len(urls)} URLs with a timeout ot {timeout} seconds each."
    )

    results: dict[str, str] = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")

            response = requests.get(
                url, timeout=timeout
            )

            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(
                f"The URL: {url} timed out."
            )
        except requests.exceptions.ConnectionError:
            status = "CONNECTION ERROR"
            logger.warning(
                f"The URL: {url} had a connection error."
            )
        except (
            requests.exceptions.RequestException
        ) as e:
            status = (
                f"RQUEST ERROR: {type(e).__name__}"
            )
            logger.exception(
                f"An unexpected request error occured for {url}",
                True,
            )

        results[url] = status
        logger.debug(f"Checked: {url:<40} -> {status}")

    logger.info("URL check finished")
    return results
