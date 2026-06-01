# gantry_robot.py

import random
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

        # Pose
        self.x_coord = None
        self.y_coord = None
        self.z_coord = None

        # Gantry_Robot
        self.status = RobotState.POWER_OFF
        self.is_initialized = False
        self.is_homed = False

        # Gripper
        self.is_gripped = False
        self.is_gripping_active = False

        # Koncovy senzor
        self.sensor_state = False

        # Motion planning
        self.trajectory = []
        self.current_trajectory_step = 0

        # Pick/place task flags
        self.pending_pick_check = False
        self.pending_place_release = False
        self.planned_plate_available = False

        self.pick_positions = [
            (80, 80),
            (80, 220),
        ]

        self.place_positions = [
            (320, 80),
            (320, 220),
        ]

        # Z levels [mm]
        self.safe_z = 80
        self.pick_z = 40
        self.place_z = 40

        # Event log
        self.logs = []
        self.log_event("Robot object created.")

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] [{self.status.value}] {message}"
        self.logs.append(line)
        print(line)

    def clear_trajectory(self):
        self.trajectory = []
        self.current_trajectory_step = 0

    def position_text(self):
        if self.x_coord is None or self.y_coord is None or self.z_coord is None:
            return "unknown"

        return f"({self.x_coord:.2f}, {self.y_coord:.2f}, {self.z_coord:.2f})"

    def is_within_limits(self, x, y, z):
        return (
            self.x_min <= x <= self.x_max
            and self.y_min <= y <= self.y_max
            and self.z_min <= z <= self.z_max
        )

    def can_execute_task(self):
        if self.status == RobotState.ESTOP:
            self.log_event("Command rejected. Robot is in ESTOP state.")
            return False

        if self.status == RobotState.FAULT:
            self.log_event("Command rejected. Robot is in FAULT state.")
            return False

        if not self.is_homed:
            self.log_event("Command rejected. Robot is not homed.")
            return False

        if self.status != RobotState.READY:
            self.log_event(f"Command rejected. Robot is currently {self.status.value}.")
            return False

        return True

    def power_on(self):
        if self.status == RobotState.ESTOP:
            self.log_event("Power on rejected. Robot is in ESTOP state.")
            return False

        self.status = RobotState.READY
        self.is_initialized = True
        self.log_event("Robot powered on. Homing required.")
        return True

    def home(self, x=0, y=0, z=0):
        if self.status == RobotState.ESTOP:
            self.log_event("Homing rejected. Robot is in ESTOP state.")
            return False

        if not self.is_within_limits(x, y, z):
            self.status = RobotState.FAULT
            self.log_event(f"Homing rejected. Home position ({x}, {y}, {z}) is out of bounds.")
            return False

        self.status = RobotState.HOMING
        self.clear_trajectory()
        self.log_event(f"Homing started to ({x}, {y}, {z}).")

        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.is_homed = True

        self.status = RobotState.READY
        self.log_event("Homing completed. Robot is READY.")
        return True

    def plan_trajectory_through_waypoints(self, waypoints, steps_per_segment=10):
        self.clear_trajectory()

        start_x = self.x_coord
        start_y = self.y_coord
        start_z = self.z_coord

        self.trajectory.append({
            "step": 0,
            "x": start_x,
            "y": start_y,
            "z": start_z,
        })

        step_counter = 1
        steps_per_segment = max(1, int(steps_per_segment))

        for target_x, target_y, target_z in waypoints:
            if not self.is_within_limits(target_x, target_y, target_z):
                self.status = RobotState.FAULT
                self.clear_trajectory()
                self.log_event(
                    f"Trajectory rejected. Waypoint "
                    f"({target_x}, {target_y}, {target_z}) is out of bounds."
                )
                return False

            for step in range(1, steps_per_segment + 1):
                t = step / steps_per_segment

                self.trajectory.append({
                    "step": step_counter,
                    "x": start_x + (target_x - start_x) * t,
                    "y": start_y + (target_y - start_y) * t,
                    "z": start_z + (target_z - start_z) * t,
                })

                step_counter += 1

            start_x = target_x
            start_y = target_y
            start_z = target_z

        return True

    def move_to(self, x, y, z, steps=20):
        if not self.can_execute_task():
            return False

        if not self.plan_trajectory_through_waypoints([(x, y, z)], steps):
            return False

        self.status = RobotState.MOVING
        self.log_event(f"Move planned to ({x}, {y}, {z}) in {steps} steps.")
        return True

    def pick_plate(self, plate_available=True, steps=1):
        if not self.can_execute_task():
            return False

        if self.is_gripped:
            self.log_event("Pick rejected. Robot is already holding a plate.")
            return False

        source_x, source_y = random.choice(self.pick_positions)

        waypoints = [
            (source_x, source_y, self.safe_z),
            (source_x, source_y, self.pick_z),
            (source_x, source_y, self.safe_z),
        ]

        if not self.plan_trajectory_through_waypoints(waypoints, steps):
            return False

        self.pending_pick_check = True
        self.planned_plate_available = plate_available
        self.sensor_state = plate_available

        self.status = RobotState.MOVING
        self.log_event(
            f"Pick sequence planned at magazine ({source_x}, {source_y}). "
            f"Plate present: {plate_available}."
        )
        return True

    def place_plate(self, steps=1):
        if not self.can_execute_task():
            return False

        if not self.is_gripped:
            self.log_event("Place rejected. Robot is not holding a plate.")
            return False

        dest_x, dest_y = random.choice(self.place_positions)

        waypoints = [
            (dest_x, dest_y, self.safe_z),
            (dest_x, dest_y, self.place_z),
            (dest_x, dest_y, self.safe_z),
        ]

        if not self.plan_trajectory_through_waypoints(waypoints, steps):
            return False

        self.pending_place_release = True

        self.status = RobotState.MOVING
        self.log_event(f"Place sequence planned at destination ({dest_x}, {dest_y}).")
        return True

    def step_motion(self):
        if self.status == RobotState.ESTOP:
            self.log_event("Motion blocked. Robot is in ESTOP state.")
            return False

        if self.status != RobotState.MOVING:
            return False

        next_step = self.current_trajectory_step + 1

        if next_step >= len(self.trajectory):
            self.finish_motion()
            return False

        point = self.trajectory[next_step]

        self.x_coord = point["x"]
        self.y_coord = point["y"]
        self.z_coord = point["z"]

        self.current_trajectory_step = next_step

        if self.current_trajectory_step >= len(self.trajectory) - 1:
            self.finish_motion()

        return True

    def finish_motion(self):
        self.status = RobotState.READY
        self.log_event(f"Motion completed. TCP position is {self.position_text()}.")

        if self.pending_pick_check:
            self.pending_pick_check = False

            if not self.planned_plate_available:
                self.status = RobotState.FAULT
                self.is_gripping_active = False
                self.is_gripped = False
                self.sensor_state = False
                self.log_event("Pick failed. Magazine was empty. Robot entered FAULT state.")
                return

            self.is_gripping_active = True
            self.is_gripped = True
            self.sensor_state = True
            self.log_event("Pick completed. Gripper closed and plate detected.")

        if self.pending_place_release:
            self.pending_place_release = False
            self.is_gripping_active = False
            self.is_gripped = False
            self.sensor_state = False
            self.log_event("Place completed. Gripper opened and plate released.")

    def emergency_stop(self):
        self.status = RobotState.ESTOP
        self.log_event(f"Emergency stop activated. TCP frozen at {self.position_text()}.")
        return True

    def reset_fault(self):
        if self.status not in [RobotState.FAULT, RobotState.ESTOP]:
            self.log_event("Reset ignored. Robot is not in FAULT or ESTOP.")
            return False

        self.status = RobotState.READY
        self.is_homed = False

        self.is_gripping_active = False
        self.is_gripped = False
        self.sensor_state = False

        self.pending_pick_check = False
        self.pending_place_release = False
        self.planned_plate_available = False

        self.clear_trajectory()

        self.log_event("Fault/ESTOP reset. Trajectory and gripper state cleared. Homing required.")
        return True

    def get_position(self):
        return {
            "x": self.x_coord,
            "y": self.y_coord,
            "z": self.z_coord,
        }

    def get_status(self):
        return {
            "name": self.name,
            "status": self.status.value,
            "is_initialized": self.is_initialized,
            "is_homed": self.is_homed,
            "is_gripped": self.is_gripped,
            "is_gripping_active": self.is_gripping_active,
            "sensor_state": self.sensor_state,
            "position": self.get_position(),
        }