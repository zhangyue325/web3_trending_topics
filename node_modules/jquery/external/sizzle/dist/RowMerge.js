/*!
 *  Merge identical table rows jQuery plugin.
 *  Copyright (C) 2021  Andrew Wagner  github.com/andreww1011
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
 *  USA
 */
var NULL_CELL = new /** @class */ (function () {
    function class_1() {
    }
    class_1.prototype.columnAddress = function () { return 0; };
    class_1.prototype.width = function () { return 0; };
    class_1.prototype.getCell = function () { return null; };
    class_1.prototype.matches = function (other) { return false; };
    return class_1;
}());
var RowMerge = /** @class */ (function () {
    function RowMerge(tableTarget, args) {
        var t = tableTarget.get(0);
        if (!(t instanceof HTMLTableElement)) {
            throw new Error("JQuery target must be a table element.");
        }
        this.origTable = t;
        var exc = args.zeroIndexed ? args.excludedColumns : args.excludedColumns.map(function (n) { return n - 1; });
        this.mergeTable = RowMerge.merge(t, args.matcher, exc);
    }
    RowMerge.merge = function (table, matcher, excludedColumns) {
        var t = table.cloneNode(true);
        var s = t.tBodies;
        for (var i = 0; i < s.length; i++) {
            var section = s.item(i);
            RowMerge.mergeSection(section, matcher, excludedColumns);
        }
        return t;
    };
    RowMerge.mergeSection = function (section, matcher, excludedColumns) {
        var rows = section.rows;
        if (rows.length == 0) {
            return;
        }
        var arr = new Array();
        arr.push(NULL_CELL);
        for (var r = 0; r < rows.length; r++) {
            var row = rows.item(r);
            var cells = RowMerge.createCells(row.cells, matcher);
            if (cells.length == 0) {
                continue;
            }
            var ia = 0;
            var ib = 0;
            var arrNew = new Array();
            var _loop_1 = function () {
                var cellA = arr[ia];
                var cellB = cells[ib];
                var ca = cellA.columnAddress();
                var cb = cellB.columnAddress();
                if (ca > cb) {
                    ib++;
                    arrNew.push(cellB);
                }
                else if (ca < cb) {
                    ia++;
                }
                else {
                    //ca == cb
                    if (excludedColumns.some(function (n) { return ca === n; })) {
                        ia++;
                        ib++;
                        arrNew.push(cellB);
                    }
                    else {
                        var wa = cellA.width();
                        var wb = cellB.width();
                        if (wa != wb) {
                            ia++;
                            ib++;
                            arrNew.push(cellB);
                        }
                        else {
                            //wa == wb
                            if (cellA.matches(cellB)) {
                                arrNew.push(cellA);
                                cellA.getCell().rowSpan++;
                                row.removeChild(cellB.getCell());
                                ia++;
                                ib++;
                            }
                            else {
                                ia++;
                                ib++;
                                arrNew.push(cellB);
                            }
                        }
                    }
                }
            };
            while (ia < arr.length && ib < cells.length) {
                _loop_1();
            }
            for (; ib < cells.length; ib++) {
                var cellB = cells[ib];
                arrNew.push(cellB);
            }
            arr = arrNew;
        }
    };
    RowMerge.createCells = function (cells, matcher) {
        var a = new Array(cells.length);
        for (var i = 0, col = 0; i < cells.length; i++) {
            var c = cells.item(i);
            var width = c.colSpan;
            a[i] = new RowMerge.SingleCell(col, width, c, matcher);
            col += width;
        }
        return a;
    };
    RowMerge.prototype.getMerged = function () {
        return this.mergeTable;
    };
    RowMerge.prototype.getOriginal = function () {
        return this.origTable;
    };
    RowMerge.SingleCell = /** @class */ (function () {
        function class_2(column, width, cell, matcher) {
            this.col = column;
            this.w = width;
            this.cell = cell;
            this.matcher = matcher;
        }
        class_2.prototype.columnAddress = function () { return this.col; };
        class_2.prototype.width = function () { return this.w; };
        class_2.prototype.getCell = function () { return this.cell; };
        class_2.prototype.matches = function (other) { return this.matcher(this.getCell(), other.getCell()); };
        return class_2;
    }());
    return RowMerge;
}());
export default RowMerge;
//# sourceMappingURL=RowMerge.js.map