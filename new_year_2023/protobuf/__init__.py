"""
May need to use nanopb
"""



# # Once we have the compiled Python module, we can use it to create
# # instances of our message and set the values of its fields:
#
# from example_pb2 import ExampleMessage
#
# msg = ExampleMessage()
# msg.value = 42
#
# # We can also serialize the message to a binary representation using
# # the `SerializeToString` method:
#
# data = msg.SerializeToString()
#
# # To deserialize the message, we can use the `ParseFromString` method:
#
# msg = ExampleMessage()
# msg.ParseFromString(data)
#
# # We can then access the fields of the deserialized message as usual:
#
# print(msg.value)  # prints 42
