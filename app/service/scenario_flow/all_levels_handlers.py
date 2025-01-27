from app.service.scenario_flow.handlers.go_to_next_level import build_go_to_next_level_command_handler
from app.service.scenario_flow.handlers.open_level_list import build_open_level_list_handler
from app.service.scenario_flow.handlers.reset_level import build_reset_level_command_handler
from app.service.scenario_flow.handlers.select_another_level import build_select_level_command_handler

all_levels_handlers = [
    build_reset_level_command_handler(),
    build_go_to_next_level_command_handler(),
    build_select_level_command_handler(),
    build_open_level_list_handler()
]