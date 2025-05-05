# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_typing.pil`
================================================================================

Type annotation definitions for PIL Images.

* Author(s): Alec Delaney
"""

from typing import Callable, Optional, Tuple

# Protocol was introduced in Python 3.8
from typing_extensions import Protocol


class PixelAccess(Protocol):
    """Type annotation for PIL's PixelAccess class"""

    # pylint: disable=invalid-name
    def __getitem__(self, xy: Tuple[int, int]) -> int:
        """Get pixels by x, y coordinate"""


class Image(Protocol):
    """Type annotation for PIL's Image class"""

    # pylint: disable=too-many-arguments,invalid-name
    @property
    def mode(self) -> str:
        """The mode of the image"""

    @property
    def size(self) -> Tuple[int, int]:
        """The size of the image"""

    def load(self) -> PixelAccess:
        """Load the image for quick pixel access"""

    def convert(
        self,
        mode: str,
        matrix: Optional[Tuple],
        dither: Callable,
        palette: int,
        colors: int,
    ):
        """Returns a converted copy of this image."""

    def rotate(
        self,
        angle: int,
        resampling,
        expand: int,
        center: Tuple[int, int],
        translate: Tuple[int, int],
        fillcolor: int,
    ):
        """Returns a rotated copy of this image."""

    def getpixel(self, xy: Tuple[int, int]):
        """Returns the pixel value at a given position."""
