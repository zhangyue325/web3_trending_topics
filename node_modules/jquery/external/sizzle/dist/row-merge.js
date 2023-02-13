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
import $ from 'jquery';
import RowMerge from './RowMerge';
// define the plugin function on the jQuery extension point.
$.fn.rowMerge = function (args) {
    var MATCH_TEXT_ONLY = function (value, other) {
        return value.textContent == other.textContent;
    };
    var target = this;
    // merge the global options with the per-call options.
    args = $.extend({}, $.fn.rowMerge.args, args);
    // factory defaults
    if (typeof args.matcher === 'undefined')
        args.matcher = MATCH_TEXT_ONLY;
    if (typeof args.excludedColumns === 'undefined')
        args.excludedColumns = new Array();
    if (typeof args.zeroIndexed === 'undefined')
        args.zeroIndexed = false;
    var rowMerge = new RowMerge(target, args);
    var methods = {
        merge: function () {
            update(rowMerge.getMerged());
        },
        unmerge: function () {
            update(rowMerge.getOriginal());
        }
    };
    methods.merge();
    return methods;
    function update(table) {
        var t = $(table);
        target.replaceWith(t);
        target = t;
    }
};
// activate plugin by targeting selector
$(function () {
    // factory defaults
    var selector = typeof $.fn.rowMerge.selector === 'undefined' ? 'table.row-merge' : $.fn.rowMerge.selector;
    // target
    var s = $(selector);
    s.each(function (i, e) {
        $(e).rowMerge();
    });
});
// define the plugin's global default selector.
$.fn.rowMerge.selector = undefined;
// define the plugin's global default options.
$.fn.rowMerge.args = {};
//# sourceMappingURL=row-merge.js.map