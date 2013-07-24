def includeTemplate(path, template_path, file, args = []):
    print("  Opening template "+path+"\\"+template_path)
    temp = "With arguments"
    for arg in args:
        temp = temp + ":" + arg
    print(temp)
    c_include = "@INC("
    c_range = "@RNG("
    template = open(path+"\\"+template_path, "r")
    n_args = len(args)
    for line in template:
        print("(Base)"+line)
        for i in range(0, n_args):
            line = line.replace("@VAR"+str(i)+"$", args[i])
            print("Replace call:'"+"@VAR"+str(i)+"$"+"', "+args[i])
        print("(Repl)"+line)
        line = parseRange(line, file, path, c_range, c_include)
        line = parseInclude(line, file, path, c_include)
        file.write(line)
    template.close

def parseRange(line, file, path, c_range, c_include):
    index = line.rfind(c_range)
    if index != -1:
        index_end = -1
        for i in range(index+len(c_include), len(line)):
            if line[i] == ")":
                if index_end == -1:
                    index_end = i
        include_args = line[index+5:index_end]
        print("  Range found : range("+include_args+")")
        include_seq = include_args.split(':')
        to_erase = line[index:index_end+1]
        for i in range(int(include_seq[0]), int(include_seq[1])+1):
            newline = line.replace(to_erase, str(i))
            newline = parseInclude(newline, file, path, c_include)
            file.write(newline)
        line = ""
    return line

def parseInclude(line, file, path, c_include):
    index = line.rfind(c_include)
    if index != -1:
        index_end = -1
        for i in range(index+len(c_include), len(line)):
            if line[i] == ")":
                if index_end == -1:
                    index_end = i
        include_args = line[index+5:index_end]
        print("  Include found : include("+include_args+")")
        include_seq = include_args.split(':')
        n_include = len(include_seq)
        to_erase = line[index:index_end+1]
        print("Replace call:'"+to_erase+"', void")
        print("(Incl)"+line)
        line = line.split(to_erase)
        file.write(line[0])
        includeTemplate(path, include_seq[0]+".sql", file, include_seq[1:])
        file.write(line[1])
        line=""
    return line

def queryt(path, template):
    file = open(path+"\\query.sql.txt", "w")
    includeTemplate(path, template, file)
    file.close()
    
              
