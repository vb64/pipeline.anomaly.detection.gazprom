python -m flake8 pipeline_anomaly_detection_gazprom
python -m flake8 tests/test
python -m pydocstyle pipeline_anomaly_detection_gazprom
python -m pydocstyle --match='.*\.py' tests/test
python -m pylint --rcfile .pylintrc2 pipeline_anomaly_detection_gazprom
python -m pylint --rcfile .pylintrc2 tests/test
pytest --cov=pipeline_anomaly_detection_gazprom --cov-report term:skip-covered --durations=5 tests
