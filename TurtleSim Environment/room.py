import math
import tkinter as tk
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav_msgs.msg import OccupancyGrid

# World parameters
WORLD_SIZE = 20.0  # 20m x 20m arena
CANVAS_PIXELS = 800  # 800x800 window resolution
SCALE = CANVAS_PIXELS / WORLD_SIZE  # 40 pixels per meter
GRID_RES = 0.1  # Occupancy grid resolution (0.1m / cell)
GRID_CELLS = int(WORLD_SIZE / GRID_RES)  # 200x200 grid

class RoomSimulatorNode(Node):
    def __init__(self, root):
        super().__init__('room_simulator_node')
        self.root = root
        self.root.title("ROS 2 Multi-Room Turtle Simulator (20m x 20m)")

        # Setup Tkinter Canvas
        self.canvas = tk.Canvas(self.root, width=CANVAS_PIXELS, height=CANVAS_PIXELS, bg="#1E1E2E")
        self.canvas.pack()

        # State variables
        self.x = 2.0
        self.y = 2.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # Define Multi-Room Walls (x1, y1, x2, y2) in meters
        self.walls = [
            # Outer perimeter
            (0.0, 0.0, WORLD_SIZE, 0.0),
            (0.0, 0.0, 0.0, WORLD_SIZE),
            (WORLD_SIZE, 0.0, WORLD_SIZE, WORLD_SIZE),
            (0.0, WORLD_SIZE, WORLD_SIZE, WORLD_SIZE),
            # Middle vertical divider (x=10) with doors at y=[3..5] and y=[15..17]
            (10.0, 0.0, 10.0, 3.0),
            (10.0, 5.0, 10.0, 15.0),
            (10.0, 17.0, 10.0, 20.0),
            # Left horizontal divider (y=10) with door at x=[4..6]
            (0.0, 10.0, 4.0, 10.0),
            (6.0, 10.0, 10.0, 10.0),
            # Right horizontal divider (y=10) with door at x=[14..16]
            (10.0, 10.0, 14.0, 10.0),
            (16.0, 10.0, 20.0, 10.0),
        ]

        # Build static occupancy grid
        self.occupancy_grid = [0] * (GRID_CELLS * GRID_CELLS)
        self._rasterize_walls()

        # ROS 2 Publishers & Subscribers
        self.cmd_sub = self.create_subscription(Twist, '/turtle1/cmd_vel', self.cmd_callback, 10)
        self.pose_pub = self.create_publisher(Pose, '/turtle1/pose', 10)
        self.map_pub = self.create_publisher(OccupancyGrid, '/map', 10)

        # Publish static map on launch
        self.timer_map = self.create_timer(1.0, self.publish_map)

        # Draw static environment
        self._draw_static_environment()

        # Main simulation update loop (50Hz = 20ms)
        self.last_time = self.get_clock().now()
        self.update_loop()

    def _rasterize_walls(self):
        for x1, y1, x2, y2 in self.walls:
            steps = max(int(math.hypot(x2 - x1, y2 - y1) / (GRID_RES / 2)), 1)
            for i in range(steps + 1):
                wx = x1 + (x2 - x1) * (i / steps)
                wy = y1 + (y2 - y1) * (i / steps)
                gx = int(wx / GRID_RES)
                gy = int(wy / GRID_RES)
                if 0 <= gx < GRID_CELLS and 0 <= gy < GRID_CELLS:
                    # Mark cell and neighbors for obstacle thickness
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            idx = (gy + dy) * GRID_CELLS + (gx + dx)
                            if 0 <= idx < len(self.occupancy_grid):
                                self.occupancy_grid[idx] = 100

    def _draw_static_environment(self):
        # Draw grid lines
        for i in range(0, CANVAS_PIXELS, int(2 * SCALE)):
            self.canvas.create_line(i, 0, i, CANVAS_PIXELS, fill="#2A2A3C", width=1)
            self.canvas.create_line(0, i, CANVAS_PIXELS, i, fill="#2A2A3C", width=1)

        # Draw wall lines
        for x1, y1, x2, y2 in self.walls:
            cx1, cy1 = x1 * SCALE, CANVAS_PIXELS - (y1 * SCALE)
            cx2, cy2 = x2 * SCALE, CANVAS_PIXELS - (y2 * SCALE)
            self.canvas.create_line(cx1, cy1, cx2, cy2, fill="#F38BA8", width=6)

    def cmd_callback(self, msg: Twist):
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def check_collision(self, test_x, test_y):
        gx = int(test_x / GRID_RES)
        gy = int(test_y / GRID_RES)
        if 0 <= gx < GRID_CELLS and 0 <= gy < GRID_CELLS:
            return self.occupancy_grid[gy * GRID_CELLS + gx] == 100
        return True

    def update_loop(self):
        rclpy.spin_once(self, timeout_sec=0)

        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now

        # Motion kinematics update
        new_theta = self.theta + self.angular_vel * dt
        new_theta = math.atan2(math.sin(new_theta), math.cos(new_theta))

        dx = self.linear_vel * math.cos(new_theta) * dt
        dy = self.linear_vel * math.sin(new_theta) * dt
        new_x = self.x + dx
        new_y = self.y + dy

        # Collision rejection
        if not self.check_collision(new_x, new_y):
            self.x, self.y, self.theta = new_x, new_y, new_theta

        # Publish Pose
        pose_msg = Pose()
        pose_msg.x = float(self.x)
        pose_msg.y = float(self.y)
        pose_msg.theta = float(self.theta)
        pose_msg.linear_velocity = float(self.linear_vel)
        pose_msg.angular_velocity = float(self.angular_vel)
        self.pose_pub.publish(pose_msg)

        # Render Turtle Sprite
        self.canvas.delete("turtle")
        cx, cy = self.x * SCALE, CANVAS_PIXELS - (self.y * SCALE)
        radius = 12

        # Draw Turtle Body
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                fill="#A6E3A1", outline="#A6E3A1", tags="turtle")
        # Draw Heading Indicator
        hx = cx + (radius + 6) * math.cos(-self.theta)
        hy = cy + (radius + 6) * math.sin(-self.theta)
        self.canvas.create_line(cx, cy, hx, hy, fill="#11111B", width=3, tags="turtle")

        self.root.after(20, self.update_loop)

    def publish_map(self):
        grid_msg = OccupancyGrid()
        grid_msg.header.stamp = self.get_clock().now().to_msg()
        grid_msg.header.frame_id = "map"
        grid_msg.info.resolution = float(GRID_RES)
        grid_msg.info.width = GRID_CELLS
        grid_msg.info.height = GRID_CELLS
        grid_msg.info.origin.position.x = 0.0
        grid_msg.info.origin.position.y = 0.0
        grid_msg.data = self.occupancy_grid
        self.map_pub.publish(grid_msg)

def main(args=None):
    rclpy.init(args=args)
    root = tk.Tk()
    node = RoomSimulatorNode(root)
    root.mainloop()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()