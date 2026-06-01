# app.py

from pathlib import Path

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
    div[data-testid="stMetric"] {
        padding: 0.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def create_robot_if_needed():
    if "robot" not in st.session_state:
        st.session_state.robot = GantryRobot()


def draw_workspace(robot, target_x, target_y):
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
            alpha=0.25,
            aspect="auto",
            zorder=0
        )

    ax.scatter(
        target_x,
        target_y,
        marker="x",
        s=70,
        label="Target TCP",
        zorder=5
    )

    if robot.x is not None and robot.y is not None:
        ax.scatter(
            robot.x,
            robot.y,
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

        executed_points = robot.trajectory[:robot.current_trajectory_step]

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
robot = st.session_state.robot

st.title("Gantry Robot Control Logic Prototype")

left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("Control panel")

    if st.button("Reset simulation"):
        st.session_state.robot = GantryRobot()
        st.rerun()

    if st.button("Power on"):
        robot.power_on()

    if st.button("Home"):
        robot.home()

    st.subheader("Move TCP")

    target_x = st.number_input(
        "Target X [mm]",
        min_value=float(robot.x_min),
        max_value=float(robot.x_max),
        value=100.0,
        step=10.0
    )

    target_y = st.number_input(
        "Target Y [mm]",
        min_value=float(robot.y_min),
        max_value=float(robot.y_max),
        value=100.0,
        step=10.0
    )

    target_z = st.number_input(
        "Target Z [mm]",
        min_value=float(robot.z_min),
        max_value=float(robot.z_max),
        value=50.0,
        step=10.0
    )

    motion_steps = st.slider(
        "Number of motion steps",
        min_value=5,
        max_value=100,
        value=30,
        help="This value defines how many simulation steps the movement takes."
    )

    if st.button("Move TCP"):
        if robot.move_to(target_x, target_y, target_z, steps=motion_steps):
            robot.step_motion()

    if st.button("Step motion"):
        robot.step_motion()

    if robot.trajectory:
        total_steps = len(robot.trajectory)
        done_steps = robot.current_trajectory_step
        remaining_steps = max(total_steps - done_steps, 0)

        st.caption(
            f"Motion progress: {done_steps}/{total_steps} steps "
            f"({remaining_steps} remaining)"
        )

        st.progress(done_steps / total_steps)

    st.divider()

    if st.button("Emergency stop"):
        robot.emergency_stop()

    if st.button("Reset fault / ESTOP"):
        robot.reset_fault()

with right_col:
    st.header("Robot status")

    status = robot.get_status()
    position = status["position"]

    status_col_1, status_col_2 = st.columns(2)
    status_col_1.metric("State", status["state"])
    status_col_2.metric("Homed", str(status["is_homed"]))

    pos_col_1, pos_col_2, pos_col_3 = st.columns(3)
    pos_col_1.metric("X [mm]", position["x"] if position["x"] is not None else "Unknown")
    pos_col_2.metric("Y [mm]", position["y"] if position["y"] is not None else "Unknown")
    pos_col_3.metric("Z [mm]", position["z"] if position["z"] is not None else "Unknown")

    st.pyplot(draw_workspace(robot, target_x, target_y))

st.subheader("Event log")

if robot.logs:
    visible_logs = robot.logs[-8:]
    log_df = pd.DataFrame({"Log message": visible_logs})
    st.dataframe(log_df, use_container_width=True, height=220)
else:
    st.info("No logs yet.")