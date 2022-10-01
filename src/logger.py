import logging as log

def config_log():
    log.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    log.info('logging configured')