import tkinter as tk
from tkinter import StringVar

class GUI:

    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("500x500")
        self.root.title("DPDA")

        self.label1 = tk.Label(self.root, text="Enter string: ", font=("Arial, 14"))
        self.label1.grid(row=0, column=0, padx=30, pady=10)

        self.string = StringVar()

        self.textbox = tk.Entry(self.root, textvariable=self.string, font=("Arial, 14"))
        self.textbox.grid(row=0, column=1)

        self.button = tk.Button(self.root, text="Test", font=("Arial, 14"), command=self.main)
        self.button.grid(row=0, column=2, padx=20)

        self.testResult = tk.Label(self.root, font=("Arial, 14"))
        self.testResult.grid(row=3, column=0, columnspan=3)

        self.root.mainloop()


    def main(self):
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

        self.stateRoot = tk.Label(self.root, font=('Arial, 14'))
        self.stateRoot.grid(row=1, column=0)
      
        self.inpStrRoot = tk.Label(self.root, font=('Arial, 14'))
        self.inpStrRoot.grid(row=1, column=1)

        self.stackRoot = tk.Label(self.root, font=('Arial, 14'))
        self.stackRoot.grid(row=2, column=0, columnspan=3)

        self.isClick = False
        self.next = tk.Button(self.root, text="Next", font=("Arial, 14"), command=self._click)
        self.next.grid(row=4, column=0, columnspan=3, pady=30)
    
    def _click(self):
        self.isClick = True

    def _isDefinedTransition(self, state, c, stackTop):
        for transition in state:
            if c == transition['READ'] and (stackTop == transition['POP'] or transition['POP'] == '~'):
                return True, transition
        return False, None
    
    def test(self, string):
        initialState = self.start
        currState = initialState
        stackTop = self.stack.peek()

        if len(string) == 0:
            return False
        
        for i in range(len(string)):
            self.stackRoot.config(text="Stack: " + self.stack.getReverse())
            result, transition = self._isDefinedTransition(self.states[currState], string[i], stackTop)
            if result:
                currState = transition['TO']
                self.stateRoot.config(text="State " + str(currState))
                self.inpStrRoot.config(text=string[i:])
                if transition["POP"] != '~' and transition["POP"] == stackTop:
                    self.stack.pop()
                if transition["PUSH"] != '~':
                    self.stack.push(transition["PUSH"])
                stackTop = self.stack.peek()
                if i == len(string) - 1 and self.stack.isEmpty() and currState in self.accept:
                    return True
            else:
                return False

            self.isClick = False
            while not self.isClick:
                self.root.update()  # Process events to update the GUI
            
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