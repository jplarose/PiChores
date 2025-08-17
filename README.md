# PiChore - A Raspberry Pi Chore and Allowance Tracker 🏠💰

## The Parent's Dilemma (aka Why This Exists)

As my kids got older, keeping track of which chores had been done and when they were done became more and more of a hassle. You know the drill - "Did you take out the trash?" "I already did it!" "When?" "Yesterday!" (Spoiler alert: it was definitely not yesterday.)

Especially with allowance becoming more important in their little financial worlds, I wanted a way to make sure we could keep everything tracked accurately. No more arguments about who did what, when they did it, or how much they've earned. Just cold, hard data that even a 10-year-old can't argue with.

As it turns out, touch screens for the Raspberry Pi are cheap! And I definitely had an old Pi sitting in a closet collecting dust. Perfect excuse to build something that would solve my parenting problems AND let me play with some code. Win-win!

## What This Thing Does

PiChore is a touchscreen-friendly chore tracking and allowance management system that:

- **Tracks chores** with customizable frequency (daily, weekly, or one-time)
- **Calculates allowances** automatically based on completed chores
- **Provides user authentication** (because kids love having their own "accounts")
- **Shows earnings history** so kids can see their financial empire grow
- **Admin panel** for parents to review everything and make sure no one's gaming the system
- **Touch-optimized interface** perfect for kitchen counters and impatient kids

## Hardware You'll Need

- **Raspberry Pi** (I used a 3B, but newer models work great too)
- **Touchscreen display** (I used a Hosyond 5" touch screen - about $40 on Amazon)
- **MicroSD card** (16GB minimum)
- **Case** (optional but recommended to survive the chaos of family life)

## Software Installation

### Quick Install (Recommended)

We've made this super easy! Just run our installation script that handles everything:

```bash
# Clone or download the project to your Pi
git clone <your-repo-url> pyChore
# Or if you're copying files manually:
# scp -r pyChore/ pi@your-pi-ip:/home/pi/

cd pyChore

# Run the magical installation script
./install-dependencies.sh
```

That's it! The script will:
- ✅ Update your system
- ✅ Install Python and PyQt5
- ✅ Set up SQLite database
- ✅ Configure touchscreen permissions
- ✅ Optimize display settings for 800x480 screens
- ✅ Create a desktop shortcut
- ✅ Initialize the database
- ✅ Test everything works

After the script completes, just reboot your Pi and you're ready to go!

### Manual Installation (For the Adventurous)

If you prefer to do things step by step:

#### Step 1: Prepare Your Raspberry Pi

1. **Flash Raspberry Pi OS** to your SD card using the [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. **Enable SSH and configure WiFi** during the imaging process (or do it manually later)
3. **Boot up your Pi** and connect to it via SSH or directly

#### Step 2: Install Dependencies

```bash
# Update your Pi
sudo apt update && sudo apt upgrade -y

# Install Python and PyQt5
sudo apt install -y python3 python3-pip python3-pyqt5 python3-pyqt5.qtwidgets

# Install SQLite
sudo apt install -y sqlite3 libsqlite3-dev

# Install display and touchscreen support
sudo apt install -y xorg xinput x11-xserver-utils libqt5gui5
```

#### Step 3: Set Up the Application

```bash
cd pyChore

# Make scripts executable
chmod +x run-chores.sh

# Initialize the database
sqlite3 Chores.db < choreSchema.sql
```

#### Step 4: Configure Touchscreen (if needed)

```bash
# Add display settings to /boot/config.txt
echo "hdmi_force_hotplug=1" | sudo tee -a /boot/config.txt
echo "hdmi_drive=2" | sudo tee -a /boot/config.txt
echo "hdmi_cvt=800 480 60 6 0 0 0" | sudo tee -a /boot/config.txt

# Add user to input group for touchscreen
sudo usermod -a -G input $USER

# Reboot to apply changes
sudo reboot
```

#### Step 5: Set Up Auto-Start (Optional but Recommended)

To make PiChore start automatically when your Pi boots:

```bash
# Create a systemd service
sudo tee /etc/systemd/system/pichore.service > /dev/null <<EOF
[Unit]
Description=PiChore Chore Tracker
After=graphical-session.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pyChore
ExecStart=/home/pi/pyChore/run-chores.sh
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=graphical-session.target
EOF

# Enable the service
sudo systemctl enable pichore.service
sudo systemctl start pichore.service
```

## Initial Setup

### Adding Users (Your Kids)

1. **Run the application**: `python3 MainWindow.py`
2. **Access admin mode**: Long-press (5 seconds) on the first user button
3. **Set up admin account**: Create a PIN for the admin user
4. **Add your kids**: Create user accounts for each child with their own PINs
5. **Create chores**: Define chores with names, values, and frequencies

### Setting Up Chores

Think about what you want to track:
- **Daily chores**: Make bed, feed pets, homework ($1-2 each)
- **Weekly chores**: Vacuum room, take out trash, clean bathroom ($5-10 each)
- **One-time chores**: Rake leaves, wash car, organize garage ($10-20 each)

## Usage

### For Kids
1. **Select your name** from the main screen
2. **Enter your PIN** (keeps siblings from messing with your earnings!)
3. **Log completed chores** by selecting them and choosing the date
4. **Check your earnings** to see how rich you're getting

### For Parents (Admin)
1. **Access admin panel** via long-press on first user
2. **Review chore logs** to make sure everything looks legit
3. **Check weekly/yearly earnings** for allowance planning
4. **Add/modify users and chores** as needed

## Technical Details

- **Built with**: Python 3 + PyQt5 for the GUI, SQLite for data storage
- **Screen resolution**: Optimized for 800x480 touchscreens
- **Data storage**: Local SQLite database (no cloud, no privacy concerns)
- **Backup**: Simply copy the `Chores.db` file to back up all data

## Troubleshooting

**App won't start?**
- Check that all Python dependencies are installed: `pip3 list | grep PyQt5`
- Verify the database exists: `ls -la Chores.db`

**Touchscreen not working?**
- Check `dmesg | grep -i touch` for hardware detection
- Verify display settings in `/boot/config.txt`

**Kids trying to hack the system?**
- Check the admin logs panel - it tracks everything! 
- Remember: they're learning valuable life skills (persistence, problem-solving, etc.)

## Contributing

Found a bug? Want to add features? Great! This started as a weekend project to solve a parenting problem, so any improvements are welcome.

Just remember: if your changes break something and cause a family uprising about missing allowance data, you're explaining it to my kids. 😄

## License

This project is licensed under "Whatever Works for Your Family" license. Use it, modify it, share it - just maybe buy me a coffee if it saves your sanity.

---

*Built by a parent who got tired of arguing about chores and decided to let code do the arguing instead.*