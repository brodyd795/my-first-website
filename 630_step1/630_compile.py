import os,string
import re

dirpath = "path/to/dir"
allfiles = os.listdir(dirpath)
newfile = open("path/to/dir", 'w')
count = 0

for g in allfiles:
    if g.endswith(".txt"):
        full_path = os.path.join(dirpath,g)
        with open(full_path, encoding='utf-8', errors="replace") as f:
            i = " ".join(line.strip() for line in f)
            d = "."
            q = "?"
            #s = [e+d for e in re.split('[\.\?\!]',i) if e]
            s = [e+d for e in i.split(d) if e]
            for item in s:
                if "There is" in item:
                    newfile.write(item + '\n')
                if "there is" in item:
                    newfile.write(item + '\n')
                if "There are" in item:
                    newfile.write(item + '\n')
                if "there are" in item:
                    newfile.write(item + '\n')
                if "There was" in item:
                    newfile.write(item + '\n')
                if "there was" in item:
                    newfile.write(item + '\n')
                if "There were" in item:
                    newfile.write(item + '\n')
                if "there were" in item:
                    newfile.write(item + '\n')
            """m = re.search('[\.\!\?]',i)
            for h in m.span():
                data = re.split('\s',h)
                for p in data:
                    if "There is" in p:
                        newfile.write(p+'\n')

            # if instance of punctuation plus whitespace
                # split at whitespace
            data = re.split("[\.\?\!]\s", i)
            for p in data:
                if "There is" in p:
                    newfile.write(p+'\n')
                if "there is" in p:
                    newfile.write(p+'\n')
                if "There are" in p:
                    newfile.write(p+'\n')
                if "there are" in p:
                    newfile.write(p+'\n')
                if "There was" in p:
                    newfile.write(p+'\n')
                if "there was" in p:
                    newfile.write(p+'\n')
                if "There were" in p:
                    newfile.write(p+'\n')
                if "there were" in p:
                    newfile.write(p+'\n')



            print(data)
            for item in data:
                if "There is" in i:
                    print(i)
            for item in f:
                f = str(f)
                data = f.split(".")
                print(data)
        full_string = f.readlines()
        print(full_string)


for g in allfiles:
    if g.endswith(".txt"):
        print(g)
        full_path = os.path.join(dirpath,g)
        with open(full_path, encoding='utf-8', errors="replace") as f:
            print(f)
            data = f.read().replace('\n',' ')
            print(data)
            sep_data = data.split('.')
            for item in sep_data:
                if "There is" in item:
                    print(item)
                    newfile.write("%s\n" % item)
                if "There are" in item:
                    print(item)
                    newfile.write("%s\n" % item)
                if "There were" in item:
                    print(item)
                    newfile.write("%s\n" % item)
                if "There was" in item:
                    print(item)
                    newfile.write("%s\n" % item)



"""