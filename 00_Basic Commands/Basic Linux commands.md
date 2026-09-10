# Basic Linux Commands

This guide contains the Linux terminal commands most frequently used while learning ROS 2. Try the examples in a terminal, but read each command before pressing <kbd>Enter</kbd>.

> [!IMPORTANT]
> Linux commands are case-sensitive. `Documents`, `documents`, and `DOCUMENTS` are three different names.

## 1. Understanding the terminal prompt

A terminal prompt may look like this:

```text
student@ubuntu:~/ros2_ws$
```

- `student` is the current username.
- `ubuntu` is the computer name.
- `~/ros2_ws` is the current directory.
- `$` indicates a normal user. A root shell commonly uses `#`.

Do not type the `$` symbol shown in some online tutorials. It represents the prompt, not part of the command.

### Command structure

Most commands follow this pattern:

```text
command [options] [arguments]
```

For example:

```bash
ls -la ~/ros2_ws
```

Here, `ls` is the command, `-la` contains options, and `~/ros2_ws` is the argument.

## 2. Useful keyboard shortcuts

| Shortcut | Purpose |
|---|---|
| <kbd>Tab</kbd> | Complete a command or path automatically |
| <kbd>Up</kbd> / <kbd>Down</kbd> | Browse previously used commands |
| <kbd>Ctrl</kbd> + <kbd>C</kbd> | Stop the currently running command or ROS node |
| <kbd>Ctrl</kbd> + <kbd>L</kbd> | Clear the terminal screen |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> | Copy selected terminal text |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd> | Paste text into the terminal |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Search command history |

> [!TIP]
> Use <kbd>Tab</kbd> completion whenever possible. It saves time and reduces typing mistakes.

## 3. Paths and directories

Important path symbols:

| Symbol | Meaning |
|---|---|
| `/` | Root of the Linux filesystem |
| `~` | Current user's home directory, such as `/home/student` |
| `.` | Current directory |
| `..` | Parent directory |
| `-` | Previous directory when used with `cd` |

An **absolute path** begins at `/`:

```text
/home/student/ros2_ws/src
```

A **relative path** begins from the current directory:

```text
src/my_robot_pkg
```

### Show the current directory

```bash
pwd
```

### List files and directories

```bash
ls
ls -l
ls -a
ls -lh
```

- `-l` displays details such as permissions and ownership.
- `-a` includes hidden files whose names begin with `.`.
- `-h` makes file sizes easier to read.

Options can be combined:

```bash
ls -lah
```

### Change directory

```bash
cd ~/ros2_ws
cd src
cd ..
cd ~
cd -
```

Running `cd` without an argument also returns to the home directory.

## 4. Creating and managing files

### Create directories

```bash
mkdir my_folder
mkdir -p ~/ros2_ws/src
```

The `-p` option creates missing parent directories and does not fail if the directory already exists.

### Create an empty file

```bash
touch notes.txt
```

### Copy files and directories

```bash
cp notes.txt notes_backup.txt
cp notes.txt ~/Documents/
cp -r my_robot_pkg my_robot_pkg_backup
```

Use `-r` to copy a directory and everything inside it.

### Move or rename

```bash
mv old_name.txt new_name.txt
mv new_name.txt ~/Documents/
```

The same `mv` command is used for both renaming and moving.

### Remove files and directories

```bash
rm unwanted.txt
rmdir empty_folder
rm -r unwanted_folder
```

> [!CAUTION]
> `rm` normally deletes permanently; it does not use a recycle bin. Check the current directory with `pwd` and inspect the target with `ls` before deleting it. Never experiment with `sudo rm -rf`, `/`, or `~`.

For confirmation before each removal, use:

```bash
rm -i unwanted.txt
rm -ri unwanted_folder
```

### Names containing spaces

Put paths containing spaces inside quotes:

```bash
cd "My Projects"
cp "robot notes.txt" ~/Documents/
```

## 5. Reading and editing text files

### Display a short file

```bash
cat package.xml
```

### Read a long file one screen at a time

```bash
less package.xml
```

Use the arrow keys or <kbd>Page Up</kbd>/<kbd>Page Down</kbd> to move, `/word` to search, and <kbd>Q</kbd> to quit.

### Show the beginning or end of a file

```bash
head -n 10 log.txt
tail -n 20 log.txt
tail -f log.txt
```

`tail -f` continuously displays new lines. Stop it with <kbd>Ctrl</kbd> + <kbd>C</kbd>.

### Edit a file with Nano

```bash
nano notes.txt
```

In Nano:

- <kbd>Ctrl</kbd> + <kbd>O</kbd>, then <kbd>Enter</kbd>: save
- <kbd>Ctrl</kbd> + <kbd>X</kbd>: exit
- <kbd>Ctrl</kbd> + <kbd>W</kbd>: search

## 6. Finding files and text

### Find files by name

```bash
find ~/ros2_ws/src -name "package.xml"
find . -name "*.py"
```

The quotes prevent the shell from expanding `*` before `find` processes it.

### Search inside files

```bash
grep "depend" package.xml
grep -R "TODO" ~/ros2_ws/src
grep -Rni "publisher" ~/ros2_ws/src
```

- `-R` searches subdirectories recursively.
- `-n` shows line numbers.
- `-i` ignores uppercase/lowercase differences.

### Locate an executable

```bash
which python3
which ros2
```

If `which ros2` returns nothing, the ROS 2 environment may not be sourced.

## 7. Command history and help

```bash
history
history | grep ros2
```

Ask a command for brief help:

```bash
ls --help
ros2 --help
ros2 topic --help
```

Open the Linux manual page for a command:

```bash
man cp
```

Press <kbd>Q</kbd> to leave a manual page.

## 8. Pipes and redirection

### Send one command's output to another command

The pipe symbol `|` connects commands:

```bash
ros2 topic list | grep camera
```

This lists ROS topics and keeps only lines containing `camera`.

### Save command output to a file

```bash
ros2 topic list > topics.txt
ros2 node list >> ros_status.txt
```

- `>` creates or overwrites the destination file.
- `>>` adds output to the end of the file.

> [!CAUTION]
> Check the filename before using `>` because existing content will be overwritten.

Display output and save it at the same time:

```bash
ros2 topic echo /chatter | tee chatter_log.txt
```

Stop recording with <kbd>Ctrl</kbd> + <kbd>C</kbd>.

## 9. Environment variables and setup files

Display an environment variable:

```bash
echo "$HOME"
echo "$ROS_DISTRO"
```

Set a variable for the current terminal:

```bash
export ROS_DOMAIN_ID=10
```

Load commands and variables from a setup file into the current shell:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

> [!IMPORTANT]
> Source the ROS 2 installation first (the **underlay**), then source the local workspace (the **overlay**).

Check the ROS environment:

```bash
printenv | grep ROS
```

To run a setup command automatically in every new Bash terminal, add it once to `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 10. Permissions and `sudo`

View file permissions:

```bash
ls -l my_node.py
```

Make a Python script executable:

```bash
chmod +x my_node.py
```

Show the current user and groups:

```bash
whoami
groups
```

`sudo` runs one command with administrator privileges:

```bash
sudo apt update
```

> [!WARNING]
> Do not add `sudo` merely because a command failed. Read the error first. ROS workspace commands such as `colcon build` and `ros2 run` should normally be executed as the regular user, not with `sudo`.

If files in the workspace accidentally belong to `root`, ask the instructor before changing ownership.

## 11. Processes and system information

### Inspect running processes

```bash
ps
ps aux
top
```

Press <kbd>Q</kbd> to exit `top`.

Search for a process:

```bash
ps aux | grep ros2
```

Stop the foreground program with <kbd>Ctrl</kbd> + <kbd>C</kbd>. To stop another process, first identify its process ID (PID), then run:

```bash
kill PID
```

Replace `PID` with the number, for example `kill 2451`. Use `kill -9 PID` only as a last resort because it prevents normal cleanup.

### Check disk and memory usage

```bash
df -h
du -sh ~/ros2_ws
free -h
```

### Check operating system and hardware

```bash
lsb_release -a
uname -a
dpkg --print-architecture
```

## 12. Installing software with APT

```bash
sudo apt update
sudo apt install PACKAGE_NAME
sudo apt remove PACKAGE_NAME
apt search KEYWORD
apt list --installed
```

Example:

```bash
sudo apt install tree
```

ROS 2 package names generally use lowercase words separated by hyphens:

```bash
sudo apt install ros-jazzy-turtlesim
```

Replace underscores in a ROS package name with hyphens when looking for its Debian package. For example, `demo_nodes_cpp` is commonly represented as `ros-jazzy-demo-nodes-cpp`.

## 13. Networking commands

Show network interfaces and IP addresses:

```bash
ip address
hostname -I
```

Test whether a host is reachable:

```bash
ping -c 4 8.8.8.8
ping -c 4 google.com
```

Download or inspect a URL:

```bash
curl -I https://docs.ros.org
```

Connect securely to another Linux computer:

```bash
ssh username@192.168.1.20
```

Copy a file to another computer:

```bash
scp notes.txt username@192.168.1.20:~/
```

> [!NOTE]
> ROS 2 machines must have compatible network settings and matching `ROS_DOMAIN_ID` values to discover one another. Follow the laboratory network instructions supplied by the instructor.

## 14. Archives

Create a compressed backup of a package:

```bash
tar -czf my_robot_pkg.tar.gz my_robot_pkg/
```

List its contents without extracting:

```bash
tar -tzf my_robot_pkg.tar.gz
```

Extract it:

```bash
tar -xzf my_robot_pkg.tar.gz
```

## 15. Common ROS 2 workspace workflow

A ROS 2 workspace normally contains a `src` directory. After building, it also contains `build`, `install`, and `log` directories.

### Create a workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### Build all packages

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --symlink-install
```

### Source the built workspace

```bash
source ~/ros2_ws/install/setup.bash
```

Source the workspace again in every new terminal after building it. If source code changes, rebuild before running it.

### Build one package

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_robot_pkg
```

### Install missing package dependencies

Run this from the workspace root after packages have been placed in `src`:

```bash
cd ~/ros2_ws
sudo apt update
rosdep install --from-paths src --ignore-src -r -y
```

### Inspect the workspace

```bash
find ~/ros2_ws/src -maxdepth 2 -name package.xml
colcon list
```

## 16. Essential ROS 2 command-line commands

These are ROS 2 commands rather than general Linux commands, but they are frequently used in the same terminal.

### Nodes

```bash
ros2 node list
ros2 node info /node_name
```

### Topics

```bash
ros2 topic list
ros2 topic list -t
ros2 topic echo /topic_name
ros2 topic info /topic_name
ros2 topic hz /topic_name
```

### Services

```bash
ros2 service list
ros2 service type /service_name
```

### Parameters

```bash
ros2 param list
ros2 param get /node_name parameter_name
```

### Packages and executables

```bash
ros2 pkg list
ros2 pkg executables my_robot_pkg
ros2 run my_robot_pkg executable_name
```

### Launch files

```bash
ros2 launch my_robot_pkg my_launch_file.launch.py
```

Use <kbd>Tab</kbd> completion and `--help` to discover valid names and options.

## 17. Common problems

### `command not found`

Check the spelling and determine whether the program exists:

```bash
which COMMAND_NAME
```

For `ros2: command not found`, run:

```bash
source /opt/ros/jazzy/setup.bash
```

### `No such file or directory`

Check the current directory and list its contents:

```bash
pwd
ls -la
```

Use <kbd>Tab</kbd> completion to verify the path.

### `Permission denied`

Inspect the file's permissions:

```bash
ls -l FILE_NAME
```

If it is your own script and should be executable, use `chmod +x FILE_NAME`. Do not immediately use `sudo`.

### ROS 2 cannot find a package

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 pkg list | grep my_robot_pkg
```

If it is still missing, return to the workspace root, rebuild the package, and read the first build error carefully.

## Quick-reference checklist

Before running a ROS 2 program, check:

```bash
pwd
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
printenv ROS_DISTRO
ros2 node list
```

Remember these habits:

- Use <kbd>Tab</kbd> completion instead of guessing paths.
- Read error messages from the first line onward.
- Check `pwd` before copying, moving, or removing files.
- Avoid `sudo` unless a command genuinely needs administrator access.
- Stop ROS nodes cleanly with <kbd>Ctrl</kbd> + <kbd>C</kbd>.
- Keep source code in `~/ros2_ws/src` and run `colcon build` from `~/ros2_ws`.
