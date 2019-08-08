import prop


if __name__ == "__main__":
    prop1 = prop.Prop()
    screen = prop.Screen(prop1)
    prop1.start()
    screen.run()
