import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import config, layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')
myTerm = "alacritty" # My terminal of choice

keys = [

    Key([mod], "b", lazy.spawn('brave')),
    Key([mod], "e", lazy.spawn('emacsclient -c -a "emacs"')),
    Key([mod], "Escape", lazy.spawn('betterlockscreen -l')),
    Key([mod], 'space', lazy.next_screen()),

    Key([mod], "m", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "t", lazy.spawn('alacritty')),
    Key([mod], "g", lazy.spawn(home + "/.config/qtile/scripts/checkForGlava.sh glava")),
    Key([mod], "r", lazy.restart()),
    # Key([mod], "v", lazy.spawn('pavucontrol')),
    # Key([mod], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    # Key([mod], "d", lazy.spawn('dmenu_run')),
    # Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn('alacritty')),
    Key([mod], "KP_Enter", lazy.spawn('alacritty')),

    Key([mod, "control"], "d", lazy.spawn("rofi -show window")),
    Key([mod, "control"], "r", lazy.restart()),

    Key([mod, "shift"], "Return", lazy.spawn('nautilus')),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show calc -no-show-match -no-sort")),
    Key([mod, "shift"], "g", lazy.spawn('killall glava')),
    # Key([mod, "shift"], "d", lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'")),
    # Key([mod, "shift"], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    # Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift", "control"], "x", lazy.shutdown()),

    Key(["mod1", "control"], "o", lazy.spawn(home + '/.config/qtile/scripts/picom-toggle.sh')),
    Key(["mod1", "control"], "t", lazy.spawn('xterm')), #Fallback terminal
    Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),

    Key(["mod1"], "p", lazy.spawn('pamac-manager')),
    # Key(["mod1"], "f", lazy.spawn('firedragon')),
    # Key(["mod1"], "m", lazy.spawn('pcmanfm')),
    # Key(["mod1"], "w", lazy.spawn('garuda-welcome')),

    # Key([mod2, "shift"], "Escape", lazy.spawn('lxtask')),

    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
    Key([mod2], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

    # Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +5%")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%- ")),

    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([mod], "c", lazy.spawn("playerctl play-pause")),
    Key([mod, "shift"], "v", lazy.spawn("playerctl next")),
    Key([mod, "shift"], "x", lazy.spawn("playerctl previous")),

#    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
#    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
#    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
#    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    # Key([mod], "n", lazy.layout.normalize()),
    # Key([mod], "space", lazy.next_layout()),

    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    # Key([mod, "shift"], "f", lazy.layout.flip()),

    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'
        ),

    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    Key([mod, "shift"], "space", lazy.window.toggle_floating()),]

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
group_labels = ["???", "???", "???", "???", "???", "???", "???", "???", "9", "???",]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
groups = []

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

def init_colors():
    return [["#1c2023", "#1c2023"], #0
            ["#c7ccd1", "#c7ccd1"], #1
            ["#c0c5ce", "#c0c5ce"], #2
            ["#ff5050", "#ff5050"], #3
            ["#1c2023", "#1c2023"], #4
            ["#ffffff", "#ffffff"], #5
            ["#ffd47e", "#ffd47e"], #6
            ["#95c7ae", "#95c7ae"], #7
            ["#000000", "#000000"], #8
            ["#c23127", "#c23127"], #9
            ["#6790eb", "#6790eb"], #10
            ["#c7ae95", "#c7ae95"], #11
            ["#4c566a", "#4c566a"], #12
            ["#282c34", "#282c34"], #13
            ["#212121", "#212121"], #14
            ["#4c566a", "#4c566a"], #15
            ["#2aa899", "#2aa899"], #16
            ["#abb2bf", "#abb2bf"], #17
            ["#81a1c1", "#81a1c1"], #18
            ["#56b6c2", "#56b6c2"], #19
            ["#1c2023", "#1c2023"], #20
            ["#245361", "#245361"], #21
            ["#4c566a", "#4c566a"], #22
            ["#282c34", "#282c34"]] #23

colors = init_colors()

def aurora_colors():
    return [
        ["#BF616A", "#BF616A"],
        ["#D08770", "#D08770"],
        ["#EBCB8B", "#EBCB8B"],
        ["#A3BE8C", "#A3BE8C"],
        ["#B48EAD", "#B48EAD"]
    ]
aurora_pallet = aurora_colors()

aurora_pallete = [
    "#BF616A",
    "#D08770",
    "#EBCB8B",
    "#A3BE8C",
    "#B48EAD"
]

def init_layout_theme():
    return {"margin":10,
            "border_width":0,
            "border_focus": aurora_pallete[3],
            "border_normal": aurora_pallete[0]
            # "border_focus": "#2aa899",
            # "border_normal": "#81a1c1"
            }

layout_theme = init_layout_theme()

layouts = [
    # layout.Spiral(new_client_position="bottom", margin=8, border_width=2, border_focus="#2aa889", border_normal="#81a1c1"),
    layout.MonadTall(margin=8, border_width=2, border_focus=aurora_pallete[3], border_normal=aurora_pallete[0]),
    # layout.MonadWide(margin=8, border_width=2, border_focus="#2aa899", border_normal="#81a1c1"),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Max(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Stack(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(
    #     sections=['FIRST', 'SECOND'],
    #     bg_color = '#141414',
    #     active_bg = '#0000ff',
    #     inactive_bg = '#1e90ff',
    #     padding_y =5,
    #     section_top =10,
    #     panel_width = 280),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

def base(fg='text', bg='dark'):
    return {'foreground': colors[14],'background': colors[15]}

def init_widgets_defaults():
    return dict(font="Montserrat",
                fontsize = 4,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list_minimal():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

                widget.Sep(
                    linewidth = 1,
                    padding = 10,
                    foreground = colors[15],
                    background = colors[15]
                ),

                widget.Image(
                    filename = "~/.config/qtile/icons/garuda-red.png",
                    iconsize = 9,
                    background = colors[15],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('jgmenu_run')}
                ),

                widget.GroupBox(
                    **base(bg=colors[15]),
                    font='UbuntuMono Nerd Font',

                    fontsize = 13,
                    margin_y = 3,
                    margin_x = 2,
                    padding_y = 5,
                    padding_x = 4,
                    borderwidth = 3,

                    active=colors[5],
                    inactive=colors[5],
                    rounded= True,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=colors[16],
                    this_current_screen_border=colors[20],
                    this_screen_border=colors[17],
                    other_current_screen_border=colors[13],
                    other_screen_border=colors[17],
                    disable_drag=True
                ),

                widget.TaskList(
                    highlight_method = 'border',
                    icon_size=0,
                    max_title_width=150,
                    rounded=True,
                    padding_x=0,
                    padding_y=0,
                    margin_y=0,
                    fontsize=12,
                    border=colors[14],
                    foreground=colors[14],
                    margin=2,
                    txt_floating='????',
                    txt_minimized='>_ ',
                    borderwidth = 1,
                    background=colors[14],
                ),

                widget.TextBox(
                    text="???",
                    fontsize=50,
                    foreground="#485262",
                    background=colors[14],
                    padding=0,
                ),

                widget.NvidiaSensors(
                    padding=0,
                    fontsize=14,
                    background=colors[22],
                ),

                widget.Clock(
                    foreground = colors[5],
                    background = colors[23],
                    fontsize = 10,
                    format="%H:%M"
                ),

                widget.CPU(
                    font="Noto Sans",
                    update_interval = 1,
                    fontsize = 10,
                    foreground = colors[5],
                    background = colors[22],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e zenith')},
                ),

                widget.Memory(
                    font="Noto Sans",
                    format = '{MemUsed: .0f}M/{MemTotal: .0f}M',
                    update_interval = 1,
                    fontsize = 10,
                    measure_mem = 'M',
                    foreground = colors[5],
                    background = colors[23],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e zenith')},
                ),

                widget.Clock(
                    foreground = colors[5],
                    background = colors[22],
                    fontsize = 12,
                    format="%d.%m.%Y"
                ),
              ]
    return widgets_list

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

                widget.Sep(
                    linewidth = 1,
                    padding = 10,
                    foreground = colors[15],
                    background = colors[15]
                ),

                widget.Image(
                    filename = "~/.config/qtile/icons/dnanordsmall.png",
                    iconsize = 9,
                    background = colors[15],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('jgmenu_run')}
                ),

                widget.GroupBox(
                    **base(bg=colors[14]),
                    font='UbuntuMono Nerd Font',

                    fontsize = 15,
                    margin_y = 3,
                    margin_x = 2,
                    padding_y = 5,
                    padding_x = 4,
                    borderwidth = 3,

                    active=colors[5],
                    inactive=colors[5],
                    rounded= True,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=colors[16],
                    this_current_screen_border=colors[20],
                    this_screen_border=colors[17],
                    other_current_screen_border=colors[13],
                    other_screen_border=colors[17],
                    disable_drag=True
                ),

                widget.TaskList(
                    highlight_method = 'border',
                    icon_size=0,
                    max_title_width=150,
                    rounded=True,
                    padding_x=0,
                    padding_y=0,
                    margin_y=0,
                    fontsize=14,
                    border=colors[0],
                    foreground=colors[14],
                    margin=2,
                    txt_floating='????',
                    txt_minimized='>_ ',
                    borderwidth = 1,
                    background=colors[14],
                ),

                widget.TextBox(
                    text="Staying busy is laziness because you stay busy to avoid something you don't want to face",
                    fontsize=12,
                    foreground="#ffffff",
                    background=colors[14],
                    padding=0,
                ),

                widget.TextBox(
                    text="???",
                    fontsize=50,
                    foreground="#272D33",
                    background=colors[14],
                    padding=0,
                ),

                # widget.CryptoTicker(
                #     background=colors[23],
                #     crypto="ETH",
                #     symbol="???",
                #     currency="EUR",
                #     fontsize="14",
                # ),

                widget.Cmus(
                    play_color=colors[16],
                    noplay_color=colors[22],
                    background=colors[22],
                ),

                widget.Clock(
                    foreground = colors[5],
                    background = colors[23],
                    fontsize = 12,
                    format="%H:%M",
                ),

                widget.CPU(
                    font="Noto Sans",
                    update_interval = 1,
                    fontsize = 12,
                    foreground = colors[5],
                    background = colors[22],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e zenith')},
                ),

                widget.Memory(
                    font="Noto Sans",
                    format = '{MemUsed: .0f}M/{MemTotal: .0f}M',
                    update_interval = 1,
                    fontsize = 12,
                    measure_mem = 'M',
                    foreground = colors[5],
                    background = colors[23],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e zenith')},
                ),

                widget.Clock(
                    foreground = colors[5],
                    background = colors[22],
                    fontsize = 12,
                    format="%d.%m.%Y"
                ),

                widget.Systray(
                    background=colors[23],
                    icon_size=20,
                    padding = 4
                ),
              ]
    return widgets_list

widgets_list = init_widgets_list()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list_minimal()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()

def init_screens():
    return [Screen(top=bar.Bar
                   (widgets=init_widgets_screen1(),
                    size=20,
                    opacity=0.85,
                    background= "000000")),
            Screen(top=bar.Bar
                   (widgets=init_widgets_screen2(),
                    size=15,
                    opacity=0.85,
                    background= "000000"))]
screens = init_screens()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",]
    d["2"] = ["emacs", "Emacs", "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",]
    d["3"] = ["rambox", "Rambox", "ferdi", "Ferdi", "Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",]
    d["4"] = ["Gimp", "gimp", "youtube music", "Youtube Music" ]
    d["5"] = ["Minecraft* 1.18.2", "Minecraft* 1.18.2", "Minecraft* 1.18.2", "Minecraft* 1.18.2", "Meld", "meld", "org.gnome.meld" "org.gnome.Meld",]
    d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
    d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer", "virtualbox manager", "virtualbox machine", "vmplayer", ]
    d["8"] = ["pcmanfm", "Nemo", "Caja", "Pcmanfm", "Pcmanfm-qt", "pcmanfm", "nemo", "caja", "pcmanfm", "pcmanfm-qt", ]
    d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird", "evolution", "geary", "mail", "thunderbird" ]
    d["0"] = ["zoom", "Zoom" ]

    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen()

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
    subprocess.call([home + '/.config/qtile/scripts/monitors.sh'])

to_position = config.Match(wm_class="GLava")
@hook.subscribe.client_managed
def _GLAVA(win):
    if win.match(to_position):  # Find matching windows
        win.cmd_static(1, 3540, 1180, 1720, 200)

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog",]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='zoom '),
    Match(wm_class='pavucontrol'),
    Match(wm_class='Zoom '),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),
],  fullscreen_border_width = 2, border_width = 2)
auto_fullscreen = True

focus_on_window_activation = "never" # or smart

wmname = "LG3D"
