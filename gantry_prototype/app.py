# app.py

from pathlib import Path
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from gantry_robot import GantryRobot


st.set_page_config(
    page_title="Gantry Robot Prototype",
    layout="wide"
)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    h2, h3 {
        font-size: 1.1rem !important;
    }

    .status-card {
        background-color: #f7f7f9;
        border: 1px solid #e2e2e8;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }

    .status-title {
        font-size: 0.75rem;
        color: #666;
        margin-bottom: 4px;
    }

    .status-value {
        font-size: 1.35rem;
        font-weight: 650;
        color: #111827;
    }

    .status-ok {
        color: #047857;
    }

    .status-bad {
        color: #b91c1c;
    }

    .status-neutral {
        color: #1f2937;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def create_robot_if_needed():
    if "robot" not in st.session_state:
        st.session_state.robot = GantryRobot()


def create_simulation_state_if_needed():
    if "plate_present" not in st.session_state:
        st.session_state.plate_present = True

    if "active_task" not in st.session_state:
        st.session_state.active_task = None


def status_card(title, value, state="neutral"):
    css_class = {
        "ok": "status-ok",
        "bad": "status-bad",
        "neutral": "status-neutral",
    }.get(state, "status-neutral")

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-title">{title}</div>
            <div class="status-value {css_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_workspace(robot, target_x, target_y, active_task=None):
    fig, ax = plt.subplots(figsize=(5.4, 3.2), dpi=100)

    ax.set_title("TCP position in XY workspace", fontsize=10)
    ax.set_xlabel("X axis [mm]", fontsize=8)
    ax.set_ylabel("Y axis [mm]", fontsize=8)

    ax.set_xlim(robot.x_min, robot.x_max)
    ax.set_ylim(robot.y_min, robot.y_max)
    ax.tick_params(axis="both", labelsize=8)
    ax.grid(True)

    image_path = Path(__file__).parent / "assets" / "robot_base.png"

    if image_path.exists():
        robot_img = mpimg.imread(image_path)

        ax.imshow(
            robot_img,
            extent=[
                robot.x_min,
                robot.x_max,
                robot.y_min,
                robot.y_max
            ],
            alpha=0.45,
            aspect="auto",
            zorder=0
        )

    if robot.trajectory:
        target_x = robot.trajectory[-1]["x"]
        target_y = robot.trajectory[-1]["y"]

    target_label = "Target TCP"
    target_color = None

    if active_task in ["pick", "place"]:
        target_label = "Pick/Place target"
        target_color = "gold"

    scatter_kwargs = {
        "marker": "x",
        "s": 90,
        "label": target_label,
        "zorder": 5,
    }

    if target_color:
        scatter_kwargs["color"] = target_color

    ax.scatter(target_x, target_y, **scatter_kwargs)

    if robot.x_coord is not None and robot.y_coord is not None:
        ax.scatter(
            robot.x_coord,
            robot.y_coord,
            s=70,
            label="Current TCP",
            zorder=6
        )

    if robot.trajectory:
        planned_xs = [point["x"] for point in robot.trajectory]
        planned_ys = [point["y"] for point in robot.trajectory]

        ax.plot(
            planned_xs,
            planned_ys,
            linestyle="--",
            linewidth=1,
            label="Planned",
            zorder=3
        )

        executed_points = robot.trajectory[:robot.current_trajectory_step +1]

        if executed_points:
            executed_xs = [point["x"] for point in executed_points]
            executed_ys = [point["y"] for point in executed_points]

            ax.plot(
                executed_xs,
                executed_ys,
                linewidth=2,
                label="Executed",
                zorder=4
            )

    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()

    return fig


create_robot_if_needed()
create_simulation_state_if_needed()

robot = st.session_state.robot

st.title("Gantry Robot Control Logic Prototype")

left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("Control panel")

    if st.button("Reset simulation"):
        st.session_state.robot = GantryRobot()
        st.session_state.plate_present = True
        st.session_state.active_task = None
        st.rerun()

    init_col_1, init_col_2 = st.columns(2)

    with init_col_1:
        if st.button("Power on", use_container_width=True):
            robot.power_on()

    with init_col_2:
        if st.button("Home", use_container_width=True):
            robot.home()
            st.session_state.active_task = None

    st.subheader("Move TCP")

    x_col, y_col, z_col = st.columns(3)

    with x_col:
        target_x = st.number_input(
            "Target X [mm]",
            min_value=float(robot.x_min),
            max_value=float(robot.x_max),
            value=100.0,
            step=10.0
        )

    with y_col:
        target_y = st.number_input(
            "Target Y [mm]",
            min_value=float(robot.y_min),
            max_value=float(robot.y_max),
            value=100.0,
            step=10.0
        )

    with z_col:
        target_z = st.number_input(
            "Target Z [mm]",
            min_value=float(robot.z_min),
            max_value=float(robot.z_max),
            value=50.0,
            step=10.0
        )

    motion_steps = st.slider(
        "Steps per movement segment",
        min_value=2,
        max_value=20,
        value=4,
        help="For pick/place, this is applied to each segment: move above, move down, move up."
    )

    move_col_1, move_col_2 = st.columns(2)

    with move_col_1:
        if st.button("Move TCP", use_container_width=True):
            if robot.move_to(target_x, target_y, target_z, steps=motion_steps):
                st.session_state.active_task = "move"
    

    with move_col_2:
        if st.button("Step motion", use_container_width=True):
            robot.step_motion()

            if robot.status.value != "MOVING":
                st.session_state.active_task = None

    if robot.trajectory:
        total_steps = len(robot.trajectory)
        done_steps = robot.current_trajectory_step
        remaining_steps = max(total_steps - done_steps, 0)

        st.caption(
            f"Motion progress: {done_steps}/{total_steps} steps "
            f"({remaining_steps} remaining)"
        )

        st.progress(done_steps / total_steps)

    st.subheader("Plate simulation")

    st.session_state.plate_present = st.toggle(
        "Plate present in magazine",
        value=st.session_state.plate_present
    )

    st.subheader("Pick / Place")

    pick_col_1, pick_col_2 = st.columns(2)

    with pick_col_1:
        if st.button("Pick plate", use_container_width=True):
            if robot.pick_plate(
                plate_available=st.session_state.plate_present,
                steps=motion_steps
            ):
                st.session_state.active_task = "pick"
                

    with pick_col_2:
        if st.button("Place plate", use_container_width=True):
            if robot.place_plate(steps=motion_steps):
                st.session_state.active_task = "place"
                

    st.divider()

    safe_col_1, safe_col_2 = st.columns(2)

    with safe_col_1:
        if st.button("Emergency stop", use_container_width=True):
            robot.emergency_stop()

    with safe_col_2:
        if st.button("Reset fault / ESTOP", use_container_width=True):
            robot.reset_fault()
            st.session_state.active_task = None

with right_col:
    st.header("Robot status")

    status = robot.get_status()
    position = status["position"]

    status_state = (
        "ok"
        if status["status"] == "READY"
        else "bad"
        if status["status"] in ["FAULT", "ESTOP"]
        else "neutral"
    )

    status_col_1, status_col_2, status_col_3 = st.columns(3)

    with status_col_1:
        status_card("Status", status["status"], status_state)

    with status_col_2:
        status_card(
            "Initialized",
            "YES" if status["is_initialized"] else "NO",
            "ok" if status["is_initialized"] else "bad"
        )

    with status_col_3:
        status_card(
            "Homed",
            "YES" if status["is_homed"] else "NO",
            "ok" if status["is_homed"] else "bad"
        )

    grip_col_1, grip_col_2 = st.columns(2)

    with grip_col_1:
        status_card(
            "Gripping active",
            "YES" if status["is_gripping_active"] else "NO",
            "ok" if status["is_gripping_active"] else "neutral"
        )

    with grip_col_2:
        status_card(
            "Plate gripped",
            "YES" if status["is_gripped"] else "NO",
            "ok" if status["is_gripped"] else "neutral"
        )

    pos_col_1, pos_col_2, pos_col_3 = st.columns(3)

    with pos_col_1:
        status_card(
            "X [mm]",
            f"{position['x']:.2f}" if position["x"] is not None else "Unknown"
        )

    with pos_col_2:
        status_card(
            "Y [mm]",
            f"{position['y']:.2f}" if position["x"] is not None else "Unknown"
        )

    with pos_col_3:
        status_card(
            "Z [mm]",
            f"{position['z']:.2f}" if position["x"] is not None else "Unknown"
        )

    st.pyplot(
        draw_workspace(
            robot,
            target_x,
            target_y,
            active_task=st.session_state.active_task
        )
    )

st.subheader("Event log")

if robot.logs:
    visible_logs = robot.logs[-5:]
    log_df = pd.DataFrame({"Log message": visible_logs})
    st.dataframe(log_df, use_container_width=True, height=220)
else:
    st.info("No logs yet.")