# gantry_robot.py

from datetime import datetime
from enum import Enum


class RobotState(Enum):
    POWER_OFF = "POWER_OFF"
    READY = "READY"
    HOMING = "HOMING"
    MOVING = "MOVING"
    FAULT = "FAULT"
    ESTOP = "ESTOP"


class GantryRobot:
    def __init__(self):
        self.name = "Gantry Robot"

        # Workspace limits [mm]
        self.x_min, self.x_max = 0, 400
        self.y_min, self.y_max = 0, 300
        self.z_min, self.z_max = 0, 200

        # TCP position
        self.x = None
        self.y = None
        self.z = None

        # Robot state
        self.state = RobotState.POWER_OFF
        self.is_homed = False

        # Motion planning
        self.trajectory = []
        self.current_trajectory_step = 0

        # Event log
        self.logs = []
        self.log_event("Robot object created.")

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] [{self.state.value}] {message}"
        self.logs.append(line)
        print(line)

    def clear_trajectory(self):
        self.trajectory = []
        self.current_trajectory_step = 0

    def position_text(self):
        if self.x is None or self.y is None or self.z is None:
            return "unknown"
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def is_within_limits(self, x, y, z):
        return (
            self.x_min <= x <= self.x_max
            and self.y_min <= y <= self.y_max
            and self.z_min <= z <= self.z_max
        )

    def power_on(self):
        if self.state == RobotState.ESTOP:
            self.log_event("Power on rejected. Robot is in ESTOP state.")
            return False

        self.state = RobotState.READY
        self.log_event("Robot powered on. Homing required.")
        return True

    def home(self, x=0, y=0, z=0):
        if self.state == RobotState.ESTOP:
            self.log_event("Homing rejected. Robot is in ESTOP state.")
            return False

        if not self.is_within_limits(x, y, z):
            self.state = RobotState.FAULT
            self.log_event(f"Homing rejected. Home position ({x}, {y}, {z}) is out of bounds.")
            return False

        self.state = RobotState.HOMING
        self.clear_trajectory()
        self.log_event(f"Homing started to ({x}, {y}, {z}).")

        self.x, self.y, self.z = x, y, z
        self.is_homed = True

        self.state = RobotState.READY
        self.log_event("Homing completed. Robot is READY.")
        return True

    def move_to(self, x, y, z, steps=20):
        if self.state == RobotState.ESTOP:
            self.log_event("Move rejected. Robot is in ESTOP state.")
            return False

        if self.state == RobotState.FAULT:
            self.log_event("Move rejected. Robot is in FAULT state.")
            return False

        if not self.is_homed:
            self.log_event("Move rejected. Robot is not homed.")
            return False

        if not self.is_within_limits(x, y, z):
            self.state = RobotState.FAULT
            self.clear_trajectory()
            self.log_event(f"Move rejected. Target ({x}, {y}, {z}) is out of bounds.")
            return False

        start_x, start_y, start_z = self.x, self.y, self.z
        steps = max(1, int(steps))

        self.clear_trajectory()

        for step in range(1, steps + 1):
            t = step / steps
            self.trajectory.append({
                "step": step,
                "x": start_x + (x - start_x) * t,
                "y": start_y + (y - start_y) * t,
                "z": start_z + (z - start_z) * t,
            })

        self.state = RobotState.MOVING
        self.log_event(f"Move planned to ({x}, {y}, {z}) in {steps} steps.")
        return True

    def step_motion(self):
        if self.state == RobotState.ESTOP:
            self.log_event("Motion blocked. Robot is in ESTOP state.")
            return False

        if self.state != RobotState.MOVING:
            return False

        if self.current_trajectory_step >= len(self.trajectory):
            self.finish_motion()
            return False

        point = self.trajectory[self.current_trajectory_step]
        self.x, self.y, self.z = point["x"], point["y"], point["z"]
        self.current_trajectory_step += 1

        if self.current_trajectory_step >= len(self.trajectory):
            self.finish_motion()

        return True

    def finish_motion(self):
        self.state = RobotState.READY
        self.log_event(f"Move completed. TCP position is {self.position_text()}.")

    def emergency_stop(self):
        self.state = RobotState.ESTOP
        self.log_event(f"Emergency stop activated. TCP frozen at {self.position_text()}.")
        return True

    def reset_fault(self):
        if self.state not in [RobotState.FAULT, RobotState.ESTOP]:
            self.log_event("Reset ignored. Robot is not in FAULT or ESTOP.")
            return False

        self.state = RobotState.READY
        self.is_homed = False
        self.clear_trajectory()

        self.log_event("Fault/ESTOP reset. Trajectory cleared. Homing required.")
        return True

    def get_position(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    def get_status(self):
        return {
            "name": self.name,
            "state": self.state.value,
            "is_homed": self.is_homed,
            "position": self.get_position(),
        }