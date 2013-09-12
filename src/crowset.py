"""Container classes for DBRow/DBRowset

Copyright (c) 2003-2012 Jamie "Entity" van den Berge <jamie@hlekkir.com>

This code is free software; you can redistribute it and/or modify
it under the terms of the BSD license (see the file LICENSE.txt
included with the distribution).

Part of this code is inspired by or based on EVE Online.
Used with permission from CCP.
"""

from . import _blue as blue

def RowsInit(rows, columns):
	header = None
	if type(rows) is types.TupleType:
		header = rows[0]
		rows = rows[1]

	if rows:
		first = rows[0]
		if type(first) != blue.DBRow:
			raise AttributeError('Not DBRow. Initialization requires a non-empty list of DBRows')
		header = first.__header__
	elif header:
		if type(header) != blue.DBRowDescriptor:
			raise AttributeError('expected (DBRowDesciptor, [])')
	if header:
		columns = header.Keys()
	return rows, columns, header


class RowDict(dict):
	__guid__ = 'dbutil.RowDict'
	__passbyvalue__ = 1
	slots = ["columns", "header", "key"]

	def __init__(self, rowList, key, columns = None):
		dict.__init__(self)

		rows, self.columns, self.header = RowsInit(rowList, columns)

		if key not in self.columns:
			raise AttributeError('Indexing key not found in row')

		self.key = key
		for row in rows:
			self[row[key]] = row


	def ReIndex(self, key):
		if key not in self.columns:
			raise AttributeError('Indexing key not found in columns')

		vals = self.values()

		self.clear()

		self.key = key
		for row in vals:
			self[row[self.key]] = row

	def Add(self, row):

		if type(row) != blue.DBRow:
			raise AttributeError('Not DBRow')

		if row.__keys__ != self.columns:
			raise ValueError('Incompatible rows')

		if self.header is None:
			self.header = row.__header__

		self[row[self.key]] = row


class RowList(list):
	__guid__ = 'dbutil.RowList'
	__passbyvalue__ = 1
	slots = ["header", "columns"]

	def __init__(self, rowList, columns = None):
		list.__init__(self)
		rows, self.columns, self.header = RowsInit(rowList, columns)
		self[:] = rows

	def append(self, row):
		if not isinstance(row, blue.DBRow):
			raise ValueError('Not DBRow: %s' % row )

		if row.__header__ is not self.header:
			raise ValueError('Incompatible headers')

		if self.header is None:
			self.header = row.__header__

		list.append(self, row)


class CIndexedRowset(dict):
	__guid__ = "dbutil.CIndexedRowset"
    
	def __init__(self, header, columnName):
		self.header = header
		self.columnName = columnName


class CFilterRowset(dict):
	__guid__ = "dbutil.CFilterRowset"

	def __setstate__(self, data):
		self.__dict__.update(data)  # header and columnName

	def __getstate__(self):
		return {"header": self.header, "columnName": self.columnName}


class CRowset(list):
	__guid__ = "dbutil.CRowset"
	__passbyvalue__	 = 1
	
	def __init__(self, header, rows):
		list.__init__(self, rows)
		self.header = header

	def Sort(self, columnName, caseInsensitive = False):
		ix = self.header.Keys().index(columnName)
		if caseInsensitive:
			self.sort(key=lambda x: x[ix].upper())
		else:			
			self.sort(key=lambda x: x[ix])

	def Index(self, columnName):
		d = CIndexedRowset(self.header, columnName)

		if "." in columnName:		
			keys = columnName.split(".")
			c = 0

			for row in self:
				combinedKey = []
				for key in keys:
					combinedKey.append(row[key])
				d[tuple(combinedKey)] = row
	
			return d
		else:
			pass

	def Filter(self, columnName, indexName=None):
		fr = CFilterRowset(self.header, columnName)

		c = 0
		keyIdx = fr.header.Keys().index(columnName)
		_get = dict.get
		if indexName is None:
			for row in self:
				key = row[keyIdx]
				grp = _get(fr, key)
				if grp is None:
					fr[key] = [row]
				else:
					grp.append(row)
		else:
			key2Idx = fr.header.Keys().index(indexName)
			for row in self:
				key = row[keyIdx]
				key2 = row[key2Idx]
				if key not in fr:
					fr[key] = {}
				fr[key][key2] = row

		return  fr


__all__ = ["RowDict", "RowList", "CIndexedRowset", "CRowset", "CFilterRowset"]

