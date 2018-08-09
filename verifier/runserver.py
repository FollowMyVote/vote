

import os
from verifier import app

if __name__ == '__main__':
    HOST = os.getenv('SERVER_HOST', 'localhost')
    PORT = os.getenv('SERVER_PORT', '5555')
    app.run(HOST, PORT)
    
