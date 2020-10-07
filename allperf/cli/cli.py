import PyInquirer
import ast
# from ..perf_tests import gprof, cachegrind

class CLI():
    def __init__(self, config):
        self.config = config
        cfg = config.get_cfg()
        past_runs = []
        self.past_questions = None

        if cfg['runs'] != []:
            if cfg['runs'] != {}:
                self.past_questions = [
                    {
                        'type': 'confirm',
                        'name': 'use_past',
                        'message': 'Some Past Runs were found, would you like to use on of those?\n',
                    },
                    {
                        'type': 'list',
                        'name': 'past_runs',
                        'message': 'Which past test would you like to run?',
                        'choices': [{'name': choice['name']} for choice in cfg['runs']],  
                        'when': lambda answers: answers['use_past']

                    }
                ]

        self.questions = [
            {
                'type': 'confirm',
                'name': 'save',
                'message': 'Would you like to save this run for future use?'
            },
            {   
                'type': 'input',
                'name': 'save_name',
                'message': 'Name to save the run under',
                'when': lambda answers: answers['save']
            },
            {
                'type': 'input',
                'name': 'git_ref',
                'message': 'What\'s the Git reference (SHA, Branch, Tag, etc.)? Blank for current ref\n',
            },
            {
                'type': 'list',
                'name': 'test',
                'message': 'Select the Perf test desired',
                'choices': [
                    {
                        'name': 'Time'

                    },
                    {
                        'name': 'Cachegrind'

                    },
                    {
                        'name': 'GProf'
                    }
                ]
            },
            {
                'type': 'input',
                'name': 'build_cmd',
                'message': 'Make Command (eg. all for "make all" blank for already built):'
            },
            {
                'type': 'input',
                'name': 'outfile',
                'message': 'Name of the output binary file:'
            },
            {
                'type': 'input',
                'name': 'run_input',
                'message': 'Args to be passed to the function\nUse comma sepration between runs\n(eg. arg1 arg2 arg3, arg1 arg2 arg3, ...)\n'
            }
        ]

    def run(self):
        if self.past_questions != None:
            self.answers = PyInquirer.prompt(self.past_questions)
            if self.answers['use_past'] == True:
                config = self.config.get_cfg()['runs']
                for (i, ans) in enumerate(config):
                    if ans == self.answers['past_runs']:
                        break
                self.run = self.config.get_cfg()['runs'][i]
                return
        
        self.answers = PyInquirer.prompt(self.questions)

        run_input = []
        for run in self.answers['run_input'].strip().split(','):
            run_input.append(run.strip())
        print(run_input)
        self.run = {
            'name': self.answers['save_name'],
            'test': self.answers['test'],
            'git_ref': self.answers['git_ref'],
            'cmd': self.answers['build_cmd'],
            'args': run_input,
            'bin': self.answers['outfile']
        }

        if self.answers['save'] == True:
            self.config.add_run(self.run)

    def get_run(self):
        return self.run