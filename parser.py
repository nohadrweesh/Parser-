import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import Qt
from scanner import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Parse Tree")

x = 10
y = 100
far_x = 10
isDone = False


def draw_lines(painter,x1,y1,x2,y2):
    painter.drawLine(x1, y1, x2, y2)


def draw_blocks(painter, text,details, isCircle):
    if isCircle == False:
        painter.drawRect(QtCore.QRectF(x, y, 70, 30))
        painter.drawText(QtCore.QRectF(x, y, 70, 30),Qt.AlignCenter|Qt.AlignTop,text+'\n'+details)
    else:
        painter.drawEllipse(QtCore.QRectF(x, y, 50, 50))
        painter.drawText(QtCore.QRectF(x, y, 50, 50), Qt.AlignCenter|Qt.AlignTop, text+'\n'+details)


def tree_dfs(painter, prog_tree):


    global x, y, far_x

    text = prog_tree.cargo
    details =prog_tree.details
    x = prog_tree.x
    y = prog_tree.y

    #print(text+' x: '+str(x)+' y:'+str(y))
    if text != '':
        draw_blocks(painter, text,details, prog_tree.isCircle)
    else:

        prog_tree.y -=60
    if len(prog_tree.children) > 0 and prog_tree.right is not None:
        for idx, ch in enumerate(prog_tree.children):

            ch.y = prog_tree.y + 50 + 10

            if idx == 0:
                ch.x = prog_tree.x
                tree_dfs(painter, ch)
            else:
                # y=y
                far_x = far_x + 70 + 10
                ch.x = far_x
                tree_dfs(painter, ch)

            if prog_tree.isCircle == False and ch.isCircle == True:
                draw_lines(painter,prog_tree.x + 35, prog_tree.y + 30, ch.x + 25, ch.y)
            elif prog_tree.isCircle == True and ch.isCircle == True:
                draw_lines(painter,prog_tree.x + 25, prog_tree.y + 50, ch.x + 25, ch.y)
            else:
                draw_lines(painter,prog_tree.x + 35, prog_tree.y + 30, ch.x + 35, ch.y)
        far_x = far_x + 70 + 10
        prog_tree.right.y = prog_tree.y
        prog_tree.right.x = far_x


        tree_dfs(painter, prog_tree.right)
        draw_lines(painter,prog_tree.x + 70, prog_tree.y + 15, prog_tree.right.x , prog_tree.y + 15)


    elif len(prog_tree.children) > 0:

        for idx, ch in enumerate(prog_tree.children):

            ch.y = prog_tree.y+50+10

            if idx == 0:
                ch.x = prog_tree.x

                tree_dfs(painter, ch)
            else:
                #y=y
                far_x = far_x + 70 + 10
                ch.x = far_x

                tree_dfs(painter, ch)

            #draw lines
            if prog_tree.isCircle == False and ch.isCircle == True:
                draw_lines(painter,prog_tree.x + 35, prog_tree.y + 30, ch.x + 25, ch.y )
            elif prog_tree.isCircle == True and ch.isCircle == True:
                draw_lines(painter,prog_tree.x + 25, prog_tree.y + 50, ch.x + 25, ch.y)
                #print("hi")
            else:
                draw_lines(painter,prog_tree.x + 35, prog_tree.y + 30, ch.x + 35, ch.y)

    elif prog_tree.right is not None:
        # print(curr.right.cargo)
        far_x = far_x + 70 + 10
        prog_tree.right.x = far_x
        prog_tree.right.y=prog_tree.y
        draw_lines(painter,prog_tree.x+70, prog_tree.y+15, prog_tree.x+70+10, prog_tree.y+15)
        tree_dfs(painter, prog_tree.right)
    if prog_tree.isFinalNode:
        x=10
        y=100
        far_x=10
        return



class MyMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def paintEvent(self, event):


        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        mark_last_node(program_tree_final)
        tree_dfs(painter, program_tree_final)





class Tree:
    def __init__(self, cargo='',details='' ,right=None):
        self.cargo = cargo
        self.details = details
        self.children = []
        self.right = right
        self.x = 10
        self.y = 100
        self.isFinalNode = False  # To mark last node
        self.isCircle = True

    def add_data(self,cargo):
        self.cargo = cargo

    def add_details(self, details):
        self.details = details

    def add_child(self, child):
        self.children.append(child)

    def add_right(self,right):
        if self.right is None:
            self.right = right
        else:
            self.right.add_right(right)

    def __str__(self):
        return str(self.cargo)


def mark_last_node(tree_complete):
    if tree_complete.right is not None:
        mark_last_node(tree_complete.right)
    elif len(tree_complete.children)>0:
        mark_last_node(tree_complete.children[len(tree_complete.children)-1])
    else:
        tree_complete.isFinalNode = True


def print_list_indented(children_list, level):
    for child in children_list:
        print_tree_indented(child, level)


def print_tree_indented(tree, level=0):
    if tree is None:
        return

    if tree is str:
        print("error")
    else:
        print('  ' * level + str(tree.cargo))

    print_list_indented(tree.children, level + 1)
    print_tree_indented(tree.right, level )


def error_func():
    # error
    output_file.write("ERROR \n ")
    sys.exit()


def advance():
    global current_token, tokens_pointer
    if tokens_pointer < len(tokens)-1:
        # select next token
        tokens_pointer += 1
        current_token = tokens[tokens_pointer][0]


def match(token_type):
    if token_type==18:
        var='hi'
        print(var)
    global current_token, tokens_pointer
    if token_type == 'number':
        if current_token.isnumeric():
            advance()
            return
        else:
            error_func()
    elif token_type == 'identifier':
        if current_token.isalpha() and current_token not in reserved_words:
            advance()
            return
        else:
            error_func()
    elif current_token == token_type:
        # advance token
        advance()
    else:
        # error
        error_func()


def unmatch():
    global current_token, tokens_pointer
    if tokens_pointer > 0:
        tokens_pointer -= 1
        current_token = tokens[tokens_pointer][0]


def program():
    program_tree = stmt_sequence()
    output_file.write("Program Found\n")
    return program_tree


def stmt_sequence():
    stmt_seq_tree = statement()

    while current_token == ';':
        match(';')
        tree_right = statement()
        stmt_seq_tree.add_right(tree_right)
    output_file.write("Statement_Sequence Found\n")
    return stmt_seq_tree


def statement():
    tree = Tree()
    tree.isMainNode = True

    if current_token == 'if':
        tree = if_stmt()
    elif current_token == 'read':
        tree = read_stmt()
    elif current_token == 'repeat':
        tree = repeat_stmt()
    elif current_token == 'write':
        tree = write_stmt()
    else:
        tree = assign_stmt()
    output_file.write("Statement Found\n")
    tree.isCircle = False
    return tree


def factor():
    factor_tree=Tree()
    if current_token == '(':
        factor_tree_left = Tree(cargo='(')
        match('(')
        factor_tree.add_child(factor_tree_left)
        factor_tree_middle = exp()
        factor_tree.add_child(factor_tree_middle)
        factor_tree_right = Tree(cargo=')')
        match(')')
        factor_tree.add_child(factor_tree_right)

    else:
        if current_token.isnumeric():
            factor_tree.add_data('const')
            factor_tree.add_details('('+current_token+')')
            match('number')
        else:
            factor_tree.add_data('id ')
            factor_tree.add_details('(' + current_token + ')')
            match('identifier')

    output_file.write("Factor Found\n")
    return factor_tree


def term():
    isRecursive = False
    term_tree_ch0 = factor()

    new_term_tree = Tree()
    while current_token == '*' or current_token == '/':
        isRecursive = True
        new_term_tree.add_data('op')
        new_term_tree.add_details('('+current_token+')')
        new_term_tree.add_child(term_tree_ch0)
        output_file.write("Mul_Operator  Found\n")
        match(current_token)
        term_tree_ch1 = factor()
        new_term_tree.add_child(term_tree_ch1)
    output_file.write("Term Found\n")
    if isRecursive:
        return new_term_tree
    else:
        return term_tree_ch0


def simple_exp():
    isRecursive = False
    term_tree_ch0 = term()
    new_term_tree = Tree()
    while current_token == '+' or current_token == '-':
        isRecursive = True
        new_term_tree.add_data('op ')
        new_term_tree.add_details('('+current_token+')')
        new_term_tree.add_child(term_tree_ch0)
        output_file.write("Add_Operator Found\n")
        match(current_token)
        term_tree_ch1 = term()
        new_term_tree.add_child(term_tree_ch1)
    output_file.write("Simple_Expression Found\n")
    if isRecursive:
        return new_term_tree
    else:
        return term_tree_ch0


def exp():
    # exp_tree = Tree()
    exp_tree_ch0 = simple_exp()
    if current_token == '<' or current_token == '=':
        new_exp_tree = Tree()
        new_exp_tree.add_data('op')
        new_exp_tree.add_details('('+current_token+')')
        new_exp_tree.add_child(exp_tree_ch0)
        output_file.write("Comparator_Operator Found\n")
        match(current_token)
        exp_tree_ch1 = simple_exp()
        new_exp_tree.add_child(exp_tree_ch1)
        output_file.write("Expression Found\n")
        return new_exp_tree
    output_file.write("Expression Found\n")
    return exp_tree_ch0


def if_stmt():
    if_tree = Tree()
    if_tree.add_data('if')
    match('if')
    if_exp_tree = exp()
    if_tree.add_child(if_exp_tree)
    match('then')
    if_then_tree = stmt_sequence()
    if_tree.add_child(if_then_tree)
    if current_token == 'end':
        match('end')
    else:
        match('else')
        if_else_tree = stmt_sequence()
        if_tree.add_child(if_else_tree)
        match('end')
    output_file.write("IF_Statement Found\n")
    return if_tree


def read_stmt():
    match('read')
    token = current_token
    match('identifier')
    output_file.write("Read_Statement Found\n")
    return Tree(cargo='read', details='('+token+')')


def repeat_stmt():
    tree = Tree()
    tree_child_0 = Tree()
    tree_child_1 = Tree()
    match('repeat')
    tree.add_data('repeat')
    tree_child_0 = stmt_sequence()
    tree.add_child(tree_child_0)
    match('until')
    tree_child_1 = exp()
    tree.add_child(tree_child_1)
    output_file.write("Repeat_Statement Found\n")
    return tree


def write_stmt():
    wr_tree = Tree()
    match('write')
    wr_tree.add_data('write')
    ch_tree = exp()
    wr_tree.add_child(ch_tree)
    output_file.write("Write_Statement Found\n")
    return wr_tree


def assign_stmt():
    assign_tree = Tree()
    token=current_token
    match('identifier')
    match(':=')
    assign_tree.add_data('assign')
    assign_tree.add_details('('+token+')')
    ch_tree = exp()
    assign_tree.add_child(ch_tree)
    output_file.write("Assignment_Statement Found\n")
    return assign_tree

# just for starting -->write tokens instead of reading from the scanner
# tokens = [('read', 'reserved word'), ('x', 'identifier'), (';', 'special symbol'), ('if', 'reserved word'),
#           ('0', 'number'), ('<', 'special symbol'), ('x', 'identifier'), ('then', 'reserved word'),
#           ('fact', 'identifier'),
#           (':=', 'special symbol'), ('1', 'number'), (';', 'special symbol'), ('repeat', 'reserved word'),
#           ('fact', 'identifier'), (':=', 'special symbol'), ('fact', 'identifier'), ('*', 'special symbol'),
#           ('x', 'identifier'), (';', 'special symbol'), ('x', 'identifier'), (':=', 'special symbol'),
#           ('x', 'identifier'),
#           ('-', 'special symbol'), ('1', 'number'), ('until', 'reserved word'), ('x', 'identifier'),
#           ('=', 'special symbol'),
#           ('0', 'number'), (';', 'special symbol'), ('write', 'reserved word'), ('fact', 'identifier'),
#           ('end', 'reserved word')]
tokens = scanner_tokens
print(tokens)
tokens_pointer = 0
current_token = tokens[tokens_pointer][0]
outFile = 'parser_output.txt'


with open(outFile, 'w')as output_file:
    program_tree_final = program() # generate tree of the program


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainscreen = MyMainScreen()
        mainscreen.show()
        app.exec_()





