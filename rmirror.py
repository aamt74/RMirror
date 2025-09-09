import sys
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from pathlib import Path
from typing import Dict
from settings import hostname, username, password
from entry import Entry, EntryUtils


def main():

    if len(sys.argv) != 2:
        print("Usage: rmirror.py <destination path>\n\nExample: python3 rmirror.py ~/Downloads")   
        exit(1)
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("Created by rdWei: https://www.github.com/rdwei\n\nUsage: rmirror.py <destination path>\n\nExample: python3 rmirror.py ~/Downloads")   
        exit(0)

    destination_path = sys.argv[1]

    # Open SSH connection
    ssh = SSHClient()
    try:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
    except Exception as e:
        print(f"Error while opening connection: {e}")
        sys.exit(1)

    # Get directory listing
    _, stdout, _ = ssh.exec_command("ls .local/share/remarkable/xochitl/*.metadata")
    file_list = stdout.read().decode("utf-8").splitlines()

    # Create entries
    print("getting metadata...")
    entries_map: Dict[str, Entry] = {}
    for filename in file_list:
        id = Path(filename).stem
        _, stdout, _ = ssh.exec_command("cat " + filename)
        metadata = stdout.read().decode("utf-8")
        entries_map[id] = Entry(id, metadata)

    # Complete relative paths
    for id, entry in entries_map.items():
        completed_path = EntryUtils.CompletePath(entry, entries_map)
        entries_map[id].relative_path = completed_path

    # Create all directories locally
    local_root = Path(destination_path)
    for entry in entries_map.values():
        if entry.is_dir():
            local_root.joinpath(entry.relative_path).mkdir(parents=True, exist_ok=True)

    # Prepare progress info
    done = 0
    todo = 0
    for entry in entries_map.values():
        if entry.is_file() and "trash" not in str(entry.relative_path):
            todo += 1

    # Start mirroring (first fast scp, then slow http)
    for entry in entries_map.values():
        if entry.is_file() and "trash" not in str(entry.relative_path):
            done += 1
            progress = int(100 * done / todo)
            path_dst = local_root.joinpath(entry.relative_path)
            print(f"[{progress:3d}%]" + " downloading " + str(path_dst))
            with SCPClient(ssh.get_transport()) as scp:
                try:
                    remote_path = f".local/share/remarkable/xochitl/{entry.ID}.pdf"
                    local_path = path_dst
                    scp.get(remote_path, local_path)
                except Exception:
                    path_src = EntryUtils.DownloadPdf(entry)
                    path_src.rename(path_dst)

    # End SSH connection
    try:
        ssh.close()
    except Exception as e:
        print(f"Error while closing connection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
