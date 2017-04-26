import os
import logging
import datetime
import errno
now = datetime.datetime.now()

class Log(object):
    def __init__(self,name,remote_addr):
        self.name = name
        # try:
        #     os.mkdir("/var/www/html/antares/antares/web/log/"+self.name+".log")
        # except OSError as exc:
        #     if exc.errno != errno.EEXIST:
        #         raise exc
        #     pass
        if not os.path.exists("/var/www/html/antares/web/log/"+self.name+".log"):
            os.makedirs("/var/www/html/antares/web/log/"+self.name+".log")
        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            hdlr = logging.FileHandler("/var/www/html/antares/web/log/" + self.name + '.log/%s-%s-%s.log' % (now.year, now.month, now.day))
            formatter = logging.Formatter(remote_addr + ' [%(asctime)s] - %(message)s', '%H:%M:%S')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)
    def write(self,message):
        self.logger.info(message)

