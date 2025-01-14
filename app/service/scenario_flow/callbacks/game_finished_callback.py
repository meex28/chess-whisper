from app.service.session_state.level_state import set_game_finished


def build_game_finished_callback():
    def run():
        set_game_finished(is_finished=True)
    return run
