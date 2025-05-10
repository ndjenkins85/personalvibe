At this stage, a large amount of project material and templated assets have been created, as well as a chunking strategy.

The challenge is that to generate all required technical code assets of the project would likely exceed the output capabilities of a large language model

Use a maximum of 20,000 output characters to deliver on the output chunk.

Reminder: ONLY GENERATE code relating to the mentioned sprint

Your response should be an executable python file with the following characteristics
- Will touch/mkdir for any new files (however, reuse existing files as much as possible)
- Write code text to the files (patch existing code as required)
- Print further directions and context to the command line

Assume that you are being run from an unknown folder within the codebase - use the following code to find the root repo path
from personalvibe import vibe_utils
REPO = vibe_utils.get_base_path()
