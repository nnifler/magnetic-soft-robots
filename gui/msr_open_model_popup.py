from pathlib import Path
from typing import List
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QMainWindow,
                               QLabel, QPushButton, QListWidget, QMessageBox,)
from src import Config


class MSROpenModelsPopup(QWidget):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        self.setWindowTitle("Models")
        self.resize(600, 400)

        self._main_window = main_window
        self._layout = QVBoxLayout(self)
        self.default_list = QListWidget()
        self.custom_list = QListWidget()

        default_label = QLabel("Default Models:")
        custom_label = QLabel("Custom Models:")

        lib_path = Path(__file__).parents[1] / "lib"

        self.load_models(self.default_list, lib_path / "models")
        self.default_list.itemClicked.connect(
            lambda item:
            self.update_loaded_model(item.text(), False, [self.custom_list]))

        self.load_models(self.custom_list, lib_path / "imported_models")
        self.custom_list.itemClicked.connect(
            lambda item:
            self.update_loaded_model(item.text(), True, [self.default_list]))

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        self._layout.addWidget(default_label)
        self._layout.addWidget(self.default_list)
        self._layout.addWidget(custom_label)
        self._layout.addWidget(self.custom_list)
        self._layout.addWidget(close_button)

    def update_loaded_model(self, model_name: str, custom_model: bool,
                            other_widgets: List[QListWidget] = None, scale=0.02) -> None:
        """Updates the loaded model in the config.

        Args:
            model_name (str): The name of the model to load.
            custom_model (bool): Whether the model is a custom model.
            other_widgets (Optional[List[QListWidget]], optional): Other widgets to clear the selection of. Defaults to None.
            scale (float, optional): The scale of the model shown in the simulation. Defaults to 0.02.
        """
        # TODO: accept different file suffixes
        # TODO: make scaling factor configurable
        if other_widgets is not None:
            for widget in other_widgets:
                widget.clearSelection()

        Config.set_model(model_name, scale, custom_model)
        self._main_window.update_model()

    def load_models(self, list_widget: QListWidget, models_path: Path) -> None:
        """Loads the default models from the default folder into the list widget.

        Args:
            list_widget (QListWidget): The list widget to add the items to.
            models_path (Path): The path to the models folder.
        """
        if not models_path.exists():
            QMessageBox.warning(
                self, "Error", f"Models folder not found at: {models_path}")
            return

        model_names = list(
            {path.stem for path in models_path.iterdir()} - {".gitkeep"})
        # use set comprehension to remove duplicates
        for model_name in model_names:
            list_widget.addItem(model_name)
