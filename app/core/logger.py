import logging


def get_logger(name: str = "cross_asset_intel") -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if reload happens
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger