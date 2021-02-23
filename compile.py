import sys, os

class Compiler:
    def __init__(self, text: str, nowrite: bool = False):
        self.text = text
        self.nowrite = nowrite

        self.prefix = '~'

        self.functions = {
                'sys': 'syscall'
        }

        self.registers = {
                '0': 'rax',
                '1': 'rdi',
                '2': 'rsi',
                '3': 'rdx',
                '4': 'r10',
                '5': 'r8',
                '6': 'r9'
        }


        self.operation_data = []

        self.new_code = ''
        self.parsed_instructions = ''

    def get_function(self):
        try:
            if self.new_code == '': self.operation_data = [[[x, [z for z in range(x+4, len(self.text)) if self.text[z] == ')'][0]], self.functions.get(self.text[x+1:x+4], -1), self.text[x+5:[z for z in range(x+4, len(self.text)) if self.text[z] == ')'][0]].split(',')] for x, i in enumerate(self.text) if i == self.prefix][0]
            else: self.operation_data = [[[x, [z for z in range(x+4, len(self.new_code)) if self.new_code[z] == ')'][0]], self.functions.get(self.new_code[x+1:x+4], -1), self.new_code[x+5:[z for z in range(x+4, len(self.new_code)) if self.new_code[z] == ')'][0]].split(',')] for x, i in enumerate(self.new_code) if i == self.prefix][0]

        except IndexError as e:
            self.operation_data = []
            return IndexError, e

    def replace_text(self, start_point: int, end_point: int, text: str):
        if self.new_code == '': self.new_code = self.text[:start_point] + text + self.text[end_point+1:]
        else: self.new_code = self.new_code[:start_point] + text + self.new_code[end_point+1:]

    def parse_instrucions(self):
        intstructions = [f'mov {self.registers.get(str(x))}, {i}' for x, i in enumerate(self.operation_data[2])]
        intstructions.append(self.operation_data[1])

        self.parsed_instructions = '\n'.join(intstructions)

    def compiler(self):

        while True:
            self.get_function()
            data = self.operation_data

            if data == []: break

            self.parse_instrucions()
            self.replace_text(data[0][0],data[0][1], self.parsed_instructions)

        if not self.nowrite:
            with open('assembly.asm', 'w') as f:
                f.write(self.new_code)


            os.system('nasm -f elf64 -o obj.o assembly.asm && ld obj.o -o main && rm assembly.asm obj.o')

        else:
            print(self.new_code)


def main():
    arguments = sys.argv[1:]
    file = sys.argv[1]

    with open(file) as f:
        file_contents = f.read()


    handler = Compiler(file_contents, 'nowrite' in arguments)
    handler.compiler()

if __name__ == '__main__':
    main()
