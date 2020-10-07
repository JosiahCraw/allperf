import yaml

class ConfigParser():
    def __init__(self, run_dir):
        self.dir = run_dir
        try:
            with open('{}/.allperf.yml'.format(run_dir), 'r') as cfg_file:
                self.cfg = yaml.safe_load(cfg_file)
                if self.cfg == None:
                    self.cfg = {'runs': []}
                    self.write_cfg()
        except FileNotFoundError:
            self.cfg = {'runs': []}
            self.write_cfg()
                
    def get_cfg(self):
        return self.cfg

    def set_cfg(self, cfg):
        self.cfg = cfg

    def add_run(self, run):
        self.cfg['runs'].append(run)
        self.write_cfg()

    def write_cfg(self):
        with open('{}/.allperf.yml'.format(self.dir), 'w') as cfg_file:
            yaml.dump(self.cfg, cfg_file, default_flow_style=False, allow_unicode=True)