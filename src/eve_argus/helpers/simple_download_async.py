"""Simple functions to download from a web server."""

import asyncio
import logging
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import perf_counter
from typing import Any

import aiohttp

from eve_argus.helpers.expand_multidict import ExpandedHeaders, expand_multi_dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

type SimpleText = tuple[str, ExpandedHeaders]
type SimpleJSON = tuple[Any, ExpandedHeaders]


async def download_file(
    url: str,
    *,
    headers: dict[str, str],
    file_path: Path,
    overwrite: bool = False,
) -> ExpandedHeaders:
    """Download a file from a URL and save it to disk.

    Args:
        url: The URL to download the file from.
        headers: The headers to include in the request.
        session: An optional aiohttp ClientSession to use for the request.
        file_path: The path to save the downloaded file to.
        overwrite: Whether to overwrite the file if it already exists.

    Returns:
        The expanded headers from the response.
    """
    logger.info(f"Downloading file from {url}")
    if file_path.is_dir():
        raise IsADirectoryError(f"File path {file_path} is a directory.")
    if file_path.exists() and not overwrite:
        logger.info(f"File {file_path} already exists and overwrite is False. {url=}")
        raise FileExistsError(
            f"File {file_path} already exists and overwrite is False."
        )
    file_path.parent.mkdir(parents=True, exist_ok=True)
    start = perf_counter()

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, allow_redirects=True) as response:
            logger.debug(
                "Received response with status %s, reason %s from %s, headers=%r",
                response.status,
                response.reason,
                response.real_url,
                response.headers,
            )
            response.raise_for_status()
            # atomic write to temp file, then move to final location
            try:
                with NamedTemporaryFile() as tmp_file:
                    tmp_file.write(await response.read())
                    tmp_file.flush()
                    shutil.copyfile(tmp_file.name, file_path)
            except Exception as e:
                logger.error(f"Error writing file to {file_path}: {e}")
                raise e
            finally:
                if os.path.exists(tmp_file.name):
                    os.remove(tmp_file.name)

            logger.info(
                f"Downloaded and wrote file from {url} to {file_path} in {perf_counter() - start:.2f} seconds"
            )
            expanded_headers = expand_multi_dict(response.headers)  # type: ignore
    await asyncio.sleep(0)  # yield control to event loop
    return expanded_headers


async def download_text(url: str, *, headers: dict[str, str]) -> SimpleText:
    """Download a text file from a URL and return its content as a string."""
    logger.info(f"Downloading text from {url}")
    start = perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            logger.debug(
                "Received response with status %s, reason %s from %s, headers=%r",
                response.status,
                response.reason,
                response.real_url,
                response.headers,
            )
            response.raise_for_status()
            text = await response.text()
            logger.info(
                f"Downloaded text from {url} in {perf_counter() - start:.2f} seconds"
            )
            result_headers = expand_multi_dict(response.headers)  # type: ignore
    await asyncio.sleep(0)  # yield control to event loop
    return (text, result_headers)


async def download_json(url: str, *, headers: dict[str, str]) -> SimpleJSON:
    """Download JSON data from a URL."""
    logger.info(f"Downloading JSON from {url}")
    start = perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            logger.debug(
                "Received response with status %s, reason %s from %s, headers=%r",
                response.status,
                response.reason,
                response.real_url,
                response.headers,
            )
            response.raise_for_status()
            json_data = await response.json()
            logger.info(
                f"Downloaded json from {url} in {perf_counter() - start:.2f} seconds"
            )
            result_headers = expand_multi_dict(response.headers)  # type: ignore
    await asyncio.sleep(0)  # yield control to event loop
    return (json_data, result_headers)
