from click.testing import CliRunner
from som_cam.cli import main


def test_hw_2_json():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "hw_2_json",
            "-i",
            "./som_cam/static/hw_config.json",
            "-o",
            "./som_cam/static/output_test.json",
            "--verbose",
            "debug",
        ],
    )
    assert result.exit_code == 2


def test_json_2_hw():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "json_2_hw",
            "-i",
            "./som_cam/static/hw_config.json",
            "--verbose",
            "debug",
        ],
    )
    assert result.exit_code == 2
