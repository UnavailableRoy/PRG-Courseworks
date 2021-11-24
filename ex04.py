#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:50:26 2021

@author: roy
"""

class File :

    def __init__(self):
        self.perm = "rwxr--r--"             # r-read w-write x-execution, three "rwx" are for user, group, others respectively.
        
    def chown(self,new_owner) :             # set new owner
        self.owner = new_owner
        return self.name + ".owner:" + self.owner
    
    def ls(self,flag=""):                   # ls("-l") is like ls -l, or just use ls() to do like ls
        self.lsrec(0,flag)                  # call the method of subclass to print the result.
        

class PlainFile(File):
    
    class_name = "PlainFile"
    
    def __init__(self,name) :
        self.name = name
        self.owner = "default"
        File.__init__(self)                 # inherit from class File

    
    def __str__(self) :
        return  "{}({})"\
            .format(self.class_name,self.name)
            
    def lsrec(self,count,flag) :
        print(self.name)



class Directory(File) :
    
    class_name = "Directory"
    helper = ""                             # for help in str

    
    def __init__(self, name, filelist, owner = "default") :
        self.name = name
        self.filelist = filelist
        self.owner = owner
        File.__init__(self)
    
    def __str__(self) :
        try:
            self.helper = self.helper + str(self.filelist[0]) # the first file should be added initially to avoid too many commas.
            for i in self.filelist[1:] :
                self.helper = self.helper + "," + str(i) # store the file in helper one by one using recursion
        except IndexError :                 # an IndexError means that the directory is empty.
            self.helper = ""

        return  self.class_name + "(" + self.name + "," + "[" + self.helper + "]" + ")"
    
    
    def lsrec(self,count,flag) :
        if count == 0 and flag == "-l" :    # the root should be printed first if the detail is needed.
            print("d" + self.perm + "  " + self.owner.ljust(10) + " | \t" + "\t"*count + self.name)
        else :                              #if detail is not needed or it has gone to subdirectory, just print the name directly
            print(self.name) 
        
        count += 1                          # count is to define how deep the indentation should be.
        
        for i in self.filelist :
            if i.class_name == "PlainFile" :
                print("-",end="")           # "-" represents plainfile in UNIX
            else :
                print("d",end="")           # "d" represents directory in UNIX
                
            if flag == "-l" :               # to distinguish between ls and ls -l
                print(i.perm + "  " + i.owner.ljust(10) + " | \t" + "\t"*count, end = "")
            else :
                print("\t"*count,end="")    # length of indentation is defined by count
            i.lsrec(count,flag)             # call itself to print the files in subdirectory or the plainfile.
            
        
        
        


class FileSystem:
    
    helper = 0                              # for help in some of the methods.
    route = []                              # To store the route of current working directory.


    def __init__(self,direc) :
        self.wd = direc                     # to mark the current working directory (wd)
        self.root = direc                   # to store the root of the directory
        

            
    def pwd(self) :
        self.wd = self.root                 # move to root
        path_root = "/" + self.root.name    # get the root first since it is not in the list of route
        path_ = ""                          # initialise path
        for i in self.route :
            self.wd = self.wd.filelist[i]   # move follow the route list
            path_ += "/" + self.wd.name     # store the names of the directories one by one
        return path_root + path_
     
        
     
    def ls(self,flag="") :
        self.wd.ls(flag)                    # call the method of class File
         
     
        
    def cd(self,filename) :
        if filename == ".." :               # go back to parent directory
            if self.wd == self.root :       # if working directory is root, no need to take action.
                return
            del self.route[-1]              # delete the last element of the list of route, which represent current working directory
            self.wd = self.root             # go back to root
            for i in self.route :           # move to the target directory step by step, following the route.
                self.wd = self.wd.filelist[i]
            return
        else :
            for i in self.wd.filelist :
                if i.name == filename :     # look for the target dile
                    if i.class_name == "PlainFile" : # you cannot move to a plainfile
                        print("Not a directory: {}".format(filename))
                        return
                    else :
                        self.route += [self.wd.filelist.index(i)] # store the route in the list
                        self.wd = i         # move to the target directory
                    break
        if self.wd.name != filename :       # meeting the condition means that the file was not found in current wd
            print ("The directory {} does not exist!".format(filename))
            
    
    
    
    def create_file(self,new_file) :
        for i in self.wd.filelist :         # check whether it is possible to create a file named "new_file"
            if new_file == i.name :
                print("A file with the same name already exists!")
                return
        self.wd.filelist += [PlainFile(new_file)] # add the file as the last element in filelist.
            
        
        
        
    def mkdir(self,new_file,owner="default") :
        for i in self.wd.filelist :         # check if possible
            if new_file == i.name :
                print("A file with the same name already exists!")
                return
            
        self.wd.filelist += [Directory(new_file,[],owner)]
                                            # owner can by indicated if you want

        
                
    def rm(self,name) :
        for i in self.wd.filelist :
            if name == i.name :
                if i.class_name == "Directory" : # if it is a plainfile, just skip the if and remove it
                    if i.filelist != [] :   # check if the directory is empty
                        print("Sorry, the directory is not empty")
                        return
                self.wd.filelist.remove(i)  # remove the file
                return
        print("The file does not exist.")   # if the method did not return and got here, the file does not exist
        

    
    
    def find(self,name) :
        for i in self.wd.filelist :         # check whether there is a file with the same name in current wd
            if name == i.name :
                self.helper = 1             # mark that the file is found
                return self.pwd() + "/" + name # call the method pwd() to show the path
    
        for i in self.wd.filelist :         # if the file is not found in current wd, move to a subdirectory (if there is one)
            if i.class_name == "Directory" :
                self.cd(i.name)             # move to the subdirectory
                result = self.find(name)    # call itself to search in the subdirectory and store the thing it return
                self.cd("..")               # move back to previous directory
                if self.helper == 1:        # if the file is found, just return and stop searching
                    return result
                
        return False                        # if it did not return in previous steps and got here, the file was not found
        
        
        
    def chown_R(self,new_owner):
        self.wd.chown(new_owner)            # chown the current wd before chown the files in subdirectories
        for i in self.wd.filelist :
            i.chown(new_owner)              # chown every file in current wd
            if i.class_name == "Directory" :
                self.cd(i.name)             # move to a subdirectory
                self.chown_R(new_owner)     # call itself to do the chown for a subdirectory
                self.cd("..")               # after chown is completely done in one subdirectory, go back and find the next subdirectory
    
    
    
    def chmod(self,command,filename) :      # command should be like "u/g/o" + "+/-" + "r/w/x" , e.g. fs.chomd("g+x","boot.exe")
                                            # u:user g:group o:others  r:read w:write x:execution
        dic = {"u":0,"g":1,"o":2,\
                      "r":0,"w":1,"x":2}    # the dictionary is to help locate the particular permission
            
        if len(command) != 3 :
            print("Wrong command!")
            return
        
        for i in self.wd.filelist:
            if filename == i.name :
                try:
                    a = dic[command[0]]*3+dic[command[2]]   # to locate the permission needed to be modified
                    if command[1] == "+" :
                        i.perm = i.perm[:a] + command[2] + i.perm[a+1:] # modify the permission
                    elif command [1] == "-" :
                        i.perm = i.perm[:a] + "-" + i.perm[a+1:]        # modify the permission
                    else :
                        print("Wrong command!")      # if command[1] is neither "+" nor "-", it must be a wrong command
                        return
                except KeyError:            # a KeyError means command[0] or command[2] is not in the dictionary. wrong command
                    print("Wrong command!")
                    return
        
        print("The file does not exist.")   # if it did not return in previous steps, the file was not found.
    
            

    def mv(self,filename,path) :
        
        check = 0                           # To mark that whether the file is found in current directory
        pathlist = []                       # To store every directory name in the path
        slash_location = [i for i,x in enumerate(path) if x == "/"] # To store the location of "/"
        
        for i,x in enumerate(slash_location) :
            try:
                pathlist += [path[x+1:slash_location[i+1]]]         # the / should not be stored, so start from x+1
            except IndexError :             # IndexError means the current i is representing the last / .
                pathlist += [path[x+1:]]
                                            # The loop is to store the every directory name into the pathlist with a list.
            
        for i in self.wd.filelist :
            if filename == i.name :
                temp = i
                check = 1
                break
        if check == 0 :
            print("The file does not exists.")
            return
                                            # the two loops above are to check whether the target file exists.
        
        if pathlist[0] != self.root.name :
            print("Not a directory: {}".format(pathlist[0]))
            return
                                            # the first directory should be root.
        
        self.wd.filelist.remove(temp)       # a move is consist of remove and add.
        
        origin_wd = self.wd                 # save the origin working directory
        
        while self.wd.name != self.root.name :
            self.cd("..")
                                            # return to the root to follow the path.
            
        for i in pathlist[1:] :             # pathlist[0] is root, so start from 1
            helper = self.wd.name
            self.cd(i)                      # move follow the path
            if self.wd.name == helper :     # meeting the equation means self.cd didn't work. the path is wrong input.
                self.wd = origin_wd         # go back to the origin wd
                self.wd.filelist += [temp]  # get the file back since it was not moved successfully.
                return
            
        self.wd.filelist += [temp]          # put the target file in the target directory.
        
        
####################
         
file = PlainFile("boot.exe")
folder = Directory("Downloads",[])
    
root = Directory("root",[PlainFile("boot.exe"),
               Directory("home",[
                   Directory("thor",
                      [PlainFile("hunde.jpg"),
                       PlainFile("quatsch.txt")]),
                   Directory("isaac",
                      [PlainFile("gatos.jpg")])])])

fs = FileSystem(root)
        
