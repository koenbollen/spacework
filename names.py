
# By Joris Dormans, 2013


import random

nameGrammar = [
  [["NAME"], ["FIRSTTHING", "SECONDTHING"]],
  [["FIRSTTHING"], ["VERB"], ["TYPE"], ["TYPE", "OPERATOR"], ["TYPE", "MODIFIER"], ["OPERATOR", "OPERATEE"], ["OPERATEE", "OPERATOR"], ["PREFIX", "OPERATOR"], ["MODIFIER", "FIRSTTHING"]],
  [["SECONDTHING"], ["OPERATOR"], ["OPERATOR", "VERSION"], ["OPERATEE", "GREEK"], ["OPERATEE", "OPERATEE"]],
  [["OPERATEE"], ["memory"], ["block"], ["function"], ["instance"], ["object"], ["class"], ["fix"], ["bug"], ["exception"], ["sort"], ["callback"], ["function", "call"]],
  [["GREEK"], ["alpha"], ["beta"], ["gamma"], ["delta"], ["epsilon"], ["omega"]],
  [["OPERATOR"], ["operator"], ["incrementer"], ["decrementer"], ["multiplier"], ["transformer"], ["iterator"], ["calculator"], ["initializer"], ["parser"], ["completer"], ["actor"], ["fix"], ["debugger"], ["sorter"], ["handler"], ["handler"]],
  [["VERSION"], ["%2"], ["%3"], ["%_v2"], ["%_v0"], ["%0.1"], ["%0.2"], ["%0.9"], ["%0.99"], ["%1.0"]],
  [["MODIFIER"], ["sloppy"], ["clever"], ["quick"], ["dirty"], ["temporary"], ["final"], ["permanent"], ["universal"], ["previous"], ["working"], ["temp"], ["new"], ["improved"], ["slow"], ["advanced"], ["expensive"], ["half"], ["leaky"], ["safe"], ["unsafe"], ["bitwise"], ["root"], ["linked"], ["double"], ["backwards"], ["parallel"], ["linear"]],
  [["PREFIX"], ["no%"], ["pro%"], ["un%"], ["after%"], ["%"]],
  [["TYPE"], ["int %"], ["class %"], ["struct %"], ["bool %"], ["void %"], ["char %"], ["//%"]],
  [["VERB"], ["growing"], ["debugging"], ["sorting"], ["moving"], ["animating"], ["bitshifting"], ["multiplying"]]
]

styleGrammar = [
  [["STYLE"], ["CAPS", "MOD"]],
  [["CAPS"], ["capitalize", "SPACE"], ["camelcaps", "nospace", "FUNCTIONCALL"], ["lowercase", "SPACE"]],
  [["MOD"], ["none"], ["none"], ["none"], ["none"], ["abrivated"]],
  [["SPACE"], ["space"], ["dots", "FUNCTIONCALL"], ["dashes", "FUNCTIONCALL"], ["underscores", "FUNCTIONCALL"]],
  [["FUNCTIONCALL"], ["none"], ["functioncall"] ]
]


def getOptions(symbol, grammar):
  result = []
  for rule in grammar:
    left = rule[0]
    if left[0] == symbol:
      i = 1
      while i < len(rule):
        result.append(rule[i])
        i += 1
  return result

def chooseOption(symbol, grammar):
  options = getOptions(symbol, grammar)
  if len(options) == 0:
    return []
  r = random.randint(0, len(options)-1)
  return options[r]

def replace(string, grammar):
  i = 0
  while i<len(string):
    symbol = string[i]
    replace = chooseOption(symbol, grammar)
    if len(replace)>0:
      del string[i]
      j = 0
      while j<len(replace):
         string.insert(i, replace[j])
         i+=1
         j+=1
    else:
      i+=1
  return string

def terminated(string):
  i = 0
  while i<len(string):
    if string[i].isupper():
      return 0
    i+=1
  return 1

def generate(string, grammar):
  t = 100
  while terminated(string) == 0 and t > 0:
    string = replace(string, grammar)
    t-=1
  return string

def contains(l, v):
  i = 0
  while i<len(l):
    if l[i] == v:
      return True
    i += 1
  return False

def formatName(name, style):
  result = ""
  if contains(style, "capitalize"):
     i = 0
     while i < len(name):
       if name[i][len(name[i])-2:] != " %":
         name[i] = name[i].capitalize()
       i += 1
  if contains(style, "camelcaps"):
     i = 1
     while i < len(name):
       if name[i][len(name[i])-2:] != " %":
         name[i] = name[i].capitalize()
       i += 1
  if contains(style, "allcaps"):
     i = 0
     while i < len(name):
       if name[i][len(name[i])-2:] != " %":
         name[i] = name[i].upper()
       i += 1

  if contains(style, "abrivated"):
     i = 0
     while i < len(name):
       if name[i][len(name[i])-2:] != " %":
         name[i] = name[i][:3]
       i += 1

  spacer = " "
  if contains(style, "dots"):
    spacer = "."
  if contains(style, "dashes"):
    spacer = "-"
  if contains(style, "underscores"):
    spacer = "_"
  if contains(style, "nospace"):
    spacer = ""

  for n in name:
    if result == "":
      result += n
    elif n[0] == "%":
      result += n[1:]
    elif result[len(result)-1] == "%":
      result = result[:len(result)-1]+n
    else:
      result += spacer+n

  if contains(style, "functioncall"):
    result += "()"
  return result


def buildname():
    return formatName(generate(["NAME"], nameGrammar), generate(["STYLE"], styleGrammar))



if __name__ == "__main__":
    for i in xrange(5):
        print(formatName(generate(["NAME"], nameGrammar), generate(["STYLE"], styleGrammar)))

# vim: expandtab tabstop=4 softtabstop=4 shiftwidth=4 textwidth=79:
