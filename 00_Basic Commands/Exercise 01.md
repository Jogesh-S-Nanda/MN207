# Exercise 01: Basic Linux Commands

**Author:** Jogesh S Nanda, Robotics Innovation Lab (RIL), IISc  
**Purpose:** MN207 lab session  
**Copyright:** © Robotics Innovation Lab (RIL), IISc

© Robotics Innovation Lab (RIL), IISc. Developed for coursework MN207.

---

## Purpose

This lab introduces useful Linux terminal commands and shows how they help when working with ROS 2. Run the commands one at a time. Read the explanation, try the command, and compare what you see with the notes.

Examples assume Ubuntu. Your screen may look a little different depending on your Ubuntu and ROS 2 versions. Commands shown in angle brackets, such as `<PID>`, are placeholders: replace them with a real value and do not type the brackets.

> **Safety:** Be careful with commands that change the computer. `sudo` gives administrator privileges. Never run a command you do not understand, and follow your instructor’s directions before installing or upgrading software.

## 1. Find your way around

### `pwd` - print working directory

Shows the full path of the folder your terminal is currently using.

```bash
pwd
```

**Try it:** Note the path. It may look like `/home/student`. This is your current working directory.

### `ls` - list files

Shows the files and folders in the current directory.

```bash
ls
ls -la
```

The first command gives a simple list. `-la` also shows hidden files (whose names begin with a dot) and extra details.

**Try it:** Run `ls` in your home folder, then run `ls -la`. Can you spot configuration files such as `.bashrc`?

### `cd` - change directory

Moves the terminal to another folder. With no path, it returns to your home folder.

```bash
cd ~
pwd
cd /
pwd
cd ~
```

`~` means your home folder, `/` is the top of the filesystem, and `..` means the parent folder. Use `cd ..` to move up one level.

**Try it:** Run `cd /`, then `ls`, then `cd ~`. Use `pwd` each time to check where you are.

## 2. Learn about the computer

### `lsb_release -a` - identify the Linux distribution

```bash
lsb_release -a
```

Shows the Ubuntu distribution name and release number. This helps you check which operating-system instructions are relevant.

**Try it:** Write down the Ubuntu version. If the command is unavailable, ask your instructor or check **Settings → About**.

### `free -h` - check memory use

```bash
free -h
```

Shows memory (RAM) and swap use. The `-h` option displays readable units such as MiB or GiB.

**Try it:** Look at the `available` value in the `Mem` row. This is an estimate of memory available to applications.

### `echo "$HOME"` - display your home folder

```bash
echo "$HOME"
```

Prints the value of the `HOME` environment variable. It usually points to your personal folder, for example `/home/student`.

### `which python3` and `which ros2` - find programs

```bash
which python3
which ros2
```

Prints the path of a program found in your command search path. `python3` is commonly installed on Ubuntu. `ros2` will only be found after ROS 2 is installed and its setup has been loaded into this terminal.

**Try it:** Run `which ros2` before and after the ROS 2 setup step in Section 6. Compare the output.

## 3. Check the network

### `ip addr` - inspect network interfaces and IP addresses

```bash
ip addr
```

Lists network interfaces and their addresses. Look for an active interface (often named `enp...`, `eth...`, or `wlan...`) and an `inet` address, which may look like `192.168.1.25`.

The address `127.0.0.1` is the computer’s loopback address. It refers to this computer itself, not its address on the local network. In a virtual machine, the displayed address depends on its network settings.

**Try it:** Find the `inet` address for the active interface. Do not share a network address publicly if your instructor or network administrator says it is private.

### `ping` - test whether a host responds

`ping` sends small network requests to another host and reports replies. Specify a host and limit the number of attempts:

```bash
ping -c 4 docs.ros.org
```

`-c 4` sends four requests and exits. Some networks block ping, so no replies do not always mean that web access is unavailable.

**Try it:** Run the command and note the replies or errors. If name resolution fails, check your internet connection or ask your instructor.

### `curl -I` - request web response headers

```bash
curl -I https://docs.ros.org
```

`curl` makes a web request; `-I` asks for response headers only. A response beginning with `HTTP/` (for example, `HTTP/2 200`) indicates that the web server responded. Redirects such as `301` or `302` can also be normal.

**Try it:** Compare this result with `ping`. A website may respond to `curl` even when ping is blocked.

### `ifconfig` and `net-tools` - older network tools

The modern Ubuntu command for inspecting interfaces is `ip addr`. `ifconfig` is an older alternative that may not be installed by default. It is included in the `net-tools` package.

```bash
sudo apt install net-tools
ifconfig
```

Use this only if your course material specifically asks for `ifconfig`. Installing packages requires an internet connection and administrator permission.

## 4. Install and update software

> **Important correction:** `sudo update` and `sudo upgrade` are not the usual Ubuntu package commands. Use `apt` with them: `sudo apt update` and `sudo apt upgrade`.

### `sudo` - run a command with administrator privileges

`sudo` runs the following command with elevated permissions. Ubuntu may ask for your password. When you type it, the terminal usually shows no characters; finish typing and press Enter.

### `sudo apt update` - refresh package information

```bash
sudo apt update
```

Refreshes the local list of packages and versions available from configured software sources. It does **not** upgrade installed software.

### `sudo apt upgrade` - upgrade installed packages

```bash
sudo apt upgrade
```

Installs available upgrades for packages already installed. Review the proposed changes and follow your instructor’s directions before confirming, especially on a course VM.

### `sudo apt install tree` - install a package

```bash
sudo apt install tree
tree ~
```

Installs the `tree` utility, which displays folders in a tree-like layout. The second command uses it to display your home folder. If asked to continue during installation, read the prompt before answering `Y`.

### `sudo snap install <package>` - install a Snap package

A Snap package is another software packaging format. You must provide the package name after `install`; the bare command `sudo snap install` is incomplete.

```bash
sudo snap install <package-name>
```

Replace `<package-name>` with the exact name of a Snap package your instructor wants you to install. For example, `sudo snap install hello-world` installs a small demonstration package where Snap is available. If `snap` is not installed or the package is unavailable, ask your instructor rather than changing system configuration.

## 5. Inspect and manage running programs

### `ps aux` - list processes

```bash
ps aux
```

Displays running processes. The `PID` column is the process ID, a number that identifies a process.

### `ps aux | grep ros2` - find ROS-related processes

```bash
ps aux | grep ros2
```

The vertical bar `|` (pipe) sends the output of the command on its left into the command on its right. `grep ros2` prints lines containing `ros2`.

The search command itself may appear in the results. To hide that matching line, you can use:

```bash
ps aux | grep '[r]os2'
```

**Try it:** Run a ROS 2 program in another terminal, then run the search. Stop the program and repeat the search.

### `top` - monitor processes live

```bash
top
```

Shows a live view of processes and CPU/memory use. Press `q` to quit and return to the shell.

### `kill <PID>` - request a process to stop

First identify the PID using `ps aux` or `top`, then substitute that number:

```bash
kill <PID>
```

For example, if the target process has PID `2468`, run `kill 2468`. This sends a normal termination request. Use it only for a process you own or are authorized to stop. For a ROS 2 program running in the foreground of your terminal, `Ctrl+C` is usually the best way to stop it.

Avoid `kill -9` unless a process will not stop normally and your instructor directs you to use it. It forces termination and does not give the program a chance to shut down cleanly.

## 6. Set up ROS 2 in a terminal

### `source` - load a setup script

```bash
source /opt/ros/<ros-distro>/setup.bash
```

Replace `<ros-distro>` with the installed ROS 2 distribution name, for example `jazzy` or `humble`. Do not type the angle brackets. `source` runs the setup script in the **current** terminal, so its environment changes are available to commands typed there.

If you built a workspace, you may also need to source its setup file, for example:

```bash
source ~/ros2_ws/install/setup.bash
```

Use the path provided by your instructor. A new terminal may need the setup commands again.

### `echo "$ROS_DISTRO"` - check the selected ROS 2 distribution

```bash
echo "$ROS_DISTRO"
```

After sourcing ROS 2, this usually prints the distribution name. If it prints a blank line, check that ROS 2 is installed and that the correct setup file was sourced in this terminal.

### `printenv | grep ROS` - view ROS environment variables

```bash
printenv | grep ROS
```

`printenv` lists environment variables; the pipe passes them to `grep`, which filters for lines containing `ROS`. The output helps verify that ROS 2 setup information is loaded.

### `ros2 topic list` - list available ROS 2 topics

With ROS 2 sourced and a ROS 2 system running:

```bash
ros2 topic list
```

This displays topics currently known to the ROS 2 graph. If no nodes are running, the list may be empty or show only standard topics. The output depends on what is running and on the ROS 2 domain/network configuration.

#### Save output with `>` and `>>`

```bash
ros2 topic list > topic.txt
ros2 topic list >> topic.txt
```

A single `>` writes output to a file and replaces its previous contents. Two `>>` append output to the end of the file. Both create `topic.txt` in the current directory if it does not exist.

**Try it:** Run `pwd` first so you know where the file will be saved. Run the first command, inspect the file with `cat topic.txt`, then run the second command and inspect it again.

## 7. Review command history

### `history` - view recent commands

```bash
history
```

Shows commands entered in the current shell’s history. Use the up and down arrow keys to recall earlier commands.

### `history | grep ros2` - find ROS 2 commands you ran

```bash
history | grep ros2
```

This filters command history to lines containing `ros2`. Your shell may not record commands from every session, and history can contain sensitive information. Do not share it without checking first.

## 8. Demonstration exercise

Run this sequence and explain what each result tells you:

```bash
pwd
ls
cd ~
lsb_release -a
free -h
ip addr
ping -c 4 docs.ros.org
curl -I https://docs.ros.org
which python3
which ros2
source /opt/ros/<ros-distro>/setup.bash
echo "$ROS_DISTRO"
printenv | grep ROS
ros2 topic list
ros2 topic list > topic.txt
cat topic.txt
history | grep ros2
```

Replace `<ros-distro>` with the installed distribution. If ROS 2 is not installed or no ROS system is running, some ROS commands may not produce output; ask your instructor which VM and ROS setup to use.

## Quick command map

| Goal | Commands |
|---|---|
| Navigate files | `pwd`, `ls`, `cd` |
| Check computer | `lsb_release -a`, `free -h`, `echo "$HOME"` |
| Check network | `ip addr`, `ping`, `curl -I` |
| Install software | `sudo apt update`, `sudo apt upgrade`, `sudo apt install`, `sudo snap install` |
| Inspect programs | `ps aux`, `grep`, `top`, `kill` |
| Prepare ROS 2 | `source`, `which ros2`, `echo "$ROS_DISTRO"`, `printenv` |
| Inspect ROS 2 | `ros2 topic list` |
| Save/check output | `>`, `>>`, `cat`, `history` |

---

**Prepared by Jogesh S Nanda**  
**Robotics Innovation Lab (RIL), IISc**  
**For course work MN207**
