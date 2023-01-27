
from package_experiments.moo import a, b


b_class = b.B()

b_class.gen()

a.A.bark = lambda self: print("meow")

b_class.moo.bark()
