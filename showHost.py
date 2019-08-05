# title: Show Host
# aurthur: Callum B-C

import session


class Hand(session.Node):
	def __init__(self, conn, host=None):
		super().__init__(conn, host)

	def end(self, exception=False):  # todo review
		self.session.end()


class Show(session.Session):
	def __init__(self, manager, name):
		super().__init__(manager, name)
		self.prop_list = []
		self.prop_status = {}


class ShowHost(session.SessionManager):
	def __init__(self, show=Show, hand=Hand, port=8089):
		super().__init__(port)
		self.session_hook = Show
		self.node_hook = Hand
		self.unassigned = []

	def loop(self):
		super().loop()
		# get new node and announce to sessions
