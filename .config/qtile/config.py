import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.config import Group, Key, Screen
from libqtile.lazy import lazy

import colors


color_scheme = colors.synthwave


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
        Key([mod, "control"], "j", lazy.layout.grow()),
        Key([mod, "control"], "k", lazy.layout.shrink()),
        Key([mod, "control"], "n", lazy.layout.reset()),
        Key([mod, "control"], "m", lazy.layout.maximize()),
        Key([mod, "control"], "f", lazy.window.toggle_floating()),
    ]
)

# change window position
keys.extend(
    [
        Key([mod, "shift"], "h", lazy.layout.swap_left()),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
        Key([mod, "shift"], "l", lazy.layout.swap_right()),
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
        Key([], "XF86AudioMute", lazy.spawn("volume toggle")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("volume up")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("volume down")),
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
        Key([mod], "r", lazy.spawn("rofi -show drun -modi drun,window")),
        Key([mod], "BackSpace", lazy.spawn("xset s activate")),
        Key([mod], "Escape", lazy.function(lambda q: q.cmd_hide_show_bar())),
    ]
)


############################
#  Groups (& keybindings)  #
############################
groups = [Group(i) for i in "1234567890"]

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
    border_focus=color_scheme.white.normal,
    border_normal=color_scheme.background,
    border_width=1,
    margin=10,
    max_ratio=0.85,
    min_ratio=0.15,
    single_border_width=0,
    single_margin=10,
)

layouts = [
    layout.MonadTall(**layout_defaults),
    layout.MonadWide(**layout_defaults),
]


############################
#       Bar & Widgets      #
############################
widget_defaults = dict(
    font="sans semibold",
    fontsize=14,
    foreground=color_scheme.foreground,
    padding=6,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(12),
                widget.AGroupBox(border=color_scheme.background),
                widget.Spacer(12),
                widget.WindowName(format="{name}"),
                widget.Spacer(bar.STRETCH),
                widget.Systray(icon_size=16, padding=10),
                widget.Spacer(12),
                widget.Sep(size_percent=69),
                widget.Spacer(12),
                widget.Clock(
                    format="%H:%M" + " " * 4 + "%b %d",
                ),
                widget.Spacer(12),
            ],
            size=24,
            background=color_scheme.background,
        ),
    ),
]

############################
# General config variables #
############################
floating_layout = layout.Floating(**layout_defaults)
follow_mouse_focus = False
wmname = "Qtile"

############################
#           Hooks          #
############################
@hook.subscribe.startup_once
def _():
    script_path = os.path.expanduser("~/.config/qtile/autostart")
    subprocess.call([script_path])
