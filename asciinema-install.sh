#!/bin/bash

check_os_release() {
    # Try /etc/os-release first, then /usr/lib/os-release as fallback
    if [ -f /etc/os-release ]; then
        . /etc/os-release
    elif [ -f /usr/lib/os-release ]; then
        . /usr/lib/os-release
    else
        echo "Error: os-release not found in /etc or /usr/lib"
        return 1
    fi

    case "$ID" in
        debian|ubuntu|linuxmint|pop|elementary)
            sudo apt install -y asciinema
            ;;
        fedora|rhel|centos|rocky|almalinux)
            sudo dnf install -y asciinema
            ;;
        opensuse*|suse)
            sudo zypper install -y asciinema
            ;;
        arch|manjaro|endeavouros)
            sudo pacman -Sy asciinema
            ;;
        alpine)
            sudo apk add -y --no-cache asciinema
            ;;
        *)
            echo "Unsupported distribution: $ID" 1>&2
            return 1
            ;;
    esac
}

# Usage with proper error handling
if install_cmd=$(check_os_release); then
    echo "Install with: $install_cmd"
    # To actually run: eval "$install_cmd"
else
    echo "Failed to determine package manager"
    exit 1
fi
