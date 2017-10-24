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

    if [ -d ./venv ]; then
        read -r -p "venv already exists. Do you want to recreate it? [y/N] " response
        case "$response" in
            [yY][eE][sS]|[yY])
                info "Deleting current venv\n"
                rm -rf ./venv/ 
                ;;
            *)
                setupKey
                ;;
        esac
    fi

    info "Creating virtualenv"
    (virtualenv -p ${1} venv) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Done!\n"
    info "Sourcing venv...\n"
    source ./venv/bin/activate

    case "$(python --version 2>&1)" in
        *" 3.5"*)
            ;;
        *)
            error "Python Version must be >= 3.5\n"
            error "Removing venv...\n"
            rm -rf ./venv/
            warning "KTHXBYE\n"
            exit 0
            ;;
    esac


    info "Installing requirements..."
    (pip install -r ../App/requirements.txt) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Installed requirements\n"
    info "Fixing broken things...\n"
    PYTHON_PATH=`ls ./venv/lib`
    cp -r "./venv/lib/${PYTHON_PATH}/site-packages/Crypto" "venv/lib/${PYTHON_PATH}/site-packages/Cryptodome"
    cp "./_raw_api.py" "venv/lib/${PYTHON_PATH}/site-packages/Crypto/Util/_raw_api.py"
    info "Installing pyinstaller straight from Github"
    (pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip) > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Finished!\n"
    deactivate
    setupKey
}


setupKey() {
    if [ -f ../App/res/server.public.key ]; then
        read -r -p "Server Keys already exist. Do you want to recreate them? [y/N] " response
        case "$response" in
            [yY][eE][sS]|[yY])
                rm -rf ../App/res/server.public.key
                [ -f ../API/bin/private.key ] && rm -rf ../API/bin/private.key
                ;;
            *)
                exit 0
                ;;
        esac
    fi
    info "Generating RSA Keys"
    (ssh-keygen -b 8192 -t rsa -f tmpkey -q -N "") > /dev/null 2>&1 &
    spinner $!
    echo -e "\n"
    success "Finished generating Keys!\n"
    info "Copying Keys...\n"
    cp ./tmpkey ../API/bin/private.key
    cp ./tmpkey.pub ../App/res/server.public.key
    rm -rf ./tmpkey*
    success "Done!\n"
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
        warning "KTHXBYE\n"
        exit 0
    else
        error "Unknown option '${1}'\n"
        exit 0
    fi
else
    error "Usage: supergirl.sh <setup/build> [python bin]\n"
    exit 0
fi
