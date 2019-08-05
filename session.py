import threading
import queue

import connection

DEBUG = True


def debug_print(msg):
    if DEBUG:
        print(str(threading.current_thread().getName()) + ": " + str(msg))


class Node(connection.SocketHook):
    class IllegalResponse(Exception):
        def __init__(self, message, response):
            super().__init__(message + "\n" + str(response))

    def __init__(self, conn, session, alias=None, host=None):
        super().__init__(conn, host)
        self.closeAll = threading.Event()
        self.closeAll.clear()
        self.alias = alias
        if self.alias is None:
            self.alias = self.addr + ":" + str(self.port)
        self.setName("Node-" + self.alias)

        self.white_list_functions = [
            "trip",
            "rename_node",
            "move_session",
            "get_session",
            "broadcast",
            "close",
            "stop"
        ]

        self.session: Session = session
        self.session.add_node(self)

    def send(self, data):
        self.send_msg(connection.encode(data))

    def callback(self, data):
        response = connection.decode(data)
        debug_print(str(response))

        if response["type"] in self.white_list_functions:
            function = getattr(self, response["type"])
            function(*response["args"])
        else:
            raise self.IllegalResponse("Request unrecognised by server: " + response["type"], response)

    # ---SERVER COMMANDS---
    # all functions must be added to self.white_list_functions

    def trip(self, msg):
        self.session.end(True)
        raise Exception("Node tripped up: " + msg)

    def rename_node(self, msg):
        self.alias = msg  # todo change to response["content"]["alias"]
        self.setName("Node-" + self.alias)

    def move_session(self, session_alias):
        self.session.manager.move_session(self, session_alias)  # todo get player ID

    def get_sessions(self):
        self.send({
            "type": "session_list",
            "content": {
                "sessions": self.session.manager.get_sessions()
            }
        })

    def broadcast(self, response):
        self.session.broadcast(response)

    def close(self):
        debug_print("closing")
        self.closeAll.set()
        self.session.end()
        super().close()

    def stop(self):
        self.session.end()


class Session(threading.Thread):
    def __init__(self, manager, alias):
        super().__init__()
        self.manager = manager
        self.setName("Session-" + alias)
        self.alias = alias
        self.nodes = []
        self.response = queue.Queue()

    def broadcast(self, data):
        for node in self.nodes:
            node.send(data)

    def add_node(self, node: Node):
        self.nodes += [node]
        node.session = self
        debug_print("Added node: " + node.alias + " -> " + self.alias)

    def remove_node(self, node: Node):
        for i in range(len(self.nodes) - 1, -1, -1):
            if self.nodes[i] is node:
                del self.nodes[i]
                debug_print("Removed node: " + node.alias + " <- " + self.alias)

    # def close(s, node: Node=None):
    # 	s.manager.close(node)

    def end(self, exception=False):
        pass


class SessionManager(connection.Host):
    def __init__(self, port=8089):
        super().__init__(port)
        self.node_hook = Node
        self.session_hook = Session
        self.sessions = {}

    def loop(self):
        conn, address = self.sock.accept()
        alias = address[0] + ":" + str(address[1])
        session = self.create_session(alias)
        node = self.node_hook(conn, session, host=self)  # todo remove requirement for host
        node.start()

    def move_session(self, node: Node, session_alias):
        session_alias = str(session_alias)
        debug_print("Moving node: " + node.alias + " -> " + session_alias)
        self.leave_session(node)
        self.join_session(node, session_alias)

    def join_session(self, node: Node, session_alias):
        session_alias = str(session_alias)
        if session_alias not in self.sessions:
            self.create_session(session_alias)
        self.sessions[session_alias].add_node(node)

    def create_session(self, session_alias):
        assert session_alias not in self.sessions
        self.sessions[session_alias] = self.session_hook(self, session_alias)
        self.sessions[session_alias].start()
        debug_print("Created new session: " + session_alias)
        return self.sessions[session_alias]

    def leave_session(self, node: Node):
        node.session.remove_node(node)
        if len(node.session.nodes) == 0:
            self.delete_session(node.session.alias)
        node.session = None

    def delete_session(self, session_alias):
        assert session_alias in self.sessions
        del self.sessions[session_alias]  # todo review
        debug_print("Deleted old session: " + session_alias)

    def get_sessions(self):
        return self.sessions.keys()
