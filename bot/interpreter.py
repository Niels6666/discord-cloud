import discord.embeds
from typing import Dict, List
import requests
from draw import Graphics
from parser import Expression, Parser

g2d = Graphics()
"""
interpreter.py static graphics
"""


class ImageFormat:
    format = ""

    def __init__(self, string: str) -> None:
        f = string.lower()
        if(f == "svg" or f == "gif" or f == "png" or f == "pdf"):
            self.format = f
        else:
            raise Exception("Le format " + string + " n'est pas accepté.")

    def __str__(self) -> str:
        return self.format


class Response:
    content = None
    files = []

    def __init__(self, content) -> None:
        self.content = content
        self.files = []

    def addFile(self, path: str):
        # curr_dir = os.getcwd()
        # self.files.append(curr_dir + "\\" + path)
        self.files.append(path)

    def __str__(self) -> str:
        res = ""
        if(isinstance(self.content, Exception)):
            res = "diff\nErreur dans la commande :\n-"
        return res + str(self.content)
    

    def build(self):
        rich = discord.embeds.Embed()
        rich.type = "rich"
        rich.title = "bot's response"
        rich.color = discord.Color.dark_orange()
        rich.description = self.__str__()
        return rich

    

class Command:
    name = ""
    arguments = {}
    description = ""
    resp = None

    def __init__(self, name: str, arguments: Dict[str, type], description: str, resp) -> None:
        self.name = name
        self.arguments = arguments
        self.description = description
        self.resp = resp

    def check(self, args: List[str]):
        nargs = self.arguments.__len__()
        if(nargs < args.__len__()):
            return Exception("La commande '" + self.name + "' prend " + str(nargs) +
                             " argument(s) mais il y en a " + str(args.__len__() - nargs) + " de trop.")
        if(nargs > args.__len__()):
            return Exception("Il manque " + str(nargs - args.__len__()) + " argument(s) pour la commande " + self.name + ".")
        return None

    def getArgs(self, args: List[str]):
        res: List[object] = []
        i = 0
        types = list(self.arguments.items().mapping.values())
        try:
            types = list(self.arguments.items().mapping.values())
            for i in range(args.__len__()):
                t = types.__getitem__(i)
                a = args[i]
                if t == str:
                    if a == "":
                        raise Exception("la phrase est vide")
                    res.append(str(a))
                elif t == float:
                    try:
                        res.append(float(a))
                    except Exception:
                        raise Exception("l'argument n'est pas un nombre")
                elif t == int:
                    try:
                        res.append(int(a))
                    except Exception:
                        raise Exception("l'argument n'est pas un nombre")
                elif t == Expression:
                    res.append(Parser().parseString(a))
                elif t == ImageFormat:
                    res.append(ImageFormat(a))
            return res
        except Exception as e:
            wrong = list(self.arguments.items().mapping.keys()).__getitem__(i)
            return Exception("Argument invalide (" + wrong + "): " + str(e))

    def response(self, args: List[object]):
        return self.resp(args)

    def __str__(self) -> str:
        return self.description


commands: Dict[str, Command] = {}

###################################################################################################################
###############################################****COMMANDS****####################################################
###################################################################################################################

def help(args):
    response = "Voici une liste de toutes les commandes et leur description:\n"
    for c in commands.keys():
        comm = commands.get(c)
        sargs = ""
        for s in comm.arguments:
            sargs += " <" + s + ">"

        response += ("\t" + c + sargs + " : " + str(comm))
        response += "\n"

    return Response(response)

HELP = Command('help',
               {},
               'Taper "help" pour afficher la liste des commandes',
               help)

###################################################################################################################

def change_prefix(args):
    new_prefix = args[0]
    CommandParser.prefix = new_prefix
    open("bot/prefix.txt", mode='wt').write(new_prefix)
    return Response("Préfixe de commande changé. Nouveau préfixe: " + new_prefix)

CHANGEPREFIX = Command("changer_préfixe",
                       {"nouveau préfixe": str},
                       "changer le préfixe de commande",
                       change_prefix)

###################################################################################################################

INFO = Command('info',
               {},
               'Plus d\'info sur le bot',
               None)

###################################################################################################################

def latex(args):
    ex = args[0]
    format = str(args[1])

    pref = r'\huge&space;\dpi{100}\bg{white}'

    url = "https://latex.codecogs.com/" + format + ".image?" + pref + ex
    r = requests.get(url)

    file = "bot/temp/image." + format

    open(file, 'wb').write(r.content)

    rep = Response(
        "Depuis l'éditeur d'équation en ligne:\nhttps://latex.codecogs.com/")
    rep.addFile(file)
    return rep

LATEX = Command("latex",
                {"expression": str, "format": ImageFormat},
                "Convertir l'expression latex en image (formats acceptés : svg, gif, png, pdf)",
                latex)

###################################################################################################################

def function(args):
    name: str = args[0]
    ex: Expression = args[1]
    g2d.function(name, ex)

    return Response(name+"(x) ajoutée au graphique")

FUNCTION = Command("fonction",
                   {"nom": str, "expression": Expression},
                   "Créer une fonction",
                   function)

###################################################################################################################

def resize(args):
    g2d.resize(args[0], args[1], args[2], args[3])
    return Response("graphique redimensionné :"+"\nx de {0} à {1}\ny de {2} à {3}".format(args[0], args[1], args[2], args[3]))

RESIZE = Command("redim",
                 {"minX": float, "maxX": float, "minY": float, "maxY": float},
                 "redimensionner le graphique",
                 resize)

###################################################################################################################

def setTitle(args):
    g2d.title(args[0])
    return Response("titre du graphique '" + args[0]+"'")

TITLE = Command("titre",
                {"titre": str},
                "renommer le graphique",
                setTitle)

###################################################################################################################

def clear(args):
    g2d.clear()
    return Response("graphique réinitialisé")

CLEAR = Command("effacer",
                {},
                "efface tout les objets du graphique",
                clear)

###################################################################################################################

def show(args):
    g2d.visualize()
    rep = Response("")
    rep.addFile("bot/temp/plot.png")
    return rep

SHOW = Command("afficher",
               {},
               "visualiser le graphique",
               show)

###################################################################################################################

SOLVE = Command("résoudre",
                {"polynome": Expression},
                "résoudre le polynome du second degré",
                None)


commands["help"] = HELP
commands["changer_préfixe"] = CHANGEPREFIX
commands["info"] = INFO
commands["latex"] = LATEX
commands["fonction"] = FUNCTION
commands["redim"] = RESIZE
commands["titre"] = TITLE
commands["effacer"] = CLEAR
commands["afficher"] = SHOW


class CommandParser:
    prefix: str = open("bot/prefix.txt", encoding='utf-8').read()
    command = ""

    def __init__(self) -> None:
        pass

    def parseCommand(self, command: str) -> Response:
        self.command = command
        self.prefix = open("bot/prefix.txt", encoding='utf-8').read()

        if(command.isspace() or command == ""):
            return Response(Exception("La commande est vide"))
        try:
            words = self.parseWords()
        except Exception as e:
            return Response(e)
        # the first word determine the command
        comm = commands.get(words[0])
        if(comm == None):
            return Response(Exception("Commande inconnue: " + words[0]))
        args = words[1:]

        checkRep = comm.check(args)
        if(isinstance(checkRep, Exception)):
            return Response(checkRep)

        if(comm.resp == None):
            return Response("Aucune réponse disponible pour le moment avec la commande " + comm.name)

        parsedArgs = comm.getArgs(args)
        if(isinstance(parsedArgs, Exception)):
            return Response(parsedArgs)

        return comm.response(parsedArgs)

    def parseWords(self):
        words = []
        tokens = list(self.command)
        i = 0
        while(i < tokens.__len__()):
            t = tokens[i]
            if(t.isspace()):
                i += 1
                continue
            else:
                word, newI = self.parseWord(tokens, i)
                words.append(word)
                i = newI
        return words

    def parseWord(self, tokens: List[str], index: int):
        s = ""
        while (index < tokens.__len__()):
            token = tokens[index]
            if(token == '\"'):
                index += 1
                s, i = self.parseSentence(tokens, index)
                index = i
                break
            elif(token.isspace()):
                index += 1
                break
            else:
                s += token
                index += 1

        return s, index

    def parseSentence(self, tokens: List[str], index: int):
        res = ""
        try:
            while(True):
                token = tokens[index]
                if(token == '\"'):
                    index += 1
                    break
                else:
                    res += token
                    index += 1
        except:
            raise Exception(
                "La phrase n'est pas terminée par un double guillemet : '\"'")
        return res, index


def demo():
    print("command prefix : '!'")
    print("(no need to insert prefix in demo)")
    print('type "exit" to exit the demo')
    print(HELP.description)
    c = CommandParser()

    while(True):
        rep = input(">>>")
        if(rep == "exit"):
            break
        print(c.parseCommand(rep))


# demo()
