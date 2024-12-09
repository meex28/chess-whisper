from app.service.session_state import get_level_state


def run_scenario_step():
    level_state = get_level_state()

    print(level_state)

    print(f"Running scenario step index: {level_state.scenario_step_index}")

    current_step = level_state.level.scenario.steps[level_state.scenario_step_index]

    for i, callback in enumerate(current_step.callbacks):
        print(f"Running callback index: {i}")
        callback()
