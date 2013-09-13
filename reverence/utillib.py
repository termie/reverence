"""Data container classes, text formatting and item type checking functions

Copyright (c) 2003-2012 Jamie "Entity" van den Berge <jamie@hlekkir.com>

This code is free software; you can redistribute it and/or modify
it under the terms of the BSD license (see the file LICENSE.txt
included with the distribution).

Parts of code inspired by or based on EVE Online, with permission from CCP.
"""

class KeyVal:
  __guid__ = "util.KeyVal"
  def __repr__(self):
    return "Anonymous KeyVal: %s" % self.__dict__
