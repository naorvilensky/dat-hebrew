import sys
import tkinter as tk
from file_processor_gui import FileProcessorApp
from log.tee_stream import TeeStream

if __name__ == '__main__':
    root = tk.Tk()
    app = FileProcessorApp(root)
    sys.stdout = TeeStream(sys.__stdout__, app.log)
    sys.stderr = TeeStream(sys.__stderr__, app.log)

    root.mainloop()
