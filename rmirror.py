import paramiko
import sys

from settings import * 
from entry.entry import Entry, EntryType


def main():

    if len(sys.argv) != 2:
        print("Usage: rmirror.py <destination path>\n\nExample: python3 rmirror.py ~/Downloads")   
        exit(1)
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("Created by rdWei: https://www.github.com/rdwei\n\nUsage: rmirror.py <destination path>\n\nExample: python3 rmirror.py ~/Downloads")   
        exit(0)
    
    destination_path = sys.argv[1]


    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accetta automaticamente la chiave dell'host
    client.connect(hostname, username=username, password=password)


    _, stdout, _ = client.exec_command("ls .local/share/remarkable/xochitl/")

    file_list = stdout.read().decode("utf-8").splitlines()

    filtered_files = [file for file in file_list if file.endswith('.pdf') or file.endswith('.metadata')]


    # Append Entry
    entry_list = []


    for filename in filtered_files:
        ID = filename.split(".")[0]
        if (filename.split(".")[1] == "metadata"):
            _, stdout, _ = client.exec_command("cat .local/share/remarkable/xochitl/"+filename)
            content = stdout.read().decode("utf-8")
            e = Entry(ID, content)

            if "trash" not in e.itsMetadataContent:
                entry_list.append(e)
            
    
    # Initialize parent directory
    for x in entry_list:
        parentID = x.itsMetadataContent.split("parent")[1].split("\"")[2]
        for y in entry_list:
            if y.itsID == parentID:
                x.itsParentVisibleName = y.itsVisibleName
                

    # End Connection
    try:
        client.close()
    except Exception as e:
        print(f"Errore durante la chiusura: {e}")


    # Divide Entry By Type
    directory_entry_list = []
    file_entry_list = []

    for x in entry_list:
        if x.itsType == EntryType.DIRECTORY:
            directory_entry_list.append(x)
        else:
            file_entry_list.append(x)

    
    # Create File Tree
    Entry.createTree(directory_entry_list, destination_path)
    

    for x in file_entry_list:
        if (x.itsParentVisibleName == "trash"):
            continue
        x.downloadPdf(directory_entry_list, destination_path)
    

if __name__ == "__main__":
    main()
