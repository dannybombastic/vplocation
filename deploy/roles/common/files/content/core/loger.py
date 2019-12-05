import logging




class Loger:

    filename = None
    logger = None
    ft = '%(filename)s | %(levelname)s | %(asctime)s |--------------------|%(message)s'


    def __init__(self, filename,name):
        self.filename = filename

        logging.basicConfig(
            filename=self.filename,
            filemode='a',
            format=self.ft,
            datefmt='%m/%d/%Y %I:%M:%S %p',
        )
        self.logger = logging.getLogger(name)



        print("filename ", filename)





    def log_debug(self, msg):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(msg)


    def log_info(self, msg):
         self.logger.setLevel(logging.INFO)
         self.logger.info(msg)

    def log_warning(self, msg):
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(msg)

    def console_info(self, msg):
        msg_console = self.bcolors.OKGREEN + '| {0: >50} |'.format(msg) + self.bcolors.ENDC
        self.log_info(msg)

    def console_success(self, msg):
        msg_console = self.bcolors.OKBLUE + '| {0: >50} |'.format(msg) + self.bcolors.ENDC
        print(msg_console)
        self.log_info(msg)

    def console_warning(self, msg):
        msg_console = self.bcolors.WARNING + '|{0: >50}|' .format(msg)+ self.bcolors.ENDC
        print(msg_console)
        self.log_warning(msg)


    class bcolors:
          HEADER = '\033[95m'
          OKBLUE = '\033[94m'
          OKGREEN = '\033[92m'
          WARNING = '\033[93m'
          FAIL = '\033[91m'
          ENDC = '\033[0m'
          BOLD = '\033[1m'
          UNDERLINE = '\033[4m'