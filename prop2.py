import audio_graph
import prop1


# if __name__ == "__main__":
#     prop = prop1.Prop()
#     screen = prop1.Screen(prop)
#     prop.start()
#     screen.run()

if __name__ == "__main__":
    graph = audio_graph.Graph()
    screen = audio_graph.Screen(graph)
    graph.screen = screen
    graph.start()
    screen.run()