import os

b_git_repo_exist = False


def check_git_repository():
    global b_git_repo_exist
    is_git_repo = os.path.exists(".git")
    if not is_git_repo:
        choice = input(
            "This directory is not a git repository. Do you want to initialize it as a git repository? (y/n): "
        )
        if choice.lower() in ["y", "yes"]:
            os.system("git init")
            remote_url = input("Enter the URL of the remote repository: ")
            os.system(f"git remote add origin {remote_url}")
            b_git_repo_exist = True
        else:
            print("Skipping initialization of git repository.")
    else:
        b_git_repo_exist = True


def create_or_skip_file(file_name, content):
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            file.write(content)
    else:
        print(f"Skipping creation of {file_name} as it already exists.")


def commit_and_push_changes():
    if b_git_repo_exist:
        choice = input(
            "Do you want to commit and push these changes automatically? (y/n): "
        )
        if choice.lower() in ["y", "yes"]:
            os.system("lua gitPusher.lua")
        else:
            print("Skipping automatic commit and push.")
    else:
        print("Not a git repository. Skipping automatic commit and push.")


gitignore_content = r"""
# Ignore Visual Studio IDE files
.vs/
.vscode/
.suo
.vcxproj
.vcproj
.pdb
.user
.userprefs
.dll
.exe

# Ignore JetBrains IntelliJ IDEA files
.idea/
.iml

# Ignore Eclipse IDE files
.classpath
.project
.settings/

# Ignore NetBeans IDE files
nbproject/

# Ignore Sublime Text editor files
*.sublime-project
*.sublime-workspace

# Ignore C/C++ compiled files and build directories
*.o
*.obj
*.out
*.dll
*.so
*.dylib
build/
Debug/
Release/

# Ignore C# compiled files
bin/
obj/

# Ignore Java compiled files
*.class
target/

# Ignore Python bytecode files
*.pyc
__pycache__/

# Ignore Lua compiled files
*.luac

# Ignore Node.js dependencies
node_modules/

# Ignore npm debug log
npm-debug.log*

# Ignore yarn lockfile
yarn.lock

# Ignore Editor-specific files
.DS_Store
Thumbs.db

# Unity generated files
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/
[Mm]emoryCaptures/
[Cc]ache/
/*.sln
/*.csproj
/*.unityproj
/*.sln.DotSettings.user
.AppleDouble
.LSOverride
._*
*.apk
*.unitypackage
/*.apk
/*.aab
/*.app
/*.ipa
.gradle/
/gradlew
/gradle-wrapper.jar
.vscode/

# Ignore Intermediate, Saved, and Build directories generated by UE4
Intermediate/
Saved/
DerivedDataCache/
Build/

# Ignore compiled binaries and executables
Binaries/
*.log
*.ini
*.uproject.user
*.xcodeproj
*.xcworkspace
*.xcuserstate
DerivedDataCache/
"""

auto_commit_content = r"""lua ./gitPusher.lua
git status
pause
"""

git_pusher_lua_content = r"""
local branchName = "master"


local function commander(argToExcute)
    local result = io.popen(argToExcute)
    local strInfo = result:read("*all")
    return strInfo
end

function tryTillSucceed(arg, tryTimes)
    tryTimes = tryTimes or 1000
    for i = 1, tryTimes, 1 do
        print("argument is: ", arg)
        local res = commander(arg)
        if res ~= "" then
            print("Conduction succeeded!")
            break
        end
    end
end

-- local curTime = os.date("%c")
local curTime = os.date("%Y-%m-%d %H:%M:%S")
print(curTime)
local cmds = {
    "git pull",
    "git add .",
    ("git commit -m \"%s"):format(tostring(curTime)) .. "\"",
    "git push -u origin " .. branchName,
    "git pull"
}

local pushMaster2github = "git push -u origin " .. branchName
local pull = "git pull"
for i = 1, #cmds, 1 do
    print(("running `%s`"):format(cmds[i]))
    commander(cmds[i])
end
tryTillSucceed(pull)
tryTillSucceed(pushMaster2github)

"""

config_yml_content = r"""theme: jekyll-theme-minimal
title: Some Project Name
description: "Some Description"
"""

readme_content = r"""# Initial Public Repository
### [[Project](https://ezharjan.github.io/SomeProjectName)] [[Code](https://github.com/Ezharjan/SomeProjectName/)] [[Paper(comming soon)](https://arxiv.org/)] 
> [**Some Project Name**](https://arxiv.org),            
> Alexander Ezharjan
> **Arxiv preprint(coming soon)**

**Official repository of Some Project Name.** 

## Abstract
This is the repository for Some Project Name doing Something.

## 📜 BibTeX
```bibtex
@software{project_name,
    author = {Alexander Ezharjan},
    title = {{Some Project Name}},
    url = {https://github.com/Ezharjan/SomeProjectName},
    year = {2024}
}
```

<br>

"""


if __name__ == "__main__":
    check_git_repository()
    create_or_skip_file(".gitignore", gitignore_content)
    create_or_skip_file("_auto-commit.bat", auto_commit_content)
    create_or_skip_file("gitPusher.lua", git_pusher_lua_content)
    create_or_skip_file("_config.yml", config_yml_content)
    create_or_skip_file("README.md", readme_content)

    commit_and_push_changes()
