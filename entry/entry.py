import os
import requests
from enum import Enum


class EntryType(Enum):
    FILE = 1
    DIRECTORY = 2

class Entry:

    def __init__(self, itsID, metadataContent):
        self.itsParentVisibleName = "None"
        self.itsMetadataContent = metadataContent
        self.itsID = itsID

        # Detect EntryType
        if ("CollectionType" in self.itsMetadataContent):
            self.itsType = EntryType.DIRECTORY
        else:
            self.itsType = EntryType.FILE
        
        # Detect VisibleName
        self.itsVisibleName = self.itsMetadataContent.split("visibleName")[1].split("\"")[2]

    def isParent(self, elementList):
        for x in elementList:
            if x.itsParentVisibleName == self.itsVisibleName:
                return True
        return False
    
    def createPath(self, destinationPath, dir_entry_list):
        currentDir = self
         
        full_dir_path = destinationPath
        dir_name_list = []
        dir_name_list.append(currentDir.itsVisibleName)

        while True:
            dir_name_list.insert(0, currentDir.itsParentVisibleName)
            for x in dir_entry_list:
                if x.itsVisibleName == currentDir.itsParentVisibleName:
                    currentDir = x
            if currentDir.itsParentVisibleName == "None" :
                dir_name_list.insert(0, currentDir.itsVisibleName)
                break

        # Without this block the path will be first/first/...
        # idk how to solve that sh1t
        if dir_name_list[0] == dir_name_list[1]: 
            dir_name_list.pop(0)

        for x in dir_name_list:
            full_dir_path = full_dir_path + "/" + x


        os.makedirs(full_dir_path, exist_ok=True)
   
    
    @staticmethod
    def filePath(file, entry_file_list, destinationPath):
        path = file.itsVisibleName

        while file.itsParentVisibleName != "None":
            for x in entry_file_list:
                if x.itsVisibleName == file.itsParentVisibleName:
                    file = x
                    path = x.itsVisibleName + "/" + path

        path = destinationPath + "/" + path

        return path
    
    def downloadPdf(self, entry_file_list, destinationPath):
        r = requests.get(f"http://10.11.99.1/download/{self.itsID}/placeholder", stream=True)
        output_file = "placeholder" 
        with open(output_file, "wb") as file:
            for chunk in r.iter_content(chunk_size=8192):  # Legge il file a blocchi
                file.write(chunk)
        os.rename("placeholder", Entry.filePath(self, entry_file_list, destinationPath) + ".pdf")

    @staticmethod
    def createTree(directory_entry_list, destination_path):
        for x in directory_entry_list:
            if not x.isParent(directory_entry_list):
                x.createPath(destination_path, directory_entry_list) 
