import threading
import queue

import connection

DEBUG = True


def debug_print(msg):
    if DEBUG:
        print(str(threading.current_thread().getName()) + ": " + str(msg))


class Node(connection.SocketHook):
    class IllegalResponse(Exception):  # fixme replace with connection.IllegalResponse
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

        self.session: Session = session
        self.session.add_node(self)

        self.white_list_functions += [
            "trip",
            "register",
            "rename_node",  # todo rename to set_node_alias
            "move_session",
            "get_sessions",
            "broadcast",
            "close",
            "stop"
        ]

    # def callback(self, data):
    #     response = connection.decode(data)
    #     debug_print(str(response))
    #
    #     if response["type"] in self.white_list_functions:
    #         function = getattr(self, response["type"])
    #         function(*response["args"])
    #     else:
    #         raise self.IllegalResponse("Request unrecognised by server: " + response["type"], response)

    # ---SERVER COMMANDS---
    # all functions must be added to self.white_list_functions

    def trip(self, msg):
        self.session.end(True)
        raise Exception("Node tripped up: " + msg)

    def register(self, node_alias, session_alias):
        self.rename_node(node_alias)
        self.move_session(session_alias)

    def rename_node(self, msg):
        debug_print("Renamed node: " + self.alias + " => " + msg)  # todo add lobby alias to message
        self.alias = msg  # todo change to response["content"]["alias"]
        self.setName("Node-" + self.alias)

    def move_session(self, session_alias):
        self.session.manager.move_session(self, session_alias)  # todo get player ID

    def get_sessions(self):  # todo review
        self.send_data({
            "type": "session_list",
            "contents": list(self.session.manager.sessions.keys())
        })

    def get_nodes(self):  # todo review
        return self.session.get_nodes()

    def broadcast(self, response, node_alias=None):
        self.session.broadcast(response, node_alias)

    def close(self):
        debug_print("closing")
        self.closeAll.set()
        self.session.end()
        super().close()

    def stop(self):
        self.session.end()


class Session():  # todo review the idea of a multilayered room structure
    def __init__(self, manager, alias):
        super().__init__()
        self.manager = manager
        self.name = "Session-" + alias
        self.alias = alias
        self.nodes = []
        self.response = queue.Queue()

    def broadcast(self, data, node_alias=None):
        for node in self.nodes:
            if node_alias is None or node.alias == node_alias:
                node.send_data(data)

    def add_node(self, node: Node):
        self.nodes += [node]
        node.session = self
        debug_print("Added node: " + node.alias + " -> " + self.alias)

    def remove_node(self, node: Node):
        for i in range(len(self.nodes) - 1, -1, -1):
            if self.nodes[i] is node:
                del self.nodes[i]
                debug_print("Removed node: " + node.alias + " <- " + self.alias)

    def get_nodes(self):
        return [node.alias for node in self.nodes]

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
        node = self.node_hook(conn, session, alias, self)  # todo remove requirement for host
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
        # self.sessions[session_alias].start()
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


if __name__ == "__main__":
    manager = SessionManager()
    manager.run()
