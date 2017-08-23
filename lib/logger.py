import os
import logging

def start_logging():
    # inicializar logging
    logging.basicConfig(filename='logs/all.log', level=logging.DEBUG)

    logging_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt=TIME_FORMAT)

    logger = logging.getLogger('class_logger')
    logger.setLevel(logging.DEBUG)


    all_log = logging.FileHandler('logs/sansanobot.log')
    all_log.setLevel(logging.DEBUG)
    all_log.setFormatter(logging_formatter)
    logger.addHandler(all_log)

    # historial log
    historial_formatter = logging.Formatter(
            "%(asctime)s - %(message)s",
            datefmt=TIME_FORMAT)

    historial_log = logging.FileHandler('logs/historial.log')
    historial_log.setLevel(logging.INFO)

    #in this case, we need the info log, so I created a class called FilterOne
    historial_log.addFilter(FilterOne(logging.INFO))
    historial_log.setFormatter(historial_formatter)
    logger.addHandler(historial_log)

    # stream log
    stream_log = logging.StreamHandler()
    stream_log.setLevel(logging.INFO)
    stream_log.addFilter(FilterOne(logging.INFO))
    stream_log.setFormatter(historial_formatter)
    logger.addHandler(stream_log)

    return logger
