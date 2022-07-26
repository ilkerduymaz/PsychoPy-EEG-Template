from psychopy import visual
from types import SimpleNamespace

class Trial:
    def __init__(self, exp, win, trig_trlstart=None, trig_trlend=None):
        ### Trial Info ###
        self.trl_type = "Trial"
        
        ### Duration ###
        self.trial_duration = 3 # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate # total number of frames to display the trial for
        
        ### Triggers ###
        self.trig = SimpleNamespace()
        self.trig.trl_start = trig_trlstart
        self.trig.trl_end = trig_trlend
        
        ### Utility ###
        self.record = False # record a video of the trial
        self.skip = False # skip trial
        
        ### Stimulus ###
        self.stim = []
        self.initStim(win)
        
    def initStim(self, win):
        self.cross = visual.TextStim(
            win, text='+', color='red', colorSpace='rgb', pos=(0, 0))
        
        self.text = visual.TextStim(
            win, text=f'This is an example trial.', color='black', colorSpace='rgb', pos=(0, 2))
        
        self.stim.append(self.cross)
        self.stim.append(self.text)

    def updateStim(self, frame=0):
        pass
    
    def writeData(self, trials):
        trials.addData('TrialType', self.trl_type)
    
    def sendTrialTriggers(self, exp, win, frame=0):
        
        if exp.send_triggers:
                       
            if frame == 0 and type(self.trig.trl_start) == int:
                win.callOnFlip(exp.p_port.setData, self.trig.trl_start)
            
            if frame == self.total_frames and type(self.trig.trl_end) == int:
                win.callOnFlip(exp.p_port.setData, self.trig.trl_end)
    
    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.updateStim(frame=frame)
        
        for stim in self.stim:
            stim.draw()
    
    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        
        self.sendTrialTriggers(exp, win, frame=frame)
        self.draw(exp, win, frame=frame, keys=keys, trials=trials)
        
        if frame == self.total_frames-1 or self.skip:
            self.writeData(trials)
