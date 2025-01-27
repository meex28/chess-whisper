from app.levels.all_levels import all_levels, find_level_by_id
from app.levels.types import UserInputHandler, LevelState, UserInputHandlerResult
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.callbacks.select_level import build_select_level_callback
import string


def build_select_level_command_handler() -> UserInputHandler:
    def run(user_input: str, _: LevelState) -> UserInputHandlerResult:
        change_level_keywords = ["zmień poziom", "wybierz poziom", "przejdź do poziomu"]
        ignored_words = ["na", "do", '.', ',']
        starts_with_keyword = any(user_input.lower().startswith(keyword) for keyword in change_level_keywords)

        if not starts_with_keyword:
            return UserInputHandlerResult(accepted=False, callbacks=[])

        user_input = user_input.translate(str.maketrans('', '', string.punctuation))
        words = user_input.lower().split()
        level_id = None

        number_words = [
            ("0", ["zero", "zerowego"]),
            ("1", ["jeden", "pierwszy", "pierwszego"]),
            ("2", ["dwa", "drugi", "drugiego"]),
            ("3", ["trzy", "trzeci", "trzeciego"]),
            ("4", ["cztery", "czwarty", "czwartego"]),
            ("5", ["pięć", "piąty", "piątego"]),
            ("6", ["sześć", "szósty", "szóstego"]),
            ("7", ["siedem", "siódmy", "siódmego"]),
            ("8", ["osiem", "ósmy", "ósmego"]),
            ("9", ["dziewięć", "dziewiąty", "dziewiątego"]),
            ("10", ["dziesięć", "dziesiąty", "dziesiątego"]),
            ("11", ["jedenaście", "jedenasty", "jedensatego"])
        ]

        for i, word in enumerate(words):
            if word.isdigit():
                level_id = word
                break

            for number, synonyms in number_words:
                if word in synonyms:
                    level_id = number
                    break

        if level_id is None:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(
                    "Nie rozpoznałem numeru poziomu. Powiedz na przykład 'zmień poziom na dwa' lub 'przejdź do poziomu trzeciego'."
                )]
            )

        selected_level = find_level_by_id(level_id)
        if selected_level is None:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(
                    f"Nie znalazłem poziomu o numerze {level_id}. Dostępne poziomy: {', '.join([str(l.id) for l in all_levels])}."
                )]
            )

        return UserInputHandlerResult(
            accepted=True,
            callbacks=[
                build_assistant_text_callback(f"Zmieniam na poziom {level_id}: {selected_level.name}."),
                build_select_level_callback(selected_level)
            ]
        )

    return run