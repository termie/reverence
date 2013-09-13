"""Cached object envelope classes.

This code is free software; you can redistribute it and/or modify
it under the terms of the BSD license (see the file LICENSE.txt
included with the distribution).

Parts of code inspired by or based on EVE Online, with permission from CCP.
"""
import zlib

from . import blue

#CachedObject = objectCaching.CachedObject

class CachedObject:
  __guid__ = "cachedObject.CachedObject"

  def __setstate_CachedObject(self, state):
    self.version, self.object, self.nodeID, self.shared, self.pickle, self.isCompressed, self.objectID = state

  def __setstate_CachedMethodCallResult(self, state):
    self.details, self.result, self.version = state

  def __setstate__(self, state):
    #print state
    if len(state) == 3:
      return self.__setstate_CachedMethodCallResult(state)
    elif len(state) == 4:
      return self.__setstate_CachedMethodCallResult(state[:3])
    else:
      return self.__setstate_CachedObject(state)


  def GetCachedObject(self):
    return self

  GetObject = GetCachedObject
