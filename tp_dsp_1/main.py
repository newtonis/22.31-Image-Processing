from scipy import signal
import matplotlib.pyplot as plt

import numpy


def generateSystem(e1, e2):
    return signal.dlti([1, e1], [1, -e1*e2], dt=1)


def addPlot(e1, e2):
    input = [0.125]

    for x in range(99):
        input.append(0)

    system = generateSystem(e1, e2)

    x_val_input = [x for x in range(len(input))]

    x_val_output, output = system.output(input, x_val_input)

    plt.plot(x_val_output, output, label = "Values = %d, %d" % (e1, e2))


def computeValues(e1, e2, x_input , input):
    system = generateSystem(e1, e2)

    x_val_output, output = system.output(input, x_input)

    return x_val_output, output


input = [0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x_input = [x for x in range(len(input))]

addPlot(0.9375, 0.9375)

x_val_output, output = computeValues(0.9375, 0.9375, x_input, input)

print(x_input, input)
print(x_val_output, output)


#addPlot(0, 0)
#addPlot(1, 0)
#addPlot(2, 0)
#addPlot(3, 0)
#addPlot(4, 0)

#addPlot(0.999, 0.999)


#addPlot(1, 1)

plt.legend()
plt.show()
