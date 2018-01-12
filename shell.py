#!/usr/bin/env python
#
# Flask example. Running shell commands.
# No lack of insecurity.
###

# Python 2/3 compatibility
from __future__ import print_function

from flask import Flask, render_template, request
import subprocess

# local functions

# Print one or more strings
def dbg(s, *args):
    print('DBG: ' + str(s), end='')
    for s in args:
        print(' ' + str(s), end='')
    print('', end='\n')

# Extremely insecure, run any shell command, including pipes
def run_cmd(cmd):
    dbg('run_cmd:', cmd)
    try:
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        ret = p.communicate()[0]
    except Exception as e:
        err = str(e)
        dbg('Exception for cmd: "' + cmd + '":\n' + err)
        ret = err
    return ret

# Main

app = Flask(__name__)
app.secret_key = '''
Pregnancy is a kind of miracle. Especially so in that it proves
that a man and woman can conspire to force God to create a new soul.
'''

@app.route('/', methods=['GET', 'POST'])
def main():
    title = 'Shell Kriminell'
    # dbg('method: ' + request.method)
    if request.method == 'POST':
        cmd = request.form.get('Command')
        output = run_cmd(cmd)
        if output:
            rows = str(len(output.split('\n')))
            # dbg('output:', output)
            return render_template('index.html', output = output,
                                   rows = rows, title = title,
                                   oldcmd = cmd)

    # GET or failed POST
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
