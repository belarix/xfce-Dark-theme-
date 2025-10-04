#!/bin/sh

case "$1" in

# No flags. Build all to user's theme folder.
'')

# Check if ran as root but not running a system-wide install. Halt if so!
if [ "$(id -u)" -eq 0 ]; then printf "\nUser Install Selected But Invoked As Root!: Please run as user.\n\n" >&2; exit 1; fi

# Now build them
for i in ./presets/*.conf
do
sh ./gen_theme.sh "$i"
done
exit
;;

# System-wide Install.
--systeminstall)

# Check if ran elevated or not...
if [ "$(id -u)" -ne 0 ]; then printf "\nSystem Install Selected: Please run as root.\n\n" >&2; exit 1; fi

for i in ./presets/*.conf
do
sh ./gen_theme.sh "$i" --systeminstall
done
exit
;;

*)
printf "\nPlease run with --systeminstall to install all to system theme folder or with\nno arguments to install all to user theme folder.\n\n" >&2; exit 1
;;

esac



