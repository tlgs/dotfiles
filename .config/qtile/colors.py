from typing import NamedTuple, Optional


class Color(NamedTuple):
    normal: str
    bright: Optional[str] = None


class Colorscheme(NamedTuple):
    background: str
    foreground: str
    black: Color
    red: Color
    green: Color
    yellow: Color
    blue: Color
    magenta: Color
    cyan: Color
    white: Color


mono_white = Colorscheme(
    "#262626",
    "#fafafa",
    Color("#3b3b3b", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
    Color("#fafafa", "#fafafa"),
)

spaceduck = Colorscheme(
    "#0f111b",
    "#ecf0c1",
    Color("#000000", "#686f9a"),
    Color("#e33400", "#e33400"),
    Color("#5ccc96", "#5ccc96"),
    Color("#b3a1e6", "#b3a1e6"),
    Color("#00a3cc", "#00a3cc"),
    Color("#f2ce00", "#f2ce00"),
    Color("#7a5ccc", "#7a5ccc"),
    Color("#686f9a", "#f0f1ce"),
)

synthwave = Colorscheme(
    "#262335",
    "#ffffff",
    Color("#011627", "#575656"),
    Color("#fe4450", "#fe4450"),
    Color("#72f1b8", "#72f1b8"),
    Color("#fede5d", "#fede5d"),
    Color("#03edf9", "#03edf9"),
    Color("#ff7edb", "#ff7edb"),
    Color("#03edf9", "#03edf9"),
    Color("#ffffff", "#ffffff"),
)
