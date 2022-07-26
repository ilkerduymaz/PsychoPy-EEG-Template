from trial import Trial
from trialbreak import TrialBreak
from blockbreak import BlockBreak
from fixation import Fixation
from intro import Intro
from outro import Outro
from psychopy import monitors, parallel
from random import shuffle
from itertools import chain
import copy
import time

class Experiment:
    """ 
        Class for defining experiment parameters like conditions, repetitions, and trial durations.         
    """
    def __init__(self):
        ### Screen ###
        self.screen_res = (1920, 1080) #screen resolution
        self.refresh_rate = 60 #screen refresh rate
        self.screen_distance_mm = 765 # participant's distance to the screen
        self.screen_width_mm = 545 # width of the experiment monitor
        self.monitor = monitors.Monitor("ExpMonitor", width=self.screen_width_mm, distance=self.screen_distance_mm) #monitor profile in Monitor Center
        self.fullscreen = True
        self.background_color = [0, 0, 0]
               
        # Block parameters
        self.total_blocks = 3 # number of blocks
        self.trial_per_block = 2
        self.current_block = 1
        
        ### Debugging Options ###
        self.autopilot = False
        self.send_triggers = False # Send triggers via the parallel port?
        self.distributed_ver = True # Experiment will be run on different computers?
                
        ### Utility ###
        self.tStarted = time.time()
        self.p_port = parallel.ParallelPort(address='0x0378')
    
    def initTrials(self, win):
        self.fixation = Fixation(self, win, duration=1)
        self.trial_break = TrialBreak(self, win)
        self.before_trials = [self.fixation]
        self.after_trials = [self.trial_break]
        
        self.trials = [
            {"cond_trl": Trial(self, win), "nreps": self.trial_per_block}
        ]
        
        block = []
        for cond in self.trials:
            trial_group = [self.before_trials, [cond["cond_trl"]], self.after_trials]
            trial_group = list(chain(*trial_group))
            cond_group = [copy.copy(y) for x in range(cond["nreps"]) for y in [trial_group]]
            block.extend(cond_group)
            
        trial_sequence = []
        blockbreak = BlockBreak(self, win)
        intro = Intro(self, win)
        trial_sequence.append(intro)
        for ind in range(self.total_blocks):
            shuffle(block)
            trial_sequence.extend(list(chain(*block)))
            if ind < self.total_blocks-1:
                trial_sequence.append(blockbreak)
        
        outro = Outro(self, win)
        trial_sequence.append(outro)
        self.trial_sequence = trial_sequence