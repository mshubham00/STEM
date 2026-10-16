#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

selected_function= sys.argv[1]
# Define the mathematical function
plt.figure(figsize=(8, 8))

def plot(): # plot argument1
    function_str = sys.argv[2]
    graph_title= sys.argv[3]
    x = np.linspace(-10, 10, 400)  # Creating 400 points between -10 and 10
    label =f'f(x)={function_str}'
    y = eval(function_str)
    return x, y, graph_title, label

def multiplot(a2, a3, a4, a5): # multiplot argument1
    x = np.linspace(-10, 10, 400)
    n = eval(a2) # num_equation argument2
    eq_1 = eval(a3) # first_equation argument3
    label =f'f(x)={eq_1}'
    if n == 3:
        eq_2 = eval(a4) #second_equation argument4
        eq_3 = eval(a5) #third_equation argument5
        label2 =f'f(x)={eq_2}'
        label3 =f'f(x)={eq_3}'
        plt.plot(x, eq_2, color='r', label=r'%s'%(label2))
        plt.plot(x, eq_3, color='k', label=r'%s'%(label3))
    elif n==4:
        eq_2 = sys.argv[4] #second_equation argument4
        y = sys.argv[5] #third_equation argument5
        z = sys.argv[6]
        label2 =f'f(x)={function_str}'
        plt.plot(x, z, color='r', label=r'%s'%(label1))
        label3 =f'f(x)={function_str}'
        plt.plot(x, w, color='r', label=r'%s'%(label2))
    elif n==5:
        w = sys.argv[4]
        y = sys.argv[5]
        z = sys.argv[6]
        a = sys.argv[7]
        label1 =f'f(x)={function_str}'
        plt.plot(x, z, color='r', label=r'%s'%(label1))
        label2 =f'f(x)={function_str}'
        plt.plot(x, w, color='r', label=r'%s'%(label2))
        label3 =f'f(x)={function_str}'
        plt.plot(x, a, color='r', label=r'%s'%(label3))
    else:
        print('Invalid choice, fuck you dumb!')
    return x, y, graph_title, label

def sigmoid(): # 2
    x = np.linspace(-10, 10, 400)  # Creating 400 points between -10 and 10
    graph_title = 'Sigmoid Function'
    label = '$f(x) = \frac{1}{1 + e^{-x}}$'
    return x, 1 / (1 + np.exp(-x)), graph_title, label

def circle():
    theta = np.linspace(0, 2*np.pi, 100)  # 100 points for a smooth circle
    print('Enter Radius')
    r = float(input())
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    graph_title = 'Circle'
    label = '$r^2=x^2 + y^2$'
    return x, y, graph_title, label

def sin():
    theta = np.linspace(0, 2*np.pi, 100)  # 100 points for a smooth circle
    g = 'Sine Function'
    l = '$f(x) = \\sin (x)$'
    return theta, np.sin(theta), g,l

def gelu():
    x = np.linspace(-3, 3, 400)  # Creating 400 points between -10 and 10
    graph_title = 'GELU Activation Function'
    label = '$f(x) = 0.5 x( 1 + tanh [\\sqrt{2/ \\pi}(x+0.044715x^3)]$'
    y = 0.5*x*(1 + np.tanh(np.sqrt(2/np.pi)*(x + 0.044715*x**3)))
    return x, y, graph_title, label

def constant():
    x = 0
    print('Give argument:')

function_dict = {
    '0': constant,
    'plot': plot,
    'multiplot': multiplot,
    '1': sigmoid,
    '2': circle,
    '3': sin,
    '4': gelu
}

#selected_function = input("Enter function (1: Sigmoid, 2: Circle, 3:Sine):")

if selected_function in function_dict:
    # Call the selected function with user input numbers as arguments
    x,y,t,l = function_dict[selected_function]()
else:
    print("Invalid function. Please enter a valid function name.")

if eval(sys.argv[1])!=0:
    # Create the plot
    plt.plot(x, y, color='b', label=r'%s'%(l))
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.show()
