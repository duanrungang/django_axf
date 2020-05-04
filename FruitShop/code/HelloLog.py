import logging
logger = logging.getLogger('hello')

handler = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.error('你错了')
logger.critical('你真错了')