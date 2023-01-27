
from package_experiments.moo.a import A


class B(A):
    moo: A

    def gen(self):
        self.moo = A()
