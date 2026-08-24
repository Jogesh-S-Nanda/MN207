# 01. Installation of ROS2 

This guide installs **ROS 2 Jazzy Jalisco** using Debian (`apt`) packages. Follow the steps in order and read the notes before running each command.

> [!IMPORTANT]
> These instructions are for **Ubuntu 24.04 LTS (Noble), 64-bit**, either installed directly or in a virtual machine. Do not use them unchanged on Ubuntu 22.04, Windows, WSL, Linux Mint, or another Linux distribution.

## What will be installed?

- ROS 2 Jazzy Desktop (ROS 2, RViz, demos, and tutorials)
- ROS development tools such as `colcon` and `rosdep`
- The official ROS 2 software repository

Allow approximately **16 to 32 GB of free disk space** and use a stable internet connection.

## Before you begin

Open a terminal with <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>. Commands in this guide are written for the default **Bash** shell.

Check the installed Ubuntu version:

```bash
lsb_release -a
```

The output should contain:

```text
Release:        24.04
Codename:       noble
```

Also confirm that the computer is 64-bit:

```bash
dpkg --print-architecture
```

Expected output is `amd64`. `arm64` is also supported on compatible ARM computers. 

## 1. Update Ubuntu packages

Refresh the package list and install available updates:

```bash
sudo apt update
sudo apt upgrade -y
```

Enter your Ubuntu password when prompted. The cursor does not move and no characters are shown while typing a password; this is normal.

> [!WARNING]
> Do **not** run `do-release-upgrade` or upgrade Ubuntu to a different release during this course. The normal `apt upgrade` command above updates packages within Ubuntu 24.04; it does not change the Ubuntu release.

If Ubuntu asks for a restart after updating, run `sudo reboot`, sign in again, and reopen the terminal.

## 2. Configure a UTF-8 locale

ROS 2 requires a locale that supports UTF-8:

```bash
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Verify the result:

```bash
locale
```

Several lines should end in `UTF-8`, including `LANG=en_US.UTF-8` and `LC_ALL=en_US.UTF-8`.

## 3. Enable the required repositories

First enable Ubuntu's `universe` repository:

```bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe
```

Press <kbd>Enter</kbd> if the command asks for confirmation.

Next, download the current ROS repository configuration package:

```bash
sudo apt update
sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
```

Install the downloaded repository package, then refresh the package list:

```bash
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update
```

This package installs the official ROS signing key and software source.

### Checkpoint

Confirm that Ubuntu can find the Jazzy desktop package:

```bash
apt-cache policy ros-jazzy-desktop
```

The `Candidate` line should show a version number. If it shows `(none)`, do not continue; see [Troubleshooting](#troubleshooting).

## 4. Install ROS 2 Jazzy

Install the recommended desktop version:

```bash
sudo apt install ros-jazzy-desktop -y
```

This download can take several minutes. Do not close the terminal while installation is in progress.

Install the development tools used later in the course:

```bash
sudo apt install ros-dev-tools -y
```

## 5. Set up the ROS 2 environment

ROS 2 commands become available after its setup file has been **sourced**. Source it in the current terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

To source ROS 2 automatically whenever a new Bash terminal opens, add the command to `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

> [!NOTE]
> Run the `echo` command only once. Adding it repeatedly creates duplicate lines in `~/.bashrc`.

Check the environment:

```bash
printenv ROS_DISTRO
ros2 --help
```

The first command should print `jazzy`; the second should display ROS 2 command-line help.

## 6. Initialize rosdep

`rosdep` installs system dependencies required by ROS packages. Initialize it once per computer:

```bash
sudo rosdep init
rosdep update
```

If `sudo rosdep init` reports that the sources list already exists, rosdep is already initialized. Run only `rosdep update`.

## 7. Verify the installation

This publisher/subscriber test confirms that the C++ and Python ROS 2 examples work.

### Terminal 1: start the talker

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

It should repeatedly print `Publishing: 'Hello World: ...'`. Leave this terminal running.

### Terminal 2: start the listener

Open a second terminal and run:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

It should print `I heard: [Hello World: ...]`. This confirms that ROS 2 nodes can communicate. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> in each terminal to stop the programs.

### Optional graphical test

Run the turtlesim example:

```bash
ros2 run turtlesim turtlesim_node
```

A window containing a turtle should open. In a second terminal, start keyboard control:

```bash
ros2 run turtlesim turtle_teleop_key
```

Keep the second terminal selected and use the arrow keys to move the turtle. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> in both terminals when finished.

## Troubleshooting

### `ros2: command not found`

Source the setup file and try again:

```bash
source /opt/ros/jazzy/setup.bash
```

Then confirm that the installation directory exists with `ls /opt/ros/jazzy`.

### `Unable to locate package ros-jazzy-desktop`

Confirm that Ubuntu reports `24.04` and `noble`, then repeat [Step 3](#3-enable-the-required-repositories), including the `sudo dpkg -i` and final `sudo apt update` commands.

### The talker and listener cannot communicate

- Confirm that both terminals use the same computer or virtual machine.
- Run `printenv ROS_DISTRO` in both terminals; each should print `jazzy`.
- Stop both nodes, open fresh terminals, and repeat the test.
- A VPN or restrictive firewall can interfere with ROS 2 discovery; disconnect the VPN if course policy permits.

### Package installation was interrupted

Repair unfinished package configuration, then retry the relevant installation command:

```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
sudo apt update
```

### No turtlesim window appears in a virtual machine

Make sure the virtual machine has a desktop environment and graphical acceleration enabled. ROS 2 may still be correctly installed if the talker/listener test succeeds.

## Installation checklist

- [ ] Ubuntu version is 24.04 (`noble`)
- [ ] UTF-8 locale is configured
- [ ] Official ROS 2 repository is enabled
- [ ] `ros-jazzy-desktop` and `ros-dev-tools` are installed
- [ ] `printenv ROS_DISTRO` prints `jazzy`
- [ ] Talker and listener exchange messages

## Reference

These notes follow the official [ROS 2 Jazzy installation guide for Ubuntu Debian packages](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Consult the official guide if the repository setup changes in the future.
