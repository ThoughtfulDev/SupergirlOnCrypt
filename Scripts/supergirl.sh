#!/bin/bash

#COLORS
RED='\033[1;31m'
YELLOW='\033[1;33m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m'

banner() {
    clear
    echo -e "
       **************************
    .*##*:*####***:::**###*:######*.
   *##: .###*            *######:,##*
 *##:  :####:             *####*.  :##:
  *##,:########**********:,       :##:
   .#########################*,  *#*
     *#########################*##:
       *##,        ..,,::**#####:
        ,##*,*****,        *##*
          *#########*########:
            *##*:*******###*
             .##*.    ,##*
               :##*  *##,
                 *####:
                   :,
    \t    ${RED}SUPERGIRL${YELLOW}ONCRYPT
    \t      Version ${CYAN}0.0.1${NC}
    "
}

error() {
    printf "${RED}[!] ${1}${NC}"
}

warning() {
    printf "${YELLOW}[!] ${1}${NC}"
}

info() {
    printf "${CYAN}[-] ${1}${NC}"
}

success() {
    printf "${GREEN}[*] ${1}${NC}"
}


spinner() {
    local pid=$1
    local delay=0.225
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

setupVEnv() {
    info "Installing virtualenv...\n"
    sudo pip install virtualenv
    info "Creating virtualenv"
    (virtualenv -p ${1} venv) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Done!\n"
    info "Sourcing venv...\n"
    source ./venv/bin/activate
    info "Installing requirements..."
    (pip install -r ../App/requirements.txt) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Installed requirements\n"
    info "Fixing broken things...\n"
    cp -r ./venv/lib/python3.5/site-packages/Crypto venv/lib/python3.5/site-packages/Cryptodome
    cp ./_raw_api.py venv/lib/python3.5/site-packages/Crypto/Util/_raw_api.py
    info "Installing pyinstaller straight from Github"
    (pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Finished!\n"
    deactivate
    warning "KTHXBYE\n"
    exit 0
}

build() {
    source ./venv/bin/activate
    info "Building binary"
    (pyinstaller --clean --onefile --add-data="../App/tor_bin:tor_bin" --add-data="../App/res:res" ../App/SupergirlOnCrypt.py) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Finished!\n"
    deactivate
    warning "KTHXBYE\n"
    exit 0
}




banner

if [ $# -ge 1 ]; then
    if [ "$1" == "setup" ]; then
        info "Entering Setup Mode\n"
        if [ $# -eq 2 ]; then
            setupVEnv $2
        else 
            error "No python path\n"
            exit 0
        fi
    elif [ "$1" == "build" ]; then
        info "Entering Build Mode\n"
        build
    else
        error "Unknown option '${1}'\n"
        exit 0
    fi
else
    error "Usage: supergirl.sh <setup/build> [python bin]\n"
    exit 0
fi
