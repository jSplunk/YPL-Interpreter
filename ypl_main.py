#YPL Interpreter Command Line

#External libraries
import sys, os

#Dictonary, where all lines that can be interpreted is stored
DIC = {
    "meu nome é" : "DOC_NAME", # example "meu nome è teste"
    "me dê" : "LIST_DECL" , # example "me dê 4 maçãs"
    "monstre-me" : "PRINT", # example "monstre-me maçãs"
    "colocar" : "VAR_DECL", # example "colocar 4 no mundo"
    "é o" : "IF" #example "é o mundo igual a plus"
}

#All variables (lists) that the .ypl file defines
LIST_DICT = {}
VAR_DICT = {}

NUMBER_OF_LINES = 0

LINES = []

def process_action(command, arg):
    func = ACTION[command]
    args = arg.split()
    var = func(*args)
    
def print_doc_name(name):
    print(name+'\n')

def add_variable_list(amount, name):
    if(not int(amount)):
        print("Você precisa especificar o valor antes do nome!")
        exit(-1)
    LIST_DICT[name] = int(amount)

def add_var(amount, dontuse, name):
    if amount in LIST_DICT:
        if(dontuse == "no"):
            x = LIST_DICT[amount]
            LIST_DICT[name] = x
            return
    elif amount in VAR_DICT:
        if(dontuse == "no"):
            x = VAR_DICT[amount]
            VAR_DICT[name] = x
            return
    if(not int(amount) or dontuse != "no"):
        print("Você precisa especificar o valor antes do nome!")
        exit(-1)
    VAR_DICT[name] = int(amount)

def if_statement():
    return

def get_variable(name):
    return VAR_DICT[name]

def print_arg(name):
    if name in LIST_DICT:
        var = LIST_DICT[name]
        for i in range(var):
            print(name)
        return
    print(get_variable(name))

def read_file(filename):
    global LINES
    with open(filename, encoding="utf-8") as fp:
        LINES = fp.readlines()
        NUMBER_OF_LINES = len(LINES)



#All the available actions tied to the interpreted line of code
ACTION = {
    "DOC_NAME" : print_doc_name,
    "LIST_DECL" : add_variable_list,
    "PRINT" : print_arg,
    "VAR_DECL" : add_var,
    "IF" : if_statement
}


def end_of_file():
    print("*-------------------------------*")
    print("Arquivo tem {} linhas de código!".format(NUMBER_OF_LINES))
    print("*-------------------------------*")

if(len(sys.argv) < 2):
    print("Nenhum arquivo fornecido para intérprete!")
    exit(-1)

if(not sys.argv[1].endswith(".ypl")):
    print("Nenhum arquivo .ypl fornecido para intérprete!")
    exit(-1)

filename = sys.argv[1]

read_file(filename)

if(not len(LINES)):
    print("Não consegue ler o conteúdo, talvez o arquivo esteja vazio?")
    exit(-1)

### MAIN LOOP ###

count_for_keys = 0
count_for_lines = 0

for line in LINES:
    for key in DIC:
        pos = line.find(key)
        if(pos == -1):
            count_for_keys += 1
            continue
        pos += len(key)+1
        try:
            process_action(DIC[key], line[pos:])
            break
        except:
            print("Erro sintático na linha {}".format(count_for_lines))
            exit(-1)
            
    if(count_for_keys == len(DIC)):
        print("Comando não encontrado!")
        print("Verificar linha número: {}".format(count_for_lines))
        exit(-1)
        
    count_for_keys = 0
    count_for_lines += 1

NUMBER_OF_LINES = count_for_lines

end_of_file()
