# -*- coding: utf-8 -*-
"""A GUI for Transfer Characteristics.

このファイルは ./transfer_characteristics.ui を雛形に作成されたものです．
ただし，種々操作を記述する必要性から，独自に編集を加えていきます．

つまり, ./transfer_characteristics.ui を利用しても，
これと同様の GUI は作成されないものと思ってください．
"""
from os import path
from PySide2 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg

ICONDIR = path.join(path.dirname(path.abspath(__file__)), "icons")


class Ui_MainWindow(object):

    devices = []
    device_settings = {"input_device_index": None, "output_device_index": None}
    default_settings = {
        "analytical_method": "chirp",
        "duration": 60,
        "fs": 96,
        "gen_options": {
            "f0": 2,
            "f1": 40,
        }
    }
    analytical_method = default_settings["analytical_method"]
    duration = default_settings["duration"]
    fs = default_settings["fs"]
    gen_options = default_settings["gen_options"]
    object_datas = None
    subject_datas = None
    recs = 0
    cols = [
        "g",
        "r",
        "y",
    ]

    def set_devices(self):
        from wave_io import get_devices
        self.devices = get_devices()

    def set_input_device(self, value):
        self.device_settings["input_device_index"] = value
        self.statusbar.showMessage("Change input device !!")

    def set_output_device(self, value):
        self.device_settings["output_device_index"] = value
        self.statusbar.showMessage("Change output device !!")

    def set_duration(self, value):
        self.duration = value
        self.statusbar.showMessage("Change sound duration !!")

    def set_fs(self, value):
        self.fs = value
        self.statusbar.showMessage("Change sound sampling rate !!")

    def set_f0(self, value):
        self.gen_options["f0"] = value
        self.statusbar.showMessage("Change charps setting (f0) !!")

    def set_f1(self, value):
        self.gen_options["f1"] = value
        self.statusbar.showMessage("Change charps setting (f1) !!")

    def on_recording(self):
        from signals import fft, to_dB
        from wave_io import playrec
        self.statusbar.showMessage("On Recording !!")
        if self.object_datas is None:
            self.gen_signal()
        options = {
            "fs": self.fs,
        }
        self.subject_datas = playrec(self.object_datas, **options)
        self.statusbar.showMessage("Fin Recording !!")

        if self.subject_datas is None:
            self.statusbar.showMessage("Faild Recording")
        else:
            self.statusbar.showMessage("Now Analysed Data!")
            for i in range(self.subject_datas.ndim):
                data = self.subject_datas[:, i]
                freq, amp = fft(data)
                self.fftGraphicsView.plot(
                    freq, to_dB(amp), pen=self.cols[i + 1]
                )
        self.statusbar.showMessage("Fin Plotting !!")

    def gen_chirp(self):
        """チャープ音を生成します."""
        from signals import gen_chirp, fft, to_dB
        self.statusbar.showMessage("Gen Charp Signal !!")
        _f0 = self.gen_options.get("f0")
        _f1 = self.gen_options.get("f1") * 1000
        t, self.object_datas = gen_chirp(
            self.duration, fs=self.fs, f0=_f0, f1=_f1
        )
        freq, amp = fft(self.object_datas)
        self.waveGraphicsView.clear()
        self.waveGraphicsView.plot(t, self.object_datas)
        self.fftGraphicsView.clear()
        self.fftGraphicsView.plot(
            freq, to_dB(amp), pen=self.cols[0], name='base'
        )
        lr = pg.LinearRegionItem([20, 20000])
        lr.setZValue(-10)
        self.fftGraphicsView.addItem(lr)
        self.fftGraphicsView.showGrid(x=True, y=True)

    def gen_signal(self):
        if self.analytical_method == "chirp":
            self.gen_chirp()

    def save_plot(self):
        from PySide2.QtWidgets import QFileDialog
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(
            None, "Open Image", path.expanduser("~"),
            "Image Files (*.png *.jpg *.bmp)"
        )
        if fileName:
            from pyqtgraph.exporters import ImageExporter
            exporter = ImageExporter(self.fftGraphicsView.plotItem)
            exporter.export(fileName)

    def setupMenu(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 31))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "File", None, -1)
        )

        self.menuNew = QtWidgets.QMenu(self.menu)
        self.menuNew.setObjectName("menuNew")
        self.menuNew.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "New...", None, -1)
        )

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings.setTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Settings", None, -1
            )
        )
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Help", None, -1)
        )
        MainWindow.setMenuBar(self.menubar)

        self.actionCharp = QtWidgets.QAction(MainWindow)
        self.actionCharp.setObjectName("actionCharp")
        self.actionCharp.setText(
            QtWidgets.QApplication.translate("MainWindow", "Charp", None, -1)
        )
        self.actionRecord = QtWidgets.QAction(MainWindow)
        self.actionRecord.setObjectName("actionRecord")
        self.actionRecord.setText(
            QtWidgets.QApplication.translate("MainWindow", "Record", None, -1)
        )
        self.actionPreference = QtWidgets.QAction(MainWindow)
        self.actionPreference.setObjectName("actionPreference")
        self.actionPreference.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Preference ...", None, -1
            )
        )

        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "About ...", None, -1
            )
        )

        self.menuNew.addAction(self.actionCharp)
        self.menu.addAction(self.menuNew.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.actionRecord)
        self.menuSettings.addAction(self.actionPreference)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

    def setupMain(self, MainWindow):
        # --------------------------------------------------------------------
        # トップボタンバー
        # --------------------------------------------------------------------
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 収録ボタン
        record_icon = QtGui.QIcon(
            path.join(
                ICONDIR,
                "baseline-fiber_smart_record-24px.svg",
            )
        )
        self.recordingButton = QtWidgets.QToolButton(self.centralwidget)
        self.recordingButton.setObjectName("recordingButton")
        self.recordingButton.clicked.connect(self.on_recording)
        self.recordingButton.setIcon(record_icon)
        # self.recordingButton.setText(
        #     QtWidgets.QApplication.translate(
        #         "MainWindow", "Recording", None, -1
        #     )
        # )
        self.horizontalLayout.addWidget(self.recordingButton)

        # save ボタン
        save_icon = QtGui.QIcon(
            path.join(
                ICONDIR,
                "baseline-save-24px.svg",
            )
        )
        self.saveImageButton = QtWidgets.QToolButton(self.centralwidget)
        self.saveImageButton.setObjectName("saveImageButton")
        self.saveImageButton.clicked.connect(self.save_plot)
        self.saveImageButton.setIcon(save_icon)
        self.horizontalLayout.addWidget(self.saveImageButton)

        # スペーサー
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)

        # 音源持続時間
        self.durationLabel = QtWidgets.QLabel(self.centralwidget)
        self.durationLabel.setObjectName("durationLabel")
        self.horizontalLayout.addWidget(self.durationLabel)

        self.durationSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.durationSpinBox.setObjectName("durationSpinBox")
        self.durationSpinBox.setValue(self.duration)
        self.durationSpinBox.setSuffix("sec")
        self.durationSpinBox.valueChanged.connect(self.set_duration)
        self.horizontalLayout.addWidget(self.durationSpinBox)

        # 開始周波数
        self.f0Label = QtWidgets.QLabel(self.centralwidget)
        self.f0Label.setObjectName("f0Label")
        self.horizontalLayout.addWidget(self.f0Label)

        self.f0SpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.f0SpinBox.setObjectName("f0SpinBox")
        self.f0SpinBox.setValue(self.gen_options["f0"])
        self.f0SpinBox.setSuffix("Hz")
        self.f0SpinBox.valueChanged.connect(self.set_f0)
        self.horizontalLayout.addWidget(self.f0SpinBox)

        # 修了周波数
        self.f1Label = QtWidgets.QLabel(self.centralwidget)
        self.f1Label.setObjectName("f1Label")
        self.horizontalLayout.addWidget(self.f1Label)

        self.f1SpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.f1SpinBox.setObjectName("f1SpinBox")
        self.f1SpinBox.setValue(self.gen_options["f1"])
        self.f1SpinBox.setSuffix("kHz")
        self.f1SpinBox.valueChanged.connect(self.set_f1)
        self.horizontalLayout.addWidget(self.f1SpinBox)

        # 音源作成ボタン
        self.genSignalButton = QtWidgets.QPushButton(self.centralwidget)
        self.genSignalButton.setObjectName("genSignalButton")
        self.genSignalButton.clicked.connect(self.gen_signal)
        self.genSignalButton.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Gen signals...", None, -1
            )
        )
        self.horizontalLayout.addWidget(self.genSignalButton)

        # 画像領域
        # -------------------------------------
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # 音声波形表示
        self.waveGraphicsView = pg.PlotWidget(
            self.centralwidget, title='Sound Wave'
        )
        self.waveGraphicsView.setObjectName("waveGraphicsView")
        self.verticalLayout.addWidget(self.waveGraphicsView)

        # 音声波形表示
        self.fftGraphicsView = pg.PlotWidget(self.centralwidget, title="SPL")
        self.fftGraphicsView.setObjectName("fftGraphicsView")
        self.verticalLayout.addWidget(self.fftGraphicsView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Transfer Characteristics")
        MainWindow.resize(917, 626)

        self.setupMenu(MainWindow)
        self.setupMain(MainWindow)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 種々初期化
        # -------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "MainWindow", None, -1
            )
        )

        self.durationLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "Time:", None, -1)
        )
        self.f0Label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Freq:", None, -1)
        )
        self.f1Label.setText(
            QtWidgets.QApplication.translate("MainWindow", "-", None, -1)
        )
