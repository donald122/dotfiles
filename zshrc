# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
  export ZSH=~/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"
# ZSH_THEME="agnoster"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

eval $(thefuck --alias)
keychain --nogui --quiet id_ed25519 id_rsa
# time command setting
TIMEFMT=$'\nreal\t%*E\nuser\t%*U\nsys\t%*S'

##########################################################################
#
# Recreate SSH_AUTH_SOCK
##########################################################################
SOCK="/tmp/ssh-agent-$USER-screen"
if test $SSH_AUTH_SOCK && [ $SSH_AUTH_SOCK != $SOCK ]
then
    env | grep ssh_auth_sock || ln -sf $SSH_AUTH_SOCK ~/.ssh/ssh_auth_sock
fi

export SSH_AUTH_SOCK=~/.ssh/ssh_auth_sock

##########################################################################
#
# Fix Display
##########################################################################

#function get_display {
#    ps -u $(id -u) -o pid= | \
#        while read pid; do
#            cat /proc/$pid/environ 2>/dev/null | tr '\0' '\n' | grep '^DISPLAY=:'
#        done | grep -o ':[0-9]*' | sort -u
#}

#tmux setenv DISPLAY $(get_display)

###########################################################################
#
# Alias
###########################################################################
alias pview="ssh -t 192.168.8.139 pview"
alias wgtn="export OS_REGION_NAME=nz_wlg_2"
alias por="export OS_REGION_NAME=nz-por-1"
alias hlz="export OS_REGION_NAME=nz-hlz-1"
alias kv2='OS_AUTH_URL=https://api.cloud.catalyst.net.nz:5000/v2.0; export OS_IDENTITY_API_VERSION=2'
alias kv3='OS_AUTH_URL=https://api.cloud.catalyst.net.nz:5000/; export OS_IDENTITY_API_VERSION=3'
alias icingatime="perl -pe 's/(\d+)/localtime($1)/e'"
# tmuxcp 0:2.1 | head  # or can use 0:name.1
alias tmuxcp="tmux capture-pane -pS -100000 -t"

###########################################################################
#
# History options
###########################################################################
unsetopt share_history
