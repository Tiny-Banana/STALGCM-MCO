import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from tkinter import filedialog

class GUI:

    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("500x300")
        self.root.title("DPDA")

        self.label1 = tk.Label(self.root, text="Enter string: ", font=("Arial, 14"))
        self.label1.grid(row=1, column=0, padx=30, pady=10)

        self.string = StringVar()

        self.textbox = tk.Entry(self.root, textvariable=self.string, font=("Arial, 14"))
        self.textbox.grid(row=1, column=1)

        self.button = tk.Button(self.root, text="Run", font=("Arial, 14"), command=self.main)
        self.button.grid(row=1, column=2, padx=20)

        self.testResult = tk.Label(self.root, font=("Arial, 14"))
        self.testResult.grid(row=5, column=0, columnspan=3)

        self.root.mainloop()

    def main(self):
        self.testResult.config(text= "")
        with open("input2.txt", "r") as file:
            N, T = map(int, file.readline().strip().split())

            states = [ [] for _ in range(N) ]

            for i in range(T):
                #FROM state Q to O, reading A, popping E and pushing D
                Q, O, A, E, D = file.readline().strip().split()
                Q, O = map(int, (Q, O))
                transition = {"FROM":Q, "TO":O, "READ":A, "POP":E, "PUSH":D}
                states[Q].append(transition)

            S = int(file.readline())
            A_str = file.readline().strip().split()
            A = [int(num) for num in A_str]

        string = self.string.get() + '~'

        dpda = DPDA(states, S, A, self.root)
        result = dpda.test(string)

        if (result):
            self.testResult.config(text= "Accepted", fg="green")
        else:
            self.testResult.config(text= "Rejected", fg="red")
        
class DPDA:

    def __init__(self, states, start, accept, root):
        self.states = states 
        self.stack = Stack()
        self.start = start
        self.accept = accept
        self.root = root
        
        self.canvas = tk.Canvas(self.root, width=420, height=100)
        self.canvas.grid(row=2, column=0, columnspan=5)
        self.canvas.create_line(0, 0, 550, 0, fill="black", width=10)

        self.stateRoot = self.canvas.create_text(1, 30, text="Current State: q", fill="black", font=("Arial", 14), anchor="w")
        self.inpStrRoot = self.canvas.create_text(1, 55, text="Input String:", fill="black", font=("Arial", 14), anchor="w")
        self.stackRoot = self.canvas.create_text(1, 80, text="Stack:", fill="black", font=("Arial", 14), anchor="w")

        self.isClick = False
        self.next = tk.Button(self.root, text="Next", font=("Arial, 14"), command=self._click)
        self.next.grid(row=6, column=0, columnspan=3, pady=30)
    
    def _click(self):
        self.isClick = True

    def _isDefinedTransition(self, state, c, stackTop):
        for transition in state:
            if c == transition['READ'] and (stackTop == transition['POP'] or transition['POP'] == '~'):
                return True, transition
        return False, None
    
    def _bold(self, x, char):
        self.canvas.create_text(x, 55, text=char, fill="black", font=("Arial", 14, "bold"), anchor="w")

    def test(self, string):
        initialState = self.start
        currState = initialState
        stackTop = self.stack.peek()

        if len(string) == 0:
            return False
        
        self.canvas.itemconfig(self.inpStrRoot, text="Input String: " + string[:-1])
        x = 106.5
        for i in range(len(string)):
            self.canvas.itemconfig(self.stateRoot, text="Current State: q" + str(currState))
            self.canvas.itemconfig(self.stackRoot, text="Stack: " + self.stack.getReverse())
            result, transition = self._isDefinedTransition(self.states[currState], string[i], stackTop)
            if result:
                if transition["POP"] != '~' and transition["POP"] == stackTop:
                    self.stack.pop()
                if transition["PUSH"] != '~':
                    self.stack.push(transition["PUSH"])
                stackTop = self.stack.peek()
                currState = transition['TO']
                
                if i == len(string) - 1 and self.stack.isEmpty() and currState in self.accept:
                    self.canvas.itemconfig(self.stackRoot, text="Stack:")
                    return True
            else:
                return False
                
            self.isClick = False
            while not self.isClick:
                self.root.update() 

            self._bold(x, string[i])
            x += 10.3
            
        return False
    
class Stack:

    def __init__(self):
        self.data = ['Z']

    def isEmpty(self):
        return len(self.data) == 0

    def pop(self):
        if not self.isEmpty():
            elem = self.data[0]
            del self.data[0]
            return elem
        else:
            return None
    
    def push(self, elem):
        for char in elem:
            if (char != "~"):
                  self.data.insert(0, char)

    def peek(self):
        if not self.isEmpty():
            return self.data[0]
        return -1
    
    def getReverse(self):
        reverse = self.data[:]
        reverse.reverse()
        return ''.join(reverse)

    def __str__(self):
        return str(self.data)
    
if __name__ == '__main__':
    GUI()