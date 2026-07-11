import os
import subprocess
import datetime
import re

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(PROJECT_DIR, '.last_version')
VERSION_PATTERN = r"2\.0\.0[^\s]*"

# Git 完整路径（系统 PATH 中没有 git）
GIT_CMD = r"C:\Program Files\Git\cmd\git.exe"

def get_current_version():
    version = None
    hopekit_file = os.path.join(PROJECT_DIR, 'hopekitmain.py')
    if os.path.exists(hopekit_file):
        with open(hopekit_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(VERSION_PATTERN, content)
            if matches:
                version = matches[0]
    return version

def get_last_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def save_version(version):
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        f.write(version)

def run_git_command(cmd):
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def has_changes():
    code, stdout, stderr = run_git_command([GIT_CMD, 'status', '--porcelain'])
    if code != 0:
        return False, f"git status failed: {stderr}"
    return len(stdout.strip()) > 0, None

def commit_and_push(version):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"chore: update version to {version} [auto-commit {now}]"
    
    code, stdout, stderr = run_git_command([GIT_CMD, 'add', '.'])
    if code != 0:
        return False, f"git add failed: {stderr}"
    
    code, stdout, stderr = run_git_command([GIT_CMD, 'commit', '-m', commit_msg])
    if code != 0:
        return False, f"git commit failed: {stderr}"
    
    code, stdout, stderr = run_git_command([GIT_CMD, 'push'])
    if code != 0:
        return False, f"git push failed: {stderr}"
    
    return True, "Commit and push successful"

def main():
    log_file = os.path.join(PROJECT_DIR, 'auto_commit.log')
    
    def log(msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {msg}\n")
        print(msg)
    
    log("=== Auto Version Commit Task Started ===")
    
    current_version = get_current_version()
    last_version = get_last_version()
    
    log(f"Current version: {current_version}")
    log(f"Last recorded version: {last_version}")
    
    if not current_version:
        log("ERROR: Could not detect current version")
        return
    
    if current_version == last_version:
        log("Version unchanged, skipping commit")
        return
    
    has_change, err = has_changes()
    if err:
        log(f"WARNING: Cannot check git status: {err}")
        log("Assuming git is not available or not configured")
        save_version(current_version)
        return
    
    if not has_change:
        log("No changes detected, skipping commit")
        save_version(current_version)
        return
    
    log(f"Version changed from '{last_version}' to '{current_version}', proceeding with commit")
    
    success, msg = commit_and_push(current_version)
    if success:
        log(f"SUCCESS: {msg}")
        save_version(current_version)
    else:
        log(f"FAILURE: {msg}")
    
    log("=== Auto Version Commit Task Finished ===")

if __name__ == "__main__":
    main()