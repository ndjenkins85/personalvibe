# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
Interactive sprint executor. Yields every assistant response so the
caller can inspect success/failure and decide to break early.

It loops up to `max_iterations` times, passing previous assistant
output back in as context when needed.
"""
