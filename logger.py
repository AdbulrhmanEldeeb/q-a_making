import logging

# adding logs to txt file 
def setup_logger(log_file="process_log.txt"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()
