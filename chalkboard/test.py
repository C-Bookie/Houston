class A1:
    foo = 1


class A2(A1):
    foo = 2


class B1(A1):
    foo = 3


class B2(B1, A2):
    def bar(self):
        return super().foo

instance = B2()
print(instance.bar())  # Output: 2
