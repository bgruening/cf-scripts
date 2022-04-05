import pytest
from conda_forge_tick.migrators.mpi_pin_run_as_build import _parse_cbc_mpi


@pytest.mark.parametrize(
    "lines,new_lines",
    [
        (
            [],
            [],
        ),
        (
            [
                "pin_run_as_build:",
            ],
            [],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                "  openmpi:",
                "",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "",
                "",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                " #dss",
                "  openmpi:",
                "",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "",
                " #dss",
                "",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  mpich:",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                "  flarg:",
                "    max_pin: x.x",
                "  mpich:",
                "    # dfjaskjs;",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                "  flarg:",
                "    max_pin: x.x",
                "    # dfjaskjs;",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                "  flarg:",
                "    max_pin: x.x",
                "  mpich:",
                "  # dfjaskjs;",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "",
                "  flarg:",
                "    max_pin: x.x",
                "  # dfjaskjs;",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  mpich:",
                "    max_pin: x.x",
                "  flarg:",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  flarg:",
                "    max_pin: x.x",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  openmpi:",
                "    max_pin: x.x",
                "  flarg:",
                "    max_pin: x.x",
                "  mpich:",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  flarg:",
                "    max_pin: x.x",
            ],
        ),
        (
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  mpich:",
                "    max_pin: x.x",
                "  openmpi:",
                "    max_pin: x.x",
                "  flarg:",
                "    max_pin: x.x",
            ],
            [
                "blah: blarg",
                "blah:",
                "  - ghghg",
                "  - ghghg",
                "pin_run_as_build:",
                "  flarg:",
                "    max_pin: x.x",
            ],
        ),
    ],
)
def test_parse_cbc_mpi(lines, new_lines):
    _new_lines = _parse_cbc_mpi(lines)
    print("".join(ln + "\n" for ln in _new_lines))

    assert not any("mpich" in ln for ln in _new_lines)
    assert not any("openmpi" in ln for ln in _new_lines)
    assert _new_lines == new_lines
