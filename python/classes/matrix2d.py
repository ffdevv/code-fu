"""
  Class to work with 2d matrix
  Copyright (C) 2022 Federico Fogo
  
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see https://www.gnu.org/licenses/lgpl-3.0.html
"""

class Node:
    def __init__(self, x, y, value, matrix):
        self.x = x
        self.y = y
        self.value = value
        self.matrix = matrix
    def __repr__(self):
        return f"<Node({self.x},{self.y},{self.value})>"
    def __str__(self):
        return str(self.value)

    def neighbours_coords(self):
        return self.node_neighbours_coords(self)

    def neighbours(self):
        return self.matrix.node_neighbours(self)

    def offset(self, x, y):
        return self.matrix.offset_node(self, x, y)

    @staticmethod
    def node_neighbours_coords(node):
        xp, x, xn = node.x - 1, node.x, node.x + 1
        yp, y, yn = node.y - 1, node.y, node.y + 1
        return (
            (xp, yp), (x , yp), (xn, yp),
            (xp, y ),           (xn , y),
            (xp, yn), (x , yn), (xn, yn),
        )

class Matrix2D:
    def __init__(self, matrix, filler = None, fill = None, **kwargs):
        if fill:
            self.fill_matrix(matrix, filler)

        if not self.validate(matrix, **kwargs):
            raise ValueError("Invalid matrix")
        
        self.rn = len(matrix)
        self.cn = len(matrix[0] if self.rn else 0)
        self.nodes = {
            (x, y): Node(x, y, matrix[y][x], self) for x, y in self.iter_coords(matrix)
        }
    
    def _get_node(self, x, y, out = None): return self.nodes.get((x, y), out)
    
    def _offset_node(self, node, x, y, out = None):
        return self._get_node(node.x + x, node.y + y, out = out)
    
    def get_node(self, x, y): 
        if not self.in_boundaries(x, y):
            raise ValueError("x y out of matrix boundaries: {}, {}".format(x, y))
        return self._get_node(x, y)
    
    def offset_node(self, node, x, y):
        x_, y_ = node.x + x, node.y + y
        if not self.in_boundaries(x_, y_):
            raise ValueError("x y out of matrix boundaries: {}, {}".format(x_, y_))
        return self._offset_node(node, x, y)
    
    def node_neighbours(self, node, out = None):
        return [self._get_node(x, y, out = out) for x, y in node.neighbours_coords()]
    
    def iter_nodes(self):
        for y in range(self.rn):
            for x in range(self.cn):
                yield self._get_node(x, y)
    
    def iter_row_nodes(self, y):
        if not self.in_boundaries(0, y):
            raise ValueError("y out of matrix boundaries: {}".format(y))
        for x in range(self.cn):
            yield self._get_node(x, y)

    def iter_column_nodes(self, x):
        if not self.in_boundaries(x, 0):
            raise ValueError("x out of matrix boundaries: {}".format(y))
        for y in range(self.rn):
            yield self._get_node(x, y)

    def next_x(self, x): return (x + 1) % self.cn
    
    def prev_x(self, x): return (x - 1) % self.cn

    def next_y(self, y): return (y + 1) % self.rn

    def prev_y(self, y): return (y - 1) % self.rn
    
    def in_boundaries(self, x, y): return 0 <= x < self.cn and 0 <= y < self.rn
    
    @classmethod
    def validate(cls,
        matrix, 
        rows_number = None, 
        columns_number = None,
        row_validator = None,
        column_validator = None
    ):
        rows_number = rows_number if rows_number is not None else len(matrix)
        columns_number = columns_number if columns_number is not None else max([len(row) for row in matrix])
        row_validator = row_validator if row_validator is not None else lambda row: len(row) == columns_number
        column_validator = column_validator if column_validator is not None else lambda col: len(col) == rows_number
        return (
            all(row_validator(row) for row in cls.iter_rows(matrix)) and 
            all(column_validator(col) for col in cls.iter_columns(matrix))
        )
    
    @staticmethod
    def fill_matrix(matrix, filler):
        if len(matrix) == 0:
            return
        l = max([len(r) for r in matrix])
        for row in matrix:
            if len(row) < l:
                row.extend([filler for _ in range(l - len(row))])
    
    @staticmethod
    def iter_rows(matrix):
        for row in matrix:
            yield row
    
    @staticmethod
    def iter_columns(matrix):
        for column in zip(*matrix):
            yield column
    
    @staticmethod
    def iter_coords(matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                yield x, y
