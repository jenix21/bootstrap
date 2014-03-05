
export LANG=en_US.utf8
export LC_ALL=en_US.utf8
set -o vi

alias listen="sudo lsof -i TCP | grep LISTEN"
alias lsjava="sudo ps -elf | grep java | grep -v 'grep'"

BLACK="\[\033[0;30m\]"
BLACKBOLD="\[\033[1;30m\]"
RED="\[\033[0;31m\]"
REDBOLD="\[\033[1;31m\]"
GREEN="\[\033[0;32m\]"
GREENBOLD="\[\033[1;32m\]"
YELLOW="\[\033[0;33m\]"
YELLOWBOLD="\[\033[1;33m\]"
BLUE="\[\033[0;34m\]"
BLUEBOLD="\[\033[1;34m\]"
PURPLE="\[\033[0;35m\]"
PURPLEBOLD="\[\033[1;35m\]"
CYAN="\[\033[0;36m\]"
CYANBOLD="\[\033[1;36m\]"
WHITE="\[\033[0;37m\]"
WHITEBOLD="\[\033[1;37m\]"

export PS1='\[\033[0;36m\]\u\[\033[00m\] in \[\033[0;36m\]$( pwd ) ($( OUT=$( ls -A | wc -l ); echo $OUT ) entries, $(( $( ls -A | wc -l ) - $( ls | wc -l ) )) hidden)\n\[\033[1;36m\]\# \! \$\[\033[;m\] '

source ~/.local/bin/bashmarks.sh
