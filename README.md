Number of qubits vs Execution time above
I parameterized the solution by making the initialization of the quantum register dynamic. Meaning, I represent the quantum register as a dictionary with all of the possible states of the quantum system as keys, with their amplitudes as the values. The keys are dynamically shaped tuples (tuples are slightly faster than lists and are hashable, so they can be used as keys in a dict), meaning that the number of qubits is easy to manipulate upon initialization.
If you run my program file as is, if you have all of the .qasm files in the same directory, you will get the output of running the circuits with how long it took to run. You will also see many commented out lines in the __name__ == __"main"__ block. These were all of my testing lines. Feel free to uncomment and try specific combinations of gates and states to see what you get. The description of how to run is below.
HOW TO RUN:
You can run my file from the command line with “python3 cs238.py”, and this will print the output from each file and how long it took (if all of the .qasm files are in the same directory as the program”
You can also import my file into the provided jupyter lab testing file, and run the function simulate on the qasm string.
Note: the code for the diagram is not provided, as this was done in a separate jupyter lab file that I used to make sure the simulate function was working in the provided test file.

