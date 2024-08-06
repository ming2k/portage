# Copyright 2013-2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

import os as _os

from portage import _encodings, _unicode_encode
from portage.util import apply_stat_permissions
from portage.util.file_copy import copyfile
from portage.util.futures import asyncio
from portage.util.futures.executor.fork import ForkExecutor
from portage.util._async.AsyncTaskFuture import AsyncTaskFuture


class FileCopier(AsyncTaskFuture):
    """
    Asynchronously copy a file.
    """

    __slots__ = ("src_path", "dest_path")

    def _start(self):
        self.future = asyncio.ensure_future(
            self.scheduler.run_in_executor(
                ForkExecutor(loop=self.scheduler),
                self._target,
                self.src_path,
                self.dest_path,
            )
        )
        super()._start()

    @staticmethod
    def _target(src_path, dest_path):
        src_path = _unicode_encode(src_path, encoding=_encodings["fs"], errors="strict")
        dest_path = _unicode_encode(
            dest_path, encoding=_encodings["fs"], errors="strict"
        )
        copyfile(src_path, dest_path)
        apply_stat_permissions(dest_path, _os.stat(src_path))
