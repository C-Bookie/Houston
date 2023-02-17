from bokeh.plotting import figure, show

def display_bowling_result(throws):
    # Create a list of rounds
    rounds = list(range(1, len(throws)//2 + 1))

    # Calculate the scores for each round
    scores = []
    score = 0
    spare = False
    for i, throw in enumerate(throws):
        if throw == '/':
            score = 10 - score
            spare = True
        else:
            score += int(throw)
        if (i + 1) % 2 == 0:
            scores.append(score)
            if spare:
                score += int(throw)
                spare = False
            else:
                score = 0

    # Create a figure and plot the scores as a line graph
    p = figure(title='Bowling Result', plot_height=400, plot_width=600,
               toolbar_location=None, tools='')
    p.line(x=rounds, y=scores, line_width=2)

    # Add labels to the graph
    p.xaxis.axis_label = 'Round'
    p.yaxis.axis_label = 'Score'

    show(p)
