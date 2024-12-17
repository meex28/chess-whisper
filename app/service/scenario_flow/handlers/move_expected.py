import chess

from app.backend.chess_engine.user_commands import recognise_move_command
from app.levels.types import ScenarioStepCallback, UserInputHandler, LevelState, UserInputHandlerResult, \
    RecognisedMoveIncorrectReason
from app.service.scenario_flow.callbacks.assistant_text import assistant_unrecognized_input_callback, \
    build_assistant_text_callback

incorrect_move_responses: dict[RecognisedMoveIncorrectReason, str] = {
    RecognisedMoveIncorrectReason.NOT_ENOUGH_INFO: "Nie udało się rozpoznać ruchu. Podano zbyt mało informacji.",
    RecognisedMoveIncorrectReason.PIECE_NOT_SELECTED: "Na podanym polu nie znajduje się żadna bierka. Wybierz pole z bierką w twoim kolorze.",
    RecognisedMoveIncorrectReason.MULTIPLE_PIECES_FOUND: "Na planszy jest więcej niż jedna bierka tego typu. Wskaż konkretne pole do ruchu.",
    RecognisedMoveIncorrectReason.PIECE_TYPE_MISMATCH: "Typ bierki na wskazanym polu nie zgadza się z wybranym typem bierki.",
    RecognisedMoveIncorrectReason.WRONG_PLAYER_PIECE: "Wybrana bierka nie należy do Ciebie. Wybierz inną bierkę w twoim kolorze.",
    RecognisedMoveIncorrectReason.ILLEGAL_MOVE: "Wybrany ruch jest niedozwolony. Spróbuj ponownie."
}

def build_user_move_expected_handler(expected_move: chess.Move, unexpected_move_response: str, callbacks: list[ScenarioStepCallback]) -> UserInputHandler:
    def run(user_input: str, level_state: LevelState) -> UserInputHandlerResult:
        recognised_move = recognise_move_command(
            player_color=level_state.user_color,
            board=level_state.board,
            raw_text=user_input
        )

        if recognised_move is None:
            # TODO: if we have more handlers we shouldn't accept allways this handler but do better validation in recognise_move_command
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[assistant_unrecognized_input_callback]
            )

        if not recognised_move.correct:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(incorrect_move_responses[recognised_move.reason])]
            )

        if not recognised_move.chess_move == expected_move:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(unexpected_move_response)]
            )

        return UserInputHandlerResult(
            accepted=True,
            callbacks=callbacks
        )
    return run
