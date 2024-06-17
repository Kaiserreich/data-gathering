import webdriver_form_filler as wff


class DataTestClass:
    def __init__(self, input_data: dict, expected_lines: dict) -> None:
        self.input_data = input_data
        self.expected_lines = expected_lines
        self.input_data["END"] = "14:00, 21 December, 1945"

    def test_correct_input(self):
        answers = wff.extract_data_for_webdriver_script(self.input_data)[0]
        try:
            for key, value in self.expected_lines.items():
                assert str(answers[key]) == str(value), f"Values should match! {key}, Expected - {value}, actual - {answers[key]}"
        except KeyError as ex:
            assert False, f"Key error encountered, looks like expected line is entirely missing! {ex}"
