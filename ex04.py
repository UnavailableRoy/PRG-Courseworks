#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:50:26 2021

@author: roy
"""

class File :

    def __init__(self):
        self.owner = "default"
        self.perm = "rwxrwxrwx"
        
    def chown(self,new_owner) :
        self.owner = new_owner
        return self.name + ".owner:" + self.owner
    
    def ls(self):
        return self.lsrec(0)
    
        

class PlainFile(File):
    
    class_name = "PlainFile"
    
    def __init__(self,name) :
        self.name = name
        File.__init__(self)

    
    def __str__(self) :
        return  "{}({})"\
            .format(self.class_name,self.name)
            
    def lsrec(self,count) :
        print(self.name)



class Directory(File) :
    
    class_name = "Directory"
    helper = ""

    
    def __init__(self,name,filelist) :
        self.name = name
        self.filelist = filelist
        File.__init__(self)
    
    def __str__(self) :
        try:
            self.helper = self.helper + str(self.filelist[0])
            for i in self.filelist[1:] :
                self.helper = self.helper + "," + str(i)
        except IndexError :
            self.helper = ""

        return  self.class_name + "(" + self.name + "," + "[" + self.helper + "]" + ")"
    
    
    def lsrec(self,count) :
        print(self.name)
        count += 1
        for i in self.filelist :
            print("\t"*count,end="")
            i.lsrec(count)


class FileSystem:
    
    helper = 0
    route = []
    uhelper = 0
    mhelper = 0
    phelper = 0

    def __init__(self,direc) :
        self.wd = direc
        self.root = direc
        
    def pwd(self) :
        self.wd = self.root
        print("/" + self.wd.name, end = "")
        for i in self.route :
            self.wd = self.wd.filelist[i]
            print("/" + self.wd.name, end = "")
     
    def ls(self) :
         return self.wd.ls()
         
     
        
    def cd(self,filename) :
        if filename == ".." :
            del self.route[-1]
            self.wd = self.root
            for i in self.route :
                self.wd = self.wd.filelist[i]
            return
        else :
            for i in self.wd.filelist :
                if i.name == filename :
                    if i.class_name == "PlainFile" :
                        print("Not a directory: {}".format(filename))
                        return
                    else :
                        self.route += [self.wd.filelist.index(i)]
                        self.wd = i
                    break
        if self.wd.name != filename :
            print ("The directory does not exist!")
            
    
    
    
    def create_file(self,new_file) :
        for i in self.wd.filelist :
            if new_file == i.name :
                print("A file with the same name already exists!")
                return
        self.wd.filelist += [PlainFile(new_file)]
            
        
        
        
    def mkdir(self,new_file,owner="default") :
        for i in self.wd.filelist :
            if new_file == i.name :
                print("A file with the same name already exists!")
                return
            
        self.wd.filelist += [Directory(new_file,[])]
        self.wd.filelist[-1].owner = owner

        
                
    def rm(self,name) :
        for i in self.wd.filelist :
            if name == i.name :
                self.helper = self.wd.filelist.index(i)
                if i.class_name == "Directory" :
                    if i.filelist != [] :
                        print("Sorry, the directory is not empty")
                        return
                del self.wd.filelist[self.helper]
                return
        print("The file does not exists.")
        
        


    def find(self,name) :
            
        for i in self.wd.filelist :
            if name == i.name :
                self.pwd()
                print("/" + name)
                self.helper = 1
                return
    
        for i in self.wd.filelist :
            if i.class_name == "Directory" :
                self.cd(i.name)
                self.find(name)
                self.cd("..")
                if self.helper == 1:
                    return
        print("False")
        
        
        
    def chown_R(self,new_owner):
        self.wd.chown(new_owner)
        for i in self.wd.filelist :
            i.chown(new_owner)
            if i.class_name == "Directory" :
                self.cd(i.name)
                self.chown_R(new_owner)
                self.cd("..")
    
    
    
    def chmod(self,command,filename) :
        
        dic = {"u":0,"g":1,"o":2,\
                      "r":0,"w":1,"x":2}
            
        if len(command) != 3 :
            print("Wrong command!")
            return
        
        for i in self.wd.filelist:
            if filename == i.name :
                try:
                    a = dic[command[0]]*3+dic[command[2]]
                    if command[1] == "+" :
                        i.perm = i.perm[:a] + command[2] + i.perm[a+1:]
                    elif command [1] == "-" :
                        i.perm = i.perm[:a] + "-" + i.perm[a+1:]
                    else :
                        print("Wrong command!")
                        return
                except KeyError:
                    print("Wrong command!")
                    return
    
    
    
    def ls_l(self) :
        dic = {"PlainFile":"-","Directory":"d"}
        for i in self.wd.filelist :
            print (dic[i.class_name] + i.perm + "  " + i.owner + "  " + i.name)
            


                
                
                
    
    
    

         
         
         
         
         
         
         
         
         
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
        

        


        



""" 
    def ls(self) :
         for i in self.wd.filelist :
             self.lshelper += i.name + "\n"
         print(self.lshelper)
"""