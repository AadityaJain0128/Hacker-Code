import subprocess

def verify(qno, user):
    with open(f"static/testcases/testcase_{qno}.txt", "r") as f:
        data = f.read().split("\n")

    path = f"static/users/{user}/problem_{qno}.txt"
    with open(path) as f:
        script = f.read()
    if "import os" in script:
        msg = ["Error in Code", "You cannot use OS Module."]
        return False, msg, "red"

    for io in data:
        inp, out = io.split("||")
        inp = inp.replace("\\n", "\n").strip()
        out = out.replace("\\n", "\n").strip()
        try:
            output = subprocess.run(["python", path], capture_output=True, text=True, input=inp, timeout=11)
            if output.returncode == 0:
                if output.stdout.strip() != out:
                    inp = str(inp).replace("\n", "\\n")
                    out = str(out).replace("\n", "\\n")
                    output = str(output.stdout).replace("\n", "\\n")
                    msg = ["All Private Test Cases are not Passed.", f"For Input :- {inp}", f"Expected Output :- {out}", f"But got :- {output}", "as the Output"]
                    return False, msg, "yellow"
            else:
                msg = ["Error in Code"] + "".join((output.stderr).split(",")[1:]).split("\n")
                return False, msg, "red"

        except:
            msg = ["Time Limit Exceeded."]
            return False, msg, "red"

    msg = ["Submission Successful.", "All Private Test Cases are Passed."]
    return True, msg, "green"


if __name__ == "__main__":
    print(verify(1, "demo"))
    # print(verify(1, "aaditya01"))