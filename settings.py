LOG_FILE = '/tmp/predictor_daemon.log' #Where requests will be logged
PREDICTOR_SERVER = "tcp://*:5555" #Port where predictor will run
PREDICTOR_CLIENT = "tcp://localhost:5555"
DB_URL = "mongodb://localhost:12345" #Point it to the db running mongodb instance
DB = "pnr"
COLLECTION = "pnr_change"
