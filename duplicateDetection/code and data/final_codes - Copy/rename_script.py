import os

def rename_all_in_dir(directory):
    
    for dirpath,dirnames,files in os.walk(directory):
        for file in files:
            print file
            if not file.endswith(".txt"):
                temp = os.path.join(dirpath,file)
                os.rename(temp, temp+'.txt')

rename_all_in_dir('D:\\users\\pravin\\Downloads\\20_newsgroups\\some')
