import argparse # to parse arguments in the CLI, 99% of CLI code is in this library
import configparser # create config files and parse them
from datetime import datetime # manipulate data and time
import grp, pwd # read user/group data
from fnmatch import fnmatch # to implement .gitignore. match things like *.txt to select all txt files
import hashlib # SHA-1 to generate hashes
from math import ceil
import os
import re
import sys # to access the command line arguments
import zlib # to compress everything

argparser = argparse.ArgumentParser(description="WYAG-VCS")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

class GitRepository (object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion: {vers}")
            
def repo_path(repo, *path):
    return os.path.join(repo.gitdir, *path)

def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add": cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")

if __name__ == "__main__":
    main()