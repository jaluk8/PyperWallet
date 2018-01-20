from pyperlib import wallet, prompter, coins
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QComboBox, QLabel, QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
import sys


class GuiWallet(wallet.Wallet):
    """A high-level graphical interface for manipulating coins."""

    def __init__(self, args, prompt=None):
        """Initialize the GuiWallet using Qt."""

        self.app = QApplication(args)
        if prompt is None:
            prompt = prompter.GuiPrompter()
        self.prompt = prompt

        self.Widgets = [CoinWidget, ImporterWidget, SettingsWidget,
                        CryptorWidget, ExporterWidget, OKWidget]

        self.initUI()

        self.mw.show()
        sys.exit(self.app.exec_())

    def initUI(self):
        """Create the UI elements."""
        self.mw = QMainWindow()
        self.mw.setCentralWidget(QWidget())

        self.main_layout = QVBoxLayout()
        self.mw.centralWidget().setLayout(self.main_layout)

        for Widget in self.Widgets:
            w = Widget(self)
            self.addMainWidget(w)

    def addMainWidget(self, widget):
        """Add a widget to the central widget."""
        self.main_layout.addWidget(widget)

    def run(self):
        """Run the wallet."""
        try:
            super().run()
        except Exception as e:
            self.prompt.show_error(e)


class PyperWidget(QWidget):
    """Base class for all custom widgets."""

    def __init__(self, wallet):
        """Initialize the Widget."""
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.wallet = wallet
        self.initUI()

    def add_combo(self, iterable, default="", slot=None):
        """Add a QComboBox to self."""
        combo = QComboBox()
        combo.addItems(iterable)
        self.layout().addWidget(combo)

        combo.setCurrentText(default)

        if slot is not None:
            combo.currentTextChanged.connect(slot)
            slot(default)

    def add_check(self, text, default=False, slot=None):
        """Add a QCheckBox to self."""
        check = QCheckBox(text)
        self.layout().addWidget(check)

        if default:
            default = Qt.Checked
        else:
            default = Qt.Unchecked
        check.setCheckState(default)

        if slot is not None:
            check.stateChanged.connect(slot)
            slot(default)

    def add_label(self, text):
        """Add a QLabel to self."""
        label = QLabel(text)
        self.layout().addWidget(label)

    def add_button(self, text, slot=None):
        """Add a QPushButton to self."""
        button = QPushButton(text)
        self.layout().addWidget(button)

        if slot is not None:
            button.clicked.connect(slot)


class CoinWidget(PyperWidget):
    """Use Qt to set up a coin."""

    def initUI(self):
        """Create the widget's UI."""
        coin_list = self.wallet.coin_f.list()

        self.add_label("Coin name:")
        self.add_combo(coin_list, "bitcoin", self.set_coin)

    def set_coin(self, text):
        """Set the wallet's coin to text."""
        self.wallet.Coin = text


class ImporterWidget(PyperWidget):
    """Use Qt to set up an importer."""

    def initUI(self):
        """Create the widget's UI."""
        importer_list = self.wallet.importer_f.list()

        self.add_label("Create coin with:")
        self.add_combo(importer_list, "gen", self.set_importer)

    def set_importer(self, text):
        """Set the wallet's importer to text."""
        self.wallet.Importer = text


class SettingsWidget(PyperWidget):
    """Use Qt to set up coin settings."""

    def initUI(self):
        """Create the widget's UI."""
        settings = coins.CoinSettings.settings
        for s in settings:
            slot = self.make_slot(s)
            if s.s_type is bool:
                self.add_check(s.name, s.default, slot)

    def make_slot(self, setting):
        """Create a slot for the setting's signal."""

        def bool_slot(state):
            """A slot for a boolean type."""
            if type(state) is int:
                state = state == Qt.Checked
            self.apply_setting(setting.name, state)

        if setting.s_type is bool:
            return bool_slot

    def apply_setting(self, name, value):
        """Apply a setting to the wallet's setting object."""
        self.wallet.kwargs[name] = value


class CryptorWidget(PyperWidget):
    """Use Qt to set up a cryptor."""

    def initUI(self):
        """Create the widget's UI."""
        cryptor_list = self.wallet.cryptor_f.list() + ["none"]

        self.add_label("Encryption method:")
        self.add_combo(cryptor_list, "none", self.set_cryptor)

    def set_cryptor(self, text):
        """Set the wallet's cryptor to text."""
        self.wallet.Cryptor = text


class ExporterWidget(PyperWidget):
    """Use Qt to set up an exporter."""

    def initUI(self):
        """Create the widget's UI."""
        exporter_list = self.wallet.exporter_f.list()

        self.add_label("Exporter:")
        self.add_combo(exporter_list, "text", self.set_exporter)

    def set_exporter(self, text):
        """Set the wallet's exporter to text."""
        self.wallet.Exporter = text


class OKWidget(PyperWidget):
    """Use Qt to run the wallet."""

    def initUI(self):
        """Create the widget's UI."""
        self.add_button("Run", self.wallet.run)
