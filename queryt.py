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
        index = line.rfind(c_include)
        if index != -1:
            index_end = -1
            for i in range(index+len(c_include), len(line)):
                if line[i] == ")":
                    if index_end == -1:
                        index_end = i
            include_args = line[index+5:index_end]
            print("  Include found : include("+include_args+")"+str(index))
            include_seq = include_args.split(':')
            n_include = len(include_seq)
            to_erase = line[index:index_end+1]
            print("Replace call:'"+to_erase+"', void")
            print("(Incl)"+line)
            to_erase = line[index:index_end+1]
            line = line.split(to_erase)
            file.write(line[0])
            includeTemplate(path, include_seq[0]+".sql", file, include_seq[1:])
            file.write(line[1])
            line = ""
        file.write(line)
    template.close

def queryt(path, template):
    file = open(path+"\\query.sql.txt", "w")
    includeTemplate(path, template, file)
    file.close()
    
              
