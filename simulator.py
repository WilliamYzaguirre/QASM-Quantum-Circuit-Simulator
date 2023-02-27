import numpy as np
import time

def qasm_to_instruction(file_name):
    in_file = open(file_name)
    file_read = in_file.read()
    file_split = file_read.split(";\n")
    
    instruction_list = []
    for i in file_split:
        if i.split(" ")[0] != "":
            instruction_list += [[i.split(" ")[0], (i.split(" ")[1]).split(",")]]
    return instruction_list

def run_circ(instruction_list):
    start = time.time()
    q_reg = {}
    
    for instruction in instruction_list:
        
        if instruction[0] == 'qreg':
            size = int(instruction[1][0][2:-1])
            q_reg = {tuple(0 for i in range(size)): 1+0j}
            
        #elif instruction[0] == 'creg':
        #    c_reg = int(instruction[1][0][2:-1])
            
        elif instruction[0] == 'h':
            q_reg = h(q_reg, int(instruction[1][0][2:-1]))
            
        elif instruction[0] == 'x':
            q_reg = x(q_reg, int(instruction[1][0][2:-1]))
            
        elif instruction[0] == 't':
            q_reg = t(q_reg, int(instruction[1][0][2:-1]))
            
        elif instruction[0] == 'tdg':
            q_reg = tdg(q_reg, int(instruction[1][0][2:-1]))
            
        elif instruction[0] == 'cx':
            q_reg = cx(q_reg, int(instruction[1][0][2:-1]), int(instruction[1][1][2:-1]))
            
        else:
            continue
        
    return q_reg, (time.time() - start)*1000

def simulate(qasm_string):
    start = time.time()
    q_reg = {}
    
    instruction_list = qasm_string.splitlines()
    #print(instruction_list)
    for instruction in instruction_list:
        split_inst = instruction.split(" ")
        #print(split_inst[1])
        if split_inst[0] == 'qreg':
            size = int(split_inst[1][2:-2])
            q_reg = {tuple(0 for i in range(size)): 1+0j}
            
        #elif instruction[0] == 'creg':
        #    c_reg = int(instruction[1][0][2:-1])
            
        elif split_inst[0] == 'h':
            q_reg = h(q_reg, int(split_inst[1][2:-2]))
            
        elif split_inst[0] == 'x':
            q_reg = x(q_reg, int(split_inst[1][2:-2]))
            
        elif split_inst[0] == 't':
            q_reg = t(q_reg, int(split_inst[1][2:-2]))
            
        elif split_inst[0] == 'tdg':
            q_reg = tdg(q_reg, int(split_inst[1][2:-2]))
            
        elif split_inst[0] == 'cx':
            split_nums = split_inst[1].split(",")
            q_reg = cx(q_reg, int(split_nums[0][2:-1]), int(split_nums[1][2:-2]))
            
        else:
            continue
        
    return q_reg
    
def h(q_reg, num):
    #print("h on {}".format(num))
    new_q_reg = {}
    for state in q_reg:
        neg = 1
        if state[num] == 1:
            neg = -1
        h_state = {tuple( 0 if i == num else state[i] for i in range(len(state))): (1/np.sqrt(2))*q_reg[state],\
            tuple( 1 if i == num else state[i] for i in range(len(state))): (neg/np.sqrt(2))*q_reg[state]}
        #state1 = {tuple( 1 if i == num else state[i] for i in range(len(state))): (neg/np.sqrt(2))*q_reg[state]}
        
        simplify(h_state, new_q_reg)
        #simplify(state1, new_q_reg)
        
        #new_q_reg[state0] = (1/np.sqrt(2))*q_reg[state]
        #new_q_reg[state1] = (neg/np.sqrt(2))*q_reg[state]
    return new_q_reg
    
def x(q_reg, num):
    #print("x on {}".format(num))
    new_q_reg = {}
    for state in q_reg:
        x_state = {tuple( (state[i]+1)%2 if i == num else state[i] for i in range(len(state))): q_reg[state]}
        #if x_state in new_q_reg:
        #    if new_q_reg[x_state] + q_reg[state] == 0:
        #        del new_q_reg[x_state]
        #    else:
        #        new_q_reg[x_state] = q_reg[state]
        #else:
        #    new_q_reg[x_state] = q_reg[state]
        #new_q_reg[x_state] = q_reg[state]
        new_q_reg = simplify(x_state, new_q_reg)
    return new_q_reg
    
def t(q_reg, num):
    #print("t on {}".format(num))
    for state in q_reg:
        if state[num] == 1:
            q_reg[state] = q_reg[state]*np.exp(1.0j*(np.pi/4))
    return q_reg
    
def tdg(q_reg, num):
    #print("tdg on {}".format(num))
    for state in q_reg:
        if state[num] == 1:
            q_reg[state] = q_reg[state]*np.exp((-1)*1.0j*(np.pi/4))
    return q_reg
    
def cx(q_reg, control_num, target_num):
    #print("cx on {}, {}".format(control_num, target_num))
    new_q_reg = {}
    for state in q_reg:
        if state[control_num] == 1:
            cx_state = {tuple( (state[i]+1)%2 if i == target_num else state[i] for i in range(len(state))): q_reg[state]}
            new_q_reg = simplify(cx_state, new_q_reg)
        else:
            cx_state = {tuple(state[i] for i in range(len(state))): q_reg[state]}
            new_q_reg = simplify(cx_state, new_q_reg)

    return new_q_reg

def simplify(state, q_reg):
    for key in state:
        if key in q_reg:
            if round(q_reg[key].real + state[key].real, 4) == 0 and round(q_reg[key].imag + state[key].imag, 4) == 0:
                del q_reg[key]
            else:
                q_reg[key] = state[key] + q_reg[key]
        else:
            q_reg[key] = state[key]
    return q_reg
    

if __name__ == "__main__":
    files = ["miller_11.qasm", "decod24-v2_43.qasm", "one-two-three-v3_101.qasm", "hwb5_53.qasm", "alu-bdd_288.qasm", \
        "f2_232.qasm", "con1_216.qasm", "mini_alu_305.qasm", "wim_266.qasm", "cm152a_212.qasm", "squar5_261.qasm", \
        "sym6_316.qasm", "rd84_142.qasm", "cnt3-5_179.qasm"]
    outputs = []
    times = []
    for filename in files:
        output, duration = run_circ(qasm_to_instruction(filename))
        outputs.append(output)
        times.append(duration)
        print("The output of {} is: {}\nAnd took {} ms".format(filename, output, duration))
        