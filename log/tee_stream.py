class TeeStream:
    def __init__(self, original_stream, log_callback):
        self.original_stream = original_stream
        self.log_callback = log_callback

    def write(self, message):
        self.original_stream.write(message)
        self.original_stream.flush()
        if message.strip():  # skip empty lines
            self.log_callback(message)

    def flush(self):
        self.original_stream.flush()
