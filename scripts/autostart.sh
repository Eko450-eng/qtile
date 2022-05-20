#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}



#starting utility applications at boot time
lxsession &
run nm-applet &
run pamac-tray &
numlockx on &
blueman-applet &
#Set correct screen pos and size
# xrandr --output DP-0 --mode 3440x1440 -r 144 --pos 1920x0 --output DP-2 --pos 0x0 &

#Sets custom background
watch -n 300 feh --randomize --bg-fill ~/Pictures/wallpapers/* &>/dev/null &

#Start Emacs daemon
emacs /usr/bin/emacs --daemon &

#Disable mouse acceleration
xinput --set-prop "pointer:""Micro-Star INT'L CO., LTD. MSI GM41 Light Weight Wireless Mode Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput --set-prop "pointer:""Micro-Star INT'L CO., LTD. MSI GM41 Light Weight Wireless Mode Gaming Mouse" "libinput Accel Speed" -0.2 &

#Run Picom custom config
picom --config $HOME/.config/picom/picom.conf &
# picom --config .config/picom/picom-blur.conf --experimental-backends &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

#Run Notificansprovider
dunst &
# feh --randomize --bg-fill ~/Pictures/wallpapers/* &
# crontab -l 2>/dev/null; echo "* * * * * feh --bg-fill -randomize ~/Pictures/wallpapers/*" | crontab - &
#starting user applications at boot time

#Its a volumeicon duh?
run volumeicon &
