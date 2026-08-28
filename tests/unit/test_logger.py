from src.utils.logger import get_logger


def test_logger_creation():
    logger = get_logger("test")

    assert logger.name == "test"
    assert logger.level == 20
    assert len(logger.handlers) == 1


def test_logger_emits_message(capsys):
    logger = get_logger("telemetry")

    logger.info("Processing vehicle EV001")

    captured = capsys.readouterr()

    assert "Processing vehicle EV001" in captured.out
