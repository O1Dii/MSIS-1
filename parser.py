import sys
import os.path
import re
from itertools import count
from math import log2

if len(sys.argv) == 4:
    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        file = open(sys.argv[1], "r")
        text = file.read()
        file.close()
        file = open(sys.argv[2], "r")
        operators = file.readlines()
        operands1 = dict()
        file.close()
        cort = ('"', "'", ')', ']', '{', '}', " else ", " method ", " sub ", " my ", " self ", " return ", "$")
        for i in range(len(cort)):
            if i < 2:
                for a in count():
                    x = text.find(cort[i])
                    y = text.find(cort[i], x + 1)
                    count1 = text.count(text[x:y])
                    if text[x:y] in operands1:
                        operands1[text[x:y]] += count1
                    else:
                        if text[x:y+1] != "":
                            operands1.setdefault(text[x:y+1], count1)
                    if x == -1 or y == -1:
                        break
                    text = text[:x - 1] + text[y + 1:]
            else:
                text = text.replace(cort[i], "")

        with open(sys.argv[3], "w") as output:
            bracket = text.find("(")
            print("\n-----OPERATORS:-----\n", file=output)

            text = re.compile(r"[#][^\n]*").sub("", text)
            text = re.compile(r"<.*>").sub("< >", text)
            sth = sorted(re.compile(r"(?:(?:(?:(?:(?:[\w+\.\[\]])*)[:.])+)|(?:[ ]))*[\w\-]*\(").findall(text))
            dic = {}
            for i in range(len(sth)):
                temp = re.compile(r"((.+(([\.:])|(::)))|(:))|[ ]").sub("", sth[i])[:-1]
                temp = temp.replace(" ", "")
                count = text.count(temp + '(')
                if temp in dic:
                    if count > dic.get(temp):
                        dic[temp] = count
                dic.setdefault(temp, count)
                text = text.replace(sth[i], "")

            for i in sorted(dic.keys()):
                print(str(i) + " - " + str(dic[i]), file=output)
            N1 = 0
            exceptions = {"(": ")", "[": "]", "??": "!!"}
            for i in range(len(operators)):
                operators[i] = operators[i].replace("\n", "")
                for index in exceptions:
                    if operators[i] == index:
                        if index == '(':
                            count = bracket
                        else:
                            count = text.count(operators[i])
                        print(str(operators[i]) + ' ' + str(exceptions.get(index)) + " - " + str(count),
                              file=output)
                        break
                else:
                    count = text.count(operators[i])
                    print(str(operators[i]) + " - " + str(count), file=output)
                N1 += count
                text = text.replace(operators[i], " ")

            n1 = len(operators)
            text = re.compile(r"[ ]{2,}").sub(" ", text)
            print("\n-----OPERANDS:-----\n", file=output)
            operands = sorted(set(text.split()), key=len, reverse=True)

            for i in operands1.keys():
                print(str(i) + ' - ' + str(operands1[i]), file=output)

            N2 = 0
            text = ' ' + text
            for i in range(len(operands)):
                operands[i] = ' ' + operands[i]
                count = text.count(operands[i])
                N2 += count
                print(operands[i] + " - " + str(count), file=output)
                text = text.replace(operands[i], ' ')

            n2 = len(operands)
            n = n1 + n2
            N = N1 + N2
            V = N * log2(n)
            print("""\nЧисло уникальных операторов = %d
Число уникальных операндов = %d
Общее число операторов = %d
Общее число операндов = %d
Словарь программы = %d
Длина программы = %d
Объём программы = %f""" % (n1, n2, N1, N2, n, N, V))

    else:
        print("\nPass on correct file paths")
else:
    print("\nYou need pass on 3 arguments:\n 1 - file with code\n 2 - file with operators\n 3 - output file")