"""This script is wrote for compile database."""
import json
import os
import re
from sys import argv


def getContent(dir, filename):
    """Get response file(.rsp file) content."""
    try:
        rsp_content = open(dir+"/"+filename.group(1), 'r')
    except Exception:
        print("Open response file failed.")
        return filename

    return rsp_content.read()[0:-1]  # no '\n' at the end


if __name__ == "__main__":
    if len(argv) == 1:
        cdb_dir = os.path.abspath(os.getcwd())
    else:
        cdb_dir = os.path.abspath(argv[1])

    if not os.path.isfile(r'{}//compile_commands.json'.format(cdb_dir)):
        print("compile_commands.json doesn't exist!")
    else:
        cdb_json = open(r'{}//compile_commands.json'.format(cdb_dir), 'rt')
        cdb_list = json.load(cdb_json)
        cdb_json.close()
        for codefile in cdb_list:
            codefile['directory'] = re.sub(r'([A-Z])(:[\\/][^<>/\\|:"?*])', lambda path: path.group(1).lower()+path.group(2), codefile['directory'])
            codefile['command'] = re.sub(r'@(.+\.rsp)', lambda filename: getContent(codefile['directory'], filename), codefile['command'])
            codefile['command'] = re.sub(r'([A-Z])(:[\\/][^<>/\\|:"?*])', lambda path: path.group(1).lower()+path.group(2), codefile['command'])
            codefile['file'] = re.sub(r'([A-Z])(:[\\/][^<>/\\|:"?*])', lambda path: path.group(1).lower()+path.group(2), codefile['file'])

        cdb_json = open('compile_commands.json', 'wt')
        json.dump(cdb_list, cdb_json, indent=2)
        cdb_json.close()

        print("compile_commands.json file adjust done.")
