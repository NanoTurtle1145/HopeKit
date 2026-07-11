"""
TCP 聊天室 demo
基于 PyQt/PySide + socket 的局域网聊天室
支持创建服务器 / 加入服务器，多客户端广播通信
"""

import socket

from hopekit.qt_compat import (
    QtCore, Signal,
    QMainWindow, QWidget,
    QGridLayout, QVBoxLayout,
    QGroupBox, QLabel, QLineEdit,
    QPushButton, QRadioButton,
    QTextEdit, QStatusBar, QThread,
)


class ServerThread(QThread):
    _signal = Signal(str)
    _text = Signal(str)
    _flag = Signal(str)

    def __init__(self, server_id: str, server_socket: socket.socket):
        super().__init__()
        self.serverID = server_id
        self.serverSocket = server_socket
        self.clientsocket: socket.socket | None = None
        self.addr = None
        self.runflag = True

    def run(self):
        self._emit_signal("等待用户加入……")
        self.clientsocket, self.addr = self.serverSocket.accept()
        self._emit_text(f"正在连接IP为 {self.addr} 的服务器！")
        self._emit_flag("connect")
        self._receive_loop()

    def _receive_loop(self):
        while self.runflag:
            try:
                data = self.clientsocket.recv(1024).decode('utf-8')
                self._emit_text(data)
            except Exception as reason:
                self._emit_signal(str(reason))
                self._emit_text(f"{self.addr} 退出了服务器...")
                self._emit_flag("disconnect")
                break
        self.clientsocket.close()

    def sendToClient(self, info: str):
        try:
            self.clientsocket.send(info.encode("utf-8"))
        except Exception as reason:
            self._emit_signal(f"广播失败: {reason}")
            self._emit_text(f"{self.addr} 退出了服务器...")
            self._emit_flag("disconnect")

    def _emit_signal(self, message: str):
        self._signal.emit(f"{self.serverID}@@@{message}")

    def _emit_text(self, text: str):
        self._text.emit(text)

    def _emit_flag(self, status: str):
        self._flag.emit(f"{self.serverID}@@@{status}")


class ClientThread(QThread):
    _signal = Signal(str)
    _text = Signal(str)
    _flag = Signal(str)

    def __init__(self, sock: socket.socket):
        super().__init__()
        self.serverSocket = sock
        self.runflag = True

    def connectServer(self, ip: str, port: int) -> bool:
        try:
            self.serverSocket.connect((ip, port))
            self._flag.emit("connect")
            return True
        except Exception as reason:
            self._signal.emit(str(reason))
            self._flag.emit("disconnect")
            return False

    def run(self):
        while self.runflag:
            try:
                msg = self.serverSocket.recv(1024).decode("utf-8")
                self._text.emit(msg)
            except Exception as reason:
                self._signal.emit(str(reason))
                self._flag.emit("disconnect")
                break


class Server:
    def __init__(self, widget, ip: str, host: str, port: int):
        self.widget = widget
        self.ip = ip
        self.hostName = host
        self.port = port
        self.serverDict: dict[str, ServerThread] = {}
        self.serverID = 0
        self._build_socket()

    def _build_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self._spawn_thread()

    def _spawn_thread(self):
        server = ServerThread(str(self.serverID), self.socket)
        self.serverDict[str(self.serverID)] = server
        self.serverID += 1
        server._flag.connect(self._on_flag)
        server._signal.connect(self._on_message)
        server._text.connect(self._on_text)
        server.start()

    def _broadcast(self, info: str):
        for sid, thread in list(self.serverDict.items()):
            try:
                if thread.clientsocket is not None:
                    thread.sendToClient(info)
            except Exception:
                self._on_flag(f"{sid}@@@disconnect")

    def btnsend(self, text: str):
        self.widget.chatEdit.append(text)
        self._broadcast(text)

    def closeThread(self):
        for thread in self.serverDict.values():
            thread.runflag = False

    def _on_flag(self, flag: str):
        parts = flag.split("@@@")
        if len(parts) < 2:
            return
        sid, status = parts[0], parts[1]
        if status == "connect":
            self._spawn_thread()
        elif status == "disconnect":
            self.serverDict[sid].runflag = False

    def _on_message(self, signal: str):
        parts = signal.split("@@@")
        if len(parts) >= 2:
            self.widget.statusBar.showMessage(f"serverID为{parts[0]} 状态：{parts[1]}")

    def _on_text(self, text: str):
        self.widget.chatEdit.append(text)
        self._broadcast(text)


class Client:
    def __init__(self, widget, ip: str, hostName: str, port: int):
        self.widget = widget
        self.ip = ip
        self.hostName = hostName
        self.port = port
        self._build_socket()

    def _build_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = ClientThread(self.socket)
        self.client._flag.connect(self._on_flag)
        self.client._signal.connect(self._on_message)
        self.client._text.connect(self._on_text)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()

    def btnsend(self, text: str):
        try:
            self.socket.send(text.encode('utf-8'))
        except Exception as reason:
            self._on_message(str(reason))
            self._on_flag("disconnect")

    def closeThread(self):
        self.client.runflag = False

    def _on_flag(self, flag: str):
        if flag == "connect":
            self.widget.statusBar.showMessage("成功连接！")
        elif flag == "disconnect":
            self.client.runflag = False

    def _on_message(self, signal: str):
        self.widget.statusBar.showMessage(str(signal))

    def _on_text(self, text: str):
        self.widget.chatEdit.append(text)


class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pc = None
        self.setWindowTitle("HopeKit 聊天室")
        self._create_widgets()
        self._compose_layout()

    def _create_widgets(self):
        self.chatEdit = QTextEdit()
        self.chatEdit.setReadOnly(True)

        self.inputLine = QLineEdit()
        self.sendBtn = QPushButton("发送")
        self.sendBtn.clicked.connect(self._send_info)

        self.ipEdit = QLineEdit()
        self.ipEdit.setInputMask('000.000.000.000; ')

        self.hostIPbtn = QPushButton("获取本机IP")
        self.hostIPbtn.clicked.connect(self._get_host_ip)

        self.portEdit = QLineEdit()
        self.portEdit.setPlaceholderText("1145")

        self.hostEdit = QLineEdit()
        self.hostEdit.setPlaceholderText(socket.gethostname())

        self.serverRbtn = QRadioButton("创建服务器")
        self.serverRbtn.setChecked(True)
        self.serverRbtn.toggled.connect(self._radio_changed)

        self.clientRbtn = QRadioButton("加入服务器")

        self.connectBtn = QPushButton("连接")
        self.connectBtn.clicked.connect(self._set_client)
        self.connectBtn.setEnabled(False)

        self.buildServerBtn = QPushButton("创建")
        self.buildServerBtn.clicked.connect(self._set_server)

        self.quitBtn = QPushButton("退出")
        self.quitBtn.clicked.connect(self._quit)

        self.statusBar = QStatusBar()

        self.configBox = QGroupBox("连接信息")
        self.controlBox = QGroupBox("控制面板")

    def _compose_layout(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.setStatusBar(self.statusBar)

        main_layout = QGridLayout(central)
        main_layout.addWidget(self.chatEdit, 0, 0, 9, 2)
        main_layout.addWidget(self.inputLine, 9, 0, 1, 1)
        main_layout.addWidget(self.sendBtn, 9, 1, 1, 1)

        config_layout = QGridLayout(self.configBox)
        config_layout.addWidget(QLabel("服务器IP地址"), 0, 0)
        config_layout.addWidget(self.ipEdit, 1, 0, 1, 3)
        config_layout.addWidget(self.hostIPbtn, 1, 3)
        config_layout.addWidget(QLabel("服务器端口"), 2, 0)
        config_layout.addWidget(self.portEdit, 2, 1, 1, 3)
        config_layout.addWidget(QLabel("昵称"), 3, 0)
        config_layout.addWidget(self.hostEdit, 3, 1, 1, 3)
        config_layout.addWidget(self.serverRbtn, 4, 0, 1, 2)
        config_layout.addWidget(self.clientRbtn, 4, 2, 1, 2)

        control_layout = QVBoxLayout(self.controlBox)
        control_layout.addWidget(self.connectBtn)
        control_layout.addWidget(self.buildServerBtn)
        control_layout.addWidget(self.quitBtn)

        main_layout.addWidget(self.configBox, 0, 2, 5, 10)
        main_layout.addWidget(self.controlBox, 5, 2, 5, 10)

    def _radio_changed(self, is_server: bool):
        self.connectBtn.setEnabled(not is_server)
        self.buildServerBtn.setEnabled(is_server)

    def _get_host_ip(self):
        hostip = socket.gethostbyname_ex(socket.gethostname())
        self.ipEdit.setText(hostip[-1][-1])

    def _send_info(self):
        if self.pc is None:
            self.statusBar.showMessage("发送失败！（未连接）")
            return
        info = self.inputLine.text()
        if not info:
            self.statusBar.showMessage("不能发送空信息！")
            return
        info = f"{self.pc.hostName}:\n{info}"
        self.pc.btnsend(info)

    def _set_server(self):
        host = self.hostEdit.text() or "服务器管理员"
        port = int(self.portEdit.text() or 1145)
        ip = self.ipEdit.text()
        if ip in ("", "..."):
            ip = "127.0.0.1"
        self.pc = Server(self, ip, host, port)

    def _set_client(self):
        host = self.hostEdit.text() or "匿名用户"
        port = int(self.portEdit.text() or 1145)
        ip = self.ipEdit.text()
        if ip in ("", "..."):
            ip = "127.0.0.1"
        self.pc = Client(self, ip, host, port)

    def _quit(self):
        if self.pc is not None:
            self.pc.closeThread()
        self.close()
