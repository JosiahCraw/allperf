import subprocess
import PyInquirer
import matplotlib.pyplot as mpl

def run_test(run, dir):
    print(run)

    args = run['args'][0].split(" ")
    num_args = len(args)

    questions = [
        {
            'type': 'list',
            'name': 'num_axis',
            'message': 'How Many axis do you want?',
            'choices': [
                {
                    'name': '2'
                },
                {
                    'name': '3'
                }
            ]
        },
        {
            'type': 'input',
            'name': 'xtitle',
            'message': 'X Axis Title:',
        },
        {
            'type': 'list',
            'name': 'xarg',
            'message': 'X Arg Num',
            'choices': [{'name':str(i)} for i in range(num_args)] + [{'name': 'Time'}]
        },
        {
            'type': 'input',
            'name': 'ytitle',
            'message': 'Y Axis Title:',
        },
        {
            'type': 'list',
            'name': 'yarg',
            'message': 'Y Arg Num',
            'choices': [{'name':str(i)} for i in range(num_args)] + [{'name': 'Time'}]
        },
        {
            'type': 'input',
            'name': 'ztitle',
            'message': 'Z Axis Title:',
            'when': lambda answers: not answers.get('num_axis', '2')
        },
        {
            'type': 'list',
            'name': 'zarg',
            'message': 'Z Arg Num',
            'choices': [{'name':str(i)} for i in range(num_args)] + [{'name': 'Time'}],
            'when': lambda answers: not answers.get('num_axis', '2')
        }
    ]

    answers = PyInquirer.prompt(questions)
    print(answers)
    run_outputs = []

    for (i, time_run) in enumerate(run['args']):
        time_run = time_run.split(" ")
        out = None
        try:
            out = subprocess.run(["cd", dir, "&&", "time", "./{}".format(run['bin'])]+time_run, shell=True, stdout=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError:
            print("An Error occurred with the process call")

        if out is not None:
            run_outputs.append(out.stdout)
        else:
            run_outputs.append(None)

    print(run_outputs)
    times = []
    for test_run in run_outputs:
        time = test_run.split('\n')
        time = time[1]
        time = float(time)
        times.append(time)
        print(time)
    
    x = []
    y = []
    z = []

    for i in range(num_args):
        xarg = answers['xarg']
        if xarg == 'Time':
            x.append(times[i])
        else:
            x.append(args.split(" ")[int(xarg)])
        yarg = answers['yarg']
        if yarg == 'Time':
            y.append(times[i])
        else:
            y.append(args.split(" ")[int(yarg)])

        if answers['num_axis'] == '3':
            yarg = answers['yarg']
            if yarg == 'Time':
                z.append(times[i])
            else:
                z.append(args.split(" ")[int(zarg)])

    if answers['num_axis'] == '3':
        mpl.plot(x, y, z)
    else:
        mpl.plot(x, y)

        
    

    

    