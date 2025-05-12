# Copyright © 2025 by Nick Jenkins. All rights reserved

import re

from personalvibe.run_context import RunContext


def test_run_context_format():
    ctx = RunContext()
    # pattern yyyyMMdd_HHmmss_hex8
    assert re.fullmatch(r"\d{8}_\d{6}_[0-9a-f]{8}", ctx.id)
