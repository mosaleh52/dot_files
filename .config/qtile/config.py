# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.d

from typing import List  # noqa: F401

from libqtile import bar, layout, widget,qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen,KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess

from libqtile.widget.base import _Widget




# Get the number of connected screens


def get_monitors():
    xr = subprocess.check_output('xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


monitors = get_monitors()
####################

mod = "mod4"
terminal = 'alacritty'

keys = [
     # Toggle floating
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),desc="Toggle floating"),
        # Cycle through windows in the floating layout
    Key([mod, "shift"], "i",lazy.window.toggle_minimize(),lazy.group.next_window(),lazy.window.bring_to_front()),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    #Key([mod], "d",lazy.spawn('rofi -show drun') , desc="lunch rofi"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),desc="Spawn a command using a prompt widget"),
    ### Switch focus to specific monitor (out of three)
	#Key([mod], "z", lazy.to_screen(0), desc="Keyboard focus to monitor 1"),
	# Key([mod], "e", lazy.to_screen(1), desc="Keyboard focus to monitor 2"),
	# Key([mod], "r", lazy.to_screen(2), desc="Keyboard focus to monitor 3"),
	### Switch focus of monitors
	Key([mod], "p", lazy.next_screen(), desc="Move focus to next monitor"),
    #### switch layout
    #

    

    # rofi scripts
    KeyChord([mod], "e", [
            Key([], "d",lazy.spawn("rofi -show drun"),desc='open rofi drun'),
            Key([], "f",lazy.spawn("firefox"),desc='open firefox'),
            Key([], "s",lazy.spawn("xfce4-settings-manager"),desc='open sittengs'),
            Key([], "t", lazy.spawn("rofi -show window"),desc="lunch rofi win switcher"),
            Key([],"a",lazy.spawn("anki")),
            Key([],"o",lazy.spawn("/home/mo/Programs/Obsidian-0.12.19.AppImage")),
            Key([],'v',lazy.spawn("virtualbox")),
            Key([],"z",lazy.spawn("vboxmanage startvm 'androidx68'")),
            Key([],"l",lazy.spawn("xflock4")),
            Key([],"c",lazy.spawn("code")),
            Key([],"m", lazy.widget["keyboardlayout"].next_keyboard(), desc='Next keyboard layout.'),
        
        ])

]
# Move window to screen with Mod, Alt and number


for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i+1), lazy.window.toscreen(i))])

# groups names
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 2,
                "fullscreen_border_width": 0,
                "single_border_width": 0,
                "single_margin": 0,
                "margin": 3,
                "border_focus": "#88c0d0",
                "border_normal": "#1D2330"
                }    

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
    background = "#2e3440" 
)
extension_defaults = widget_defaults.copy()
######## defin function for opening rofi using mouse calbake
def open_rofi():
    qtile.cmd_spawn("rofi -show drun")
######## fun for prayer times in qbar

def get_prayer():
    n_prayer = subprocess.check_output('next-prayer -i', shell=True).decode().replace("\n", "").replace("AM",'').replace("PM",'')
    r_time = subprocess.check_output('next-prayer -l', shell=True).decode().replace("\n", "")[:5]
    out_put = f'{n_prayer}⏱️{r_time}'
    return out_put





screens = [
    Screen(
        top=bar.Bar(
               [widget.Sep(
                linewidth = 0,
                padding = 1,
                foreground = ["#ffffff", "#ffffff"],
                background = ["#2e3440","#2e3440"]
                ),
                widget.Image(
                filename = "~/.config/qtile/icons/but.png",
                scale = "False",
                mouse_callbacks = {'Button1':open_rofi ,}
                ),
                widget.CurrentLayoutIcon(scale=.6, padding = 1),
                widget.CurrentScreen(active_text='I',inactive_color='#bf616a',active_color='#a3be8c'),
                #widget.GroupBox(hide_unused=True,margin =3 ,padding = .5),
                widget.AGroupBox(margin =3 ,padding = .5,borderwidth=.01,border='#ffffff'),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(),
                widget.Systray(),
                widget.PulseVolume(),
                widget.Pomodoro(color_active='#a3be8c',color_inactive='#bf616a'),
                widget.KeyboardLayout(configured_keyboards=["us","ar"]),
                widget.GenPollText(func = get_prayer,update_interval = 60 ),
                widget.Clock(format='⏰%I:%M',),
                #widget.GenPollText(func = get_time,update_interval = 1,
                #mouse_callbacks ={"Button1":stop_time}
                #),
            ],
            20,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
            widget.Sep(
                linewidth = 0, padding = 1,foreground = ["#ffffff", "#ffffff"],background = ["#2e3440","#2e3440"]),
                widget.CurrentLayoutIcon(scale=.6, padding = 1),
                widget.CurrentScreen(active_text='I',inactive_color='#bf616a',active_color='#a3be8c'),
                widget.GroupBox(hide_unused=True,margin =3 ,padding = .5),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),

                
                        ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='conky(mo-lab)'), 
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"

