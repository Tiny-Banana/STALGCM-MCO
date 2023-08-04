# STALGCM-MCO

# Input Machine


The first line reads a pair (N, T) of integers, indicating the number of states and the number of transitions that make up the PDA respectively.

Subsequently, we input T lines representing the transitions of the PDA, in the form **Q O A E D** indicating a transition from state **Q** to state **O** by reading **A** in the input string, popping **E** from the stack, and pushing **D**, all separated by a space.

**S** was then read which is the start state, and **C** as the accepting states.

Finally, a string will be received to be evaluated by the PDA.