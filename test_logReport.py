import sys
from unittest.mock import patch
from datetime import datetime 
import logReport
import pytest
import tempfile
import json
from logReport import process_logs

# тест параметров
def test_parse_args():
    test_args = [
        'logReport',                  
        '--file', 'example1.log', 'example2.log', 'example3.log',
        '--report', 'average',
        '--date', '2025-22-06'
    ]
    with patch('sys.argv', test_args):
        args = logReport.parse_args()
        assert args.file == ['example1.log', 'example2.log', 'example3.log']
        assert args.report == 'average'
        assert args.date == '2025-22-06'

# тест формата даты
def test_date_format():
    """
    Утверждает, что данная строка даты соответствует указанному формату.
    Raises:
        AssertionError: Если строка даты не соответствует формату.
    """
    test_args = [
        'logReport',                  
        '--file', 'example1.log', 'example2.log', 'example3.log',
        '--report', 'average',
        '--date', '2025-22-06'
    ]
    with patch('sys.argv', test_args):
        args = logReport.parse_args()
    try:
        assert datetime.strptime(args.date, "%Y-%d-%m")
    except ValueError:
        raise AssertionError(f"Строка даты'{args.date}' не соответствует формату '{"%Y-%d-%m"}'")

# образцы логов
sample_logs = [
    {"@timestamp": "2025-07-26T10:00:00Z", "url": "/api/context/...", "response_time": 0.1},
    {"@timestamp": "2025-07-26T11:00:00Z", "url": "/api/context/...", "response_time": 0.3},
    {"@timestamp": "2025-07-26T12:00:00Z", "url": "/api/users/...", "response_time": 0.5}
]

# устанавливает поддельный файл логов для сохранения образцов логов
@pytest.fixture
def temp_log_file():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        for entry in sample_logs:
            f.write(json.dumps(entry) + "\n")
        yield f.name

# тест ввода данных без логи
def test_process_logs_wrong_date(temp_log_file):
    """
    Утверждает, что логы не возвращаются, если указана несуществующая дата
    """
    result = process_logs([temp_log_file], date_filter="2025-25-07")
    assert result == []
