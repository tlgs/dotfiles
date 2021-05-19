import os
import subprocess
from typing import NamedTuple, Optional

from libqtile import bar, hook, layout, widget
from libqtile.config import Group, Key, Screen
from libqtile.lazy import lazy


############################
#          Utils           #
############################
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


############################
# General config variables #
############################
wmname = "Qtile"


############################
#          Hooks           #
############################
@hook.subscribe.startup_once
def autostart():
    script_path = os.path.expanduser("~/.config/qtile/autostart")
    subprocess.call([script_path])


############################
#           Keys           #
############################
mod = "mod4"
keys = []

# change window focus
keys.extend(
    [
        Key([mod], "h", lazy.layout.left()),
        Key([mod], "j", lazy.layout.down()),
        Key([mod], "k", lazy.layout.up()),
        Key([mod], "l", lazy.layout.right()),
        Key(["mod1"], "Tab", lazy.layout.next()),
    ]
)

# change window size / behaviour
keys.extend(
    [
        Key([mod, "control"], "h", lazy.layout.shrink()),
        Key([mod, "control"], "j", lazy.layout.shrink()),
        Key([mod, "control"], "k", lazy.layout.grow()),
        Key([mod, "control"], "l", lazy.layout.grow()),
        Key([mod, "control"], "n", lazy.layout.reset()),
        Key([mod, "control"], "m", lazy.layout.maximize()),
        Key([mod, "control"], "f", lazy.window.toggle_floating()),
    ]
)

# change window position
keys.extend(
    [
        Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
        Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ]
)

# other Qtile functions
keys.extend(
    [
        Key([mod], "space", lazy.next_layout()),
        Key([mod], "w", lazy.window.kill()),
        Key([mod, "control"], "r", lazy.restart()),
        Key([mod, "control"], "q", lazy.shutdown()),
    ]
)

# multimedia
keys.extend(
    [
        Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-")),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
        Key([], "XF86AudioPause", lazy.spawn("playerctl pause")),
        Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    ]
)

# brightness
keys.extend(
    [
        Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
    ]
)

# print
keys.extend(
    [
        Key(
            [],
            "Print",
            lazy.spawn("sh -c 'maim -u | xclip -selection clipboard -t image/png'"),
        ),
        Key(
            ["control"],
            "Print",
            lazy.spawn("sh -c 'maim -s | xclip -selection clipboard -t image/png'"),
        ),
    ]
)

# applications
keys.extend(
    [
        Key([mod], "Return", lazy.spawn("alacritty")),
        Key([mod], "t", lazy.spawn("thunderbird")),
        Key([mod], "f", lazy.spawn("firefox")),
        Key([mod], "r", lazy.spawn("rofi -show drun")),
        Key([mod], "BackSpace", lazy.spawn("screenlock")),
    ]
)


############################
#  Groups (& keybindings)  #
############################
groups = [Group(str(x)) for x in range(1, 10)]

# switch workspaces
keys.extend([Key([mod], "Tab", lazy.screen.next_group(skip_empty=True))])
for x in groups:
    keys.extend(
        [
            Key([mod], x.name, lazy.group[x.name].toscreen()),
            Key([mod, "shift"], x.name, lazy.window.togroup(x.name, switch_group=True)),
        ]
    )


############################
#         Layouts          #
############################
layout_defaults = dict(
    border_focus=spaceduck.foreground,
    border_normal=spaceduck.background,
    border_width=3,
    margin=10,
    single_border_width=0,
    single_margin=10,
)

layouts = [
    layout.MonadTall(**layout_defaults),
    layout.MonadWide(**layout_defaults),
    layout.Max(**layout_defaults),
]


############################
#       Bar & Widgets      #
############################
widget_defaults = dict(
    font="sans-serif bold",
    fontsize=16,
    foreground=spaceduck.foreground,
    padding=6,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(16),
                widget.Image(filename="~/.config/qtile/arch.png"),
                widget.Spacer(24),
                widget.GroupBox(
                    active=spaceduck.foreground,
                    block_highlight_text_color=spaceduck.background,
                    hide_unused=True,
                    highlight_method="block",
                    inactive=spaceduck.white.normal,
                    this_current_screen_border=spaceduck.blue.normal,
                    urgent_border=spaceduck.red.normal,
                    use_mouse_wheel=False,
                ),
                widget.Spacer(),
                widget.CheckUpdates(
                    colour_have_updates=spaceduck.white.normal,
                    custom_command="paru -Qu",
                    display_format="",
                    font="Font Awesome 5 Free",
                    update_interval=1200,
                ),
                widget.Spacer(),
                widget.Systray(icon_size=24, padding=8),
                widget.Spacer(24),
                widget.Clock(
                    format="%H:%M" + " " * 6 + "%b %d",
                ),
                widget.Spacer(16),
            ],
            size=48,
            background=spaceduck.background,
            margin=[10, 10, 0, 10],
        ),
    ),
]
