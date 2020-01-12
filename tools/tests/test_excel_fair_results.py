"""Tests for excel_fair_results.py"""

import os
import pathlib
import subprocess

import matplotlib.animation
import pytest
import tools.excel_fair_results as efr

this_dir = pathlib.Path(__file__).parents[0]


@pytest.mark.slow
def test_animation_file(tmpdir):
    # We use GIF and PIL here to not require CI/CD servers to install ffmpeg for mp4.
    writer = matplotlib.animation.PillowWriter()
    filename = this_dir.joinpath('excel_fair_results_test.xlsx')
    efr.process_ghgs(excelfile=filename, outdir=str(tmpdir), writer=writer, ext='.gif')
    for pds in range(1, 4):
        outfile = tmpdir.join(f"excel_fair_results_test_PDS{pds}.gif")
        assert outfile.size() > 1024

        outfile = tmpdir.join(f"excel_fair_results_test_Temperature_PDS{pds}.csv")
        assert outfile.size() > 1024
        contents = outfile.open().read()
        assert "Baseline" in contents
        assert "2020" in contents

        outfile = tmpdir.join(f"excel_fair_results_test_Concentration_PDS{pds}.csv")
        assert outfile.size() > 1024
        contents = outfile.open().read()
        assert "Total" in contents
        assert "2020" in contents
