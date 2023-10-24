# Copyright (C) 2022 Adam Kirchberger
#
# This file is part of Nectl.
#
# Nectl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Nectl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nectl.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import shutil
from typing import Dict

from ..logging import get_logger


logger = get_logger()


def write_configs_to_dir(
    configs: Dict[str, str], output_dir: str, extension: str, replace=True
) -> int:
    """
    Writes supplied configs dict to an output directory using the key as the
    filename and value as content.

    Args:
        configs (Dict[str,str]): configs dict.
        output_dir (str): directory to write files to.
        extension (str): optional file extension to use.
        replace (bool): Delete any existing files when writing. Defaults to True.

    Returns:
        int: total created files.
    """
    total = 0
    ts_start = time.perf_counter()
    logger.debug("start writing config files")

    # Wipe output dir
    if replace:
        try:
            shutil.rmtree(output_dir)
            logger.debug(f"deleted output dir: {output_dir}")
        except FileNotFoundError:
            logger.debug(f"skipped delete output dir not found: {output_dir}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"writing config files to: {output_dir}")

    # Loop through each host config
    for host, conf in configs.items():
        if conf:
            filename = f"{output_dir}/{host}.{extension}"
            with open(filename, "w", encoding="utf-8") as fh:
                fh.write(conf)  # write config
                fh.write("\n")  # write config with newline at EOF
                logger.debug(f"config written to file: {filename}")
            total += 1

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished writing config files ({dur}s)")

    return total
