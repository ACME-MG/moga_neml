"""
    Title:          Progress Visualiser
    Description:    Contains progress visualisation functions
    Author:         Janzen Choi

"""

# Libraries
import time

# Constants
BAR     = "bar"
WAVE    = "wave"
ARROW   = "arrow"
WHEEL   = "wheel"
TIMER   = "timer"
PERCENT = "percent"

# The Visualiser class
class Visualiser:

    # Constructor
    def __init__(self, num_steps, options=[], pretext="", clear=False, newline=True):
        
        # Initialise inputs
        self.num_steps  = num_steps
        self.options    = options
        self.pretext    = pretext
        self.clear      = clear
        self.newline    = newline
        
        # Initialise other
        self.start_time = time.time()
        self.display_string = ""
        
        # First print
        self.curr_step = 1
        self.__print_progress__()

    # Progresses the process
    def progress(self):
        if self.curr_step <= self.num_steps:
            self.__print_progress__() 
        if self.curr_step == self.num_steps and not self.clear and self.newline:
            print("")
        if self.curr_step == self.num_steps and self.clear:
            self.__clear_display__()
        self.curr_step += 1

    # Prematurely ends the process
    def end(self):
        while self.curr_step <= self.num_steps:
            self.progress()

    # Clears the display string
    def __clear_display__(self):
        print("\b" * (len(self.display_string)), end="", flush=True)

    # Prints the progress
    def __print_progress__(self):
        
        # Clear previous visual and apply pretext
        self.__clear_display__()
        self.display_string = f"{self.pretext} " if self.pretext != "" else ""
        
        # Apply Options
        for option in self.options:
            
            # Add progress bar
            if option == BAR:
                self.display_string += f"[{'■' * self.curr_step} {' ' * (self.num_steps - self.curr_step)}] "
                
            # Add progress percentage
            if option == PERCENT:
                self.display_string += f"({round((self.curr_step+1) / self.num_steps * 100, 1)}%) "
            
            # Add time elapsed
            if option == TIMER:
                self.display_string += f"({round(time.time() - self.start_time, 1)}s) "
        
            # Add loading wheel
            if option == WHEEL:
                symbols = "◐◓◑◒"
                self.display_string += f"({symbols[self.curr_step % len(symbols)]} ) "
        
            # Add loading wave
            if option == WAVE:
                symbols = "▁▂▃▄▅▆▇██▇▆▅▄▃▂▁"
                wave = "".join([symbols[(self.curr_step % len(symbols) + i) % len(symbols)] for i in range(4)])
                self.display_string += f"|{wave}| "
        
            # Add an arrow (>--►)
            if option == ARROW:
                pass
        
        # Print out everything
        print(self.display_string, end="", flush=True)
