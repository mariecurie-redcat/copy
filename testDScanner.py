from scanner import Scanner


with open("bash.txt", "r") as f:
    content = f.read()

scanner = Scanner(content)
tokens = scanner.scanTokens()

for token in tokens:
    print(repr(token))