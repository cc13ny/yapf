# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for yapf.line_joiner."""

import textwrap
import unittest

from yapf.yapflib import comment_splicer
from yapf.yapflib import line_joiner
from yapf.yapflib import pytree_unwrapper
from yapf.yapflib import pytree_utils


class LineJoinerTest(unittest.TestCase):

  def _ParseAndUnwrap(self, code):
    """Produces unwrapped lines from the given code.

    Parses the code into a tree, performs comment splicing and runs the
    unwrapper.

    Arguments:
      code: code to parse as a string

    Returns:
      List of unwrapped lines.
    """
    tree = pytree_utils.ParseCodeToTree(code)
    comment_splicer.SpliceComments(tree)
    return pytree_unwrapper.UnwrapPyTree(tree)

  def _CheckLineJoining(self, code, join_lines):
    """Check that the given UnwrappedLines are joined as expected.

    Arguments:
      code: The code to check to see if we can join it.
      join_lines: True if we expect the lines to be joined.
    """
    uwlines = self._ParseAndUnwrap(code)
    self.assertEqual(line_joiner.CanMergeMultipleLines(uwlines),
                     join_lines)

  def testSimpleSingleLineStatement(self):
    code = textwrap.dedent(u"""\
        if isinstance(a, int): continue
        """)
    self._CheckLineJoining(code, join_lines=True)

  def testSimpleMultipleLineStatement(self):
    code = textwrap.dedent(u"""\
        if isinstance(b, int):
            continue
        """)
    self._CheckLineJoining(code, join_lines=False)

  def testSimpleMultipleLineComplexStatement(self):
    code = textwrap.dedent(u"""\
        if isinstance(c, int):
            while True:
                continue
        """)
    self._CheckLineJoining(code, join_lines=False)

  def testSimpleMultipleLineStatementWithComment(self):
    code = textwrap.dedent(u"""\
        if isinstance(d, int): continue  # We're pleased that d's an int.
        """)
    self._CheckLineJoining(code, join_lines=True)

  def testSimpleMultipleLineStatementWithLargeIndent(self):
    code = textwrap.dedent(u"""\
        if isinstance(e, int):    continue
        """)
    self._CheckLineJoining(code, join_lines=True)


def suite():
  result = unittest.TestSuite()
  result.addTests(unittest.makeSuite(LineJoinerTest))
  return result


if __name__ == '__main__':
  unittest.main()