# -*- coding: utf-8 -*-
"""A GUI for Transfer Characteristics.

このファイルは ./transfer_characteristics.ui を雛形に作成されたものです．
ただし，種々操作を記述する必要性から，独自に編集を加えていきます．

つまり, ./transfer_characteristics.ui を利用しても，
これと同様の GUI は作成されないものと思ってください．
"""
from PySide2 import QtCore, QtWidgets
import pyqtgraph as pg


class Ui_MainWindow(object):

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

    def set_duration(self, value):
        self.duration = value

    def set_fs(self, value):
        self.fs = value

    def set_f0(self, value):
        self.gen_options["f0"] = value

    def set_f1(self, value):
        self.gen_options["f1"] = value

    def on_recording(self):
        print("On Record fired!")
        from signals import fft, to_dB
        self.recs = self.recs + 1
        if self.object_datas is not None:
            from wave_io import playrec
            self.subject_datas = playrec(self.object_datas, fs=self.fs)
            print("subject_datas")
            print("Fin Recording.")
            if self.subject_datas is not None:
                for i in range(self.subject_datas.ndim):
                    data = self.subject_datas[i]
                    freq, amp = fft(data)
                    print(amp)
                    self.fftGraphicsView.plot(
                        freq,
                        to_dB(amp),
                        pen='r',
                        name='res_{}: channel = {}'.format(
                            str(self.recs), str(i)
                        )
                    )
                print("Fin plot")
        else:
            from wave_io import rec
            self.subject_datas = rec(self.duration, fs=self.fs)
            freq, amp = fft(self.subject_datas)
            self.fftGraphicsView.plot(freq, to_dB(amp))

    def gen_chirp(self):
        from signals import gen_chirp, fft, to_dB
        _f0 = self.gen_options.get("f0")
        _f1 = self.gen_options.get("f1") * 1000
        t, self.object_datas = gen_chirp(
            self.duration, fs=self.fs, f0=_f0, f1=_f1
        )
        freq, amp = fft(self.object_datas)
        self.waveGraphicsView.clear()
        self.waveGraphicsView.plot(t, self.object_datas)
        self.fftGraphicsView.clear()
        self.fftGraphicsView.plot(freq, to_dB(amp), pen='g', name='base')

    def gen_signal(self):
        print("Gen Signal fired!")
        if self.analytical_method == "chirp":
            self.gen_chirp()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Transfer Characteristics")
        MainWindow.resize(917, 626)

        # --------------------------------------------------------------------
        # メニューバー
        # --------------------------------------------------------------------
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 31))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuNew = QtWidgets.QMenu(self.menu)
        self.menuNew.setObjectName("menuNew")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCharp = QtWidgets.QAction(MainWindow)
        self.actionCharp.setObjectName("actionCharp")
        self.actionRecord = QtWidgets.QAction(MainWindow)
        self.actionRecord.setObjectName("actionRecord")
        self.actionPreference = QtWidgets.QAction(MainWindow)
        self.actionPreference.setObjectName("actionPreference")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuNew.addAction(self.actionCharp)
        self.menu.addAction(self.menuNew.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.actionRecord)
        self.menuSettings.addAction(self.actionPreference)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # --------------------------------------------------------------------
        # トップボタンバー
        # --------------------------------------------------------------------
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 収録ボタン
        self.recordingButton = QtWidgets.QToolButton(self.centralwidget)
        self.recordingButton.setObjectName("recordingButton")
        self.recordingButton.clicked.connect(self.on_recording)
        self.horizontalLayout.addWidget(self.recordingButton)

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

        # 評価領域
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout)

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
        self.recordingButton.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Recording", None, -1
            )
        )

        self.genSignalButton.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Gen signals...", None, -1
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
        self.label.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "評価: xxxxx", None, -1
            )
        )
        self.menu.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "File", None, -1)
        )
        self.menuNew.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "New...", None, -1)
        )
        self.menuSettings.setTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Settings", None, -1
            )
        )
        self.menuHelp.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Help", None, -1)
        )
        self.actionCharp.setText(
            QtWidgets.QApplication.translate("MainWindow", "Charp", None, -1)
        )
        self.actionRecord.setText(
            QtWidgets.QApplication.translate("MainWindow", "Record", None, -1)
        )
        self.actionPreference.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Preference ...", None, -1
            )
        )
        self.actionAbout.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "About ...", None, -1
            )
        )
