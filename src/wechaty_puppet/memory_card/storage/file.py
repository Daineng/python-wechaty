"""doc"""
from __future__ import annotations
import os
from ..types import MemoryCardPayload
from .backend import StorageBackend
from .backend_config import (
    StorageBackendOptions,
    StorageFileOptions
)

import logging
import json
import re

log = logging.getLogger("file")


class StorageFile(StorageBackend):
    absFileName: str = None

    def __init__(self, name: str, options: StorageBackendOptions):
        log.info('StorageFile', 'constructor(%s, ...)' % name)
        options.type = 'file'
        super().__init__(name, options)

        self.absFileName = self.name if os.path.isabs(self.name) else os.path.abspath(self.name)

        if not re.match(r'\.memory-card\.json$', self.absFileName):
            self.absFileName += '.memory-card.json'

    def toString(self) -> str:
        text = ''.join([self.name, '<', self.absFileName, '>'])
        return text

    async def load(self) -> MemoryCardPayload:
        log.info('StorageFile', 'load() from %s' % self.absFileName)

        if not os.path.exists(self.absFileName):
            log.info('MemoryCard', 'load() file not exist, NOOP')
            return {}
        # TODO
        """
         const buffer = await new Promise<Buffer>((resolve, reject) => fs.readFile(this.absFileName, (err, buf) => {
          if (err) {
            reject(err)
          } else {
            resolve(buf)
          }
        }))
        """
        buffer: str = ""
        text = str(buffer)

        payload: MemoryCardPayload = {}

        try:
            payload = json.loads(text)
        except Exception as e:
            log.error('MemoryCard', 'load() exception: %s', e)

        return payload

    async def save(self, payload: MemoryCardPayload) -> None:
        log.info('StorageFile', 'save() to %s' % self.absFileName)
        text = json.dumps(payload)

        # TODO
        """
        await new Promise<void>((resolve, reject) => {
          fs.writeFile(
            this.absFileName,
            text,
            err => err ? reject(err) : resolve(),
          )
        })
        """
    async def destroy(self) -> None:
        log.info('StorageFile', 'destroy()')
        if os.path.exists(self.absFileName):
            os.unlink(self.absFileName)
