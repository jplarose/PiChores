#!/bin/bash

# PiChore Dependency Installation Script
# This script installs all necessary dependencies for PiChore on Raspberry Pi OS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running on Raspberry Pi
check_platform() {
    if [[ ! -f /proc/device-tree/model ]] || ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_warning "This script is designed for Raspberry Pi OS, but we'll try to continue anyway..."
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Running on Raspberry Pi - good to go!"
    fi
}

# Function to check if user has sudo privileges
check_sudo() {
    if ! sudo -n true 2>/dev/null; then
        print_error "This script requires sudo privileges. Please run with sudo or ensure your user is in the sudo group."
        exit 1
    fi
}

# Function to update system packages
update_system() {
    print_status "Updating system packages..."
    sudo apt update
    sudo apt upgrade -y
    print_success "System packages updated"
}

# Function to install Python and PyQt5
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Install Python 3 and pip if not already installed
    sudo apt install -y python3 python3-pip python3-venv
    
    # Install PyQt5 and related packages
    sudo apt install -y python3-pyqt5 python3-pyqt5.qtwidgets python3-pyqt5.qtcore python3-pyqt5.qtgui
    
    # Install additional PyQt5 components that might be needed
    sudo apt install -y python3-pyqt5.qtquick python3-pyqt5.qtopengl
    
    print_success "Python dependencies installed"
}

# Function to install SQLite
install_sqlite() {
    print_status "Installing SQLite..."
    sudo apt install -y sqlite3 libsqlite3-dev
    print_success "SQLite installed"
}

# Function to install additional system dependencies
install_system_deps() {
    print_status "Installing additional system dependencies..."
    
    # Install libraries that might be needed for touchscreen support
    sudo apt install -y libqt5gui5 libqt5widgets5 libqt5core5a
    
    # Install X11 and display-related packages (for touchscreen)
    sudo apt install -y xorg xinput x11-xserver-utils
    
    # Install audio libraries (in case we add sound notifications later)
    sudo apt install -y libasound2-dev
    
    print_success "System dependencies installed"
}

# Function to set up permissions for touchscreen
setup_touchscreen_permissions() {
    print_status "Setting up touchscreen permissions..."
    
    # Add user to input group for touchscreen access
    sudo usermod -a -G input $USER
    
    # Create udev rule for touchscreen devices
    sudo tee /etc/udev/rules.d/99-touchscreen.rules > /dev/null <<EOF
# Touchscreen permissions for PiChore
SUBSYSTEM=="input", GROUP="input", MODE="0664"
KERNEL=="event*", SUBSYSTEM=="input", GROUP="input", MODE="0664"
EOF
    
    print_success "Touchscreen permissions configured"
}

# Function to optimize for touchscreen displays
configure_display() {
    print_status "Configuring display settings for touchscreen..."
    
    # Backup original config
    if [[ ! -f /boot/config.txt.backup ]]; then
        sudo cp /boot/config.txt /boot/config.txt.backup
        print_status "Backed up original /boot/config.txt"
    fi
    
    # Add display configuration if not already present
    if ! grep -q "# PiChore display settings" /boot/config.txt; then
        sudo tee -a /boot/config.txt > /dev/null <<EOF

# PiChore display settings
hdmi_force_hotplug=1
hdmi_drive=2
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
EOF
        print_success "Display configuration added to /boot/config.txt"
        print_warning "You'll need to reboot for display changes to take effect"
    else
        print_status "Display configuration already present"
    fi
}

# Function to create desktop shortcut
create_desktop_shortcut() {
    print_status "Creating desktop shortcut..."
    
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    DESKTOP_FILE="$HOME/Desktop/PiChore.desktop"
    
    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PiChore
Comment=Family Chore and Allowance Tracker
Exec=python3 $SCRIPT_DIR/MainWindow.py
Icon=$SCRIPT_DIR/icon.png
Path=$SCRIPT_DIR
Terminal=false
StartupNotify=false
Categories=Utility;Education;
EOF
    
    chmod +x "$DESKTOP_FILE"
    print_success "Desktop shortcut created"
}

# Function to initialize database
setup_database() {
    print_status "Setting up database..."
    
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    
    if [[ -f "$SCRIPT_DIR/choreSchema.sql" ]]; then
        if [[ ! -f "$SCRIPT_DIR/Chores.db" ]]; then
            sqlite3 "$SCRIPT_DIR/Chores.db" < "$SCRIPT_DIR/choreSchema.sql"
            print_success "Database initialized"
        else
            print_status "Database already exists, skipping initialization"
        fi
    else
        print_error "choreSchema.sql not found. Make sure you're running this script from the PiChore directory."
        exit 1
    fi
}

# Function to test the installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python imports
    python3 -c "
import sys
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    import sqlite3
    print('✓ All Python dependencies working')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
    
    print_success "Installation test passed!"
}

# Main installation function
main() {
    echo "========================================="
    echo "    PiChore Dependency Installer"
    echo "========================================="
    echo
    
    print_status "Starting installation process..."
    
    # Run installation steps
    check_platform
    check_sudo
    update_system
    install_python_deps
    install_sqlite
    install_system_deps
    setup_touchscreen_permissions
    configure_display
    setup_database
    create_desktop_shortcut
    test_installation
    
    echo
    echo "========================================="
    print_success "Installation completed successfully!"
    echo "========================================="
    echo
    print_status "Next steps:"
    echo "1. Reboot your Pi to apply display settings: sudo reboot"
    echo "2. After reboot, run PiChore: python3 MainWindow.py"
    echo "3. Or use the desktop shortcut that was created"
    echo "4. Set up your admin account and add users/chores"
    echo
    print_warning "Note: You may need to log out and back in for group permissions to take effect"
    echo
}

# Run main function
main "$@"