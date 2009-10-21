# -*- coding: utf-8 -*-
# Copyright (c) 2008-2009, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    This module is a direct C -> Python port of the keysyms module from
    xcb-util which can be found here: http://cgit.freedesktop.org/xcb/util

    xcb-keysyms license::

        Copyright © 2008 Ian Osgood <iano@quirkster.com>
        Copyright © 2008 Jamey Sharp <jamey@minilop.net>
        Copyright © 2008 Josh Triplett <josh@freedesktop.org>
        Copyright © 2008 Ulrich Eckhardt <doomster@knuut.de>

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without
        restriction, including without limitation the rights to use, copy,
        modify, merge, publish, distribute, sublicense, and/or sell copies
        of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
        CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
        WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

        Except as contained in this notice, the names of the authors or
        their institutions shall not be used in advertising or otherwise to
        promote the sale, use or other dealings in this Software without
        prior written authorization from the authors.

    .. data:: X_KEYS

        list of X key names
"""

from . import keysymdef
from .util import cached_property

NO_SYMBOL = 0

def convert_case(sym):
    """
        return (lower, upper) for internal use.

        :note: direct port of
               http://cgit.freedesktop.org/xcb/util/tree/keysyms/keysyms.c#n361
    """
    lower = sym
    upper = sym

    enc = sym >> 8

    if enc == 0: # latin1
        if ((sym >= keysymdef.keysyms["A"]) and (sym <= keysymdef.keysyms["Z"])):
            lower += (keysymdef.keysyms["a"] - keysymdef.keysyms["A"])
        elif ((sym >= keysymdef.keysyms["a"]) and (sym <= keysymdef.keysyms["z"])):
            upper -= (keysymdef.keysyms["a"] - keysymdef.keysyms["A"])
        elif ((sym >= keysymdef.keysyms["Agrave"])
                and (sym <= keysymdef.keysyms["Odiaeresis"])):
            lower += (keysymdef.keysyms["agrave"] - keysymdef.keysyms["Agrave"])
        elif ((sym >= keysymdef.keysyms["agrave"])
                and (sym <= keysymdef.keysyms["odiaeresis"])):
            upper -= (keysymdef.keysyms["agrave"] - keysymdef.keysyms["Agrave"])
        elif ((sym >= keysymdef.keysyms["Ooblique"]) and (sym <= keysymdef.keysyms["Thorn"])):
            lower += (keysymdef.keysyms["oslash"] - keysymdef.keysyms["Ooblique"])
        elif ((sym >= keysymdef.keysyms["oslash"]) and (sym <= keysymdef.keysyms["thorn"])):
            upper -= (keysymdef.keysyms["oslash"] - keysymdef.keysyms["Ooblique"])
    elif enc == 1: # latin2
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym == keysymdef.keysyms["Aogonek"]):
            lower = keysymdef.keysyms["aogonek"]
        elif (sym >= keysymdef.keysyms["Lstroke"] and sym <= keysymdef.keysyms["Sacute"]):
            lower += (keysymdef.keysyms["lstroke"] - keysymdef.keysyms["Lstroke"])
        elif (sym >= keysymdef.keysyms["Scaron"] and sym <= keysymdef.keysyms["Zacute"]):
            lower += (keysymdef.keysyms["scaron"] - keysymdef.keysyms["Scaron"])
        elif (sym >= keysymdef.keysyms["Zcaron"] and sym <= keysymdef.keysyms["Zabovedot"]):
            lower += (keysymdef.keysyms["zcaron"] - keysymdef.keysyms["Zcaron"])
        elif (sym == keysymdef.keysyms["aogonek"]):
            upper = keysymdef.keysyms["Aogonek"]
        elif (sym >= keysymdef.keysyms["lstroke"] and sym <= keysymdef.keysyms["sacute"]):
            upper -= (keysymdef.keysyms["lstroke"] - keysymdef.keysyms["Lstroke"])
        elif (sym >= keysymdef.keysyms["scaron"] and sym <= keysymdef.keysyms["zacute"]):
            upper -= (keysymdef.keysyms["scaron"] - keysymdef.keysyms["Scaron"])
        elif (sym >= keysymdef.keysyms["zcaron"] and sym <= keysymdef.keysyms["zabovedot"]):
            upper -= (keysymdef.keysyms["zcaron"] - keysymdef.keysyms["Zcaron"])
        elif (sym >= keysymdef.keysyms["Racute"] and sym <= keysymdef.keysyms["Tcedilla"]):
            lower += (keysymdef.keysyms["racute"] - keysymdef.keysyms["Racute"])
        elif (sym >= keysymdef.keysyms["racute"] and sym <= keysymdef.keysyms["tcedilla"]):
            upper -= (keysymdef.keysyms["racute"] - keysymdef.keysyms["Racute"])
    elif enc == 2: # latin3
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.keysyms["Hstroke"] and sym <= keysymdef.keysyms["Hcircumflex"]):
            lower += (keysymdef.keysyms["hstroke"] - keysymdef.keysyms["Hstroke"])
        elif (sym >= keysymdef.keysyms["Gbreve"] and sym <= keysymdef.keysyms["Jcircumflex"]):
            lower += (keysymdef.keysyms["gbreve"] - keysymdef.keysyms["Gbreve"])
        elif (sym >= keysymdef.keysyms["hstroke"] and sym <= keysymdef.keysyms["hcircumflex"]):
            upper -= (keysymdef.keysyms["hstroke"] - keysymdef.keysyms["Hstroke"])
        elif (sym >= keysymdef.keysyms["gbreve"] and sym <= keysymdef.keysyms["jcircumflex"]):
            upper -= (keysymdef.keysyms["gbreve"] - keysymdef.keysyms["Gbreve"])
        elif (sym >= keysymdef.keysyms["Cabovedot"]
                and sym <= keysymdef.keysyms["Scircumflex"]):
            lower += (keysymdef.keysyms["cabovedot"] - keysymdef.keysyms["Cabovedot"])
        elif (sym >= keysymdef.keysyms["cabovedot"]
                and sym <= keysymdef.keysyms["scircumflex"]):
            upper -= (keysymdef.keysyms["cabovedot"] - keysymdef.keysyms["Cabovedot"])
    elif enc == 3: # latin4
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.keysyms["Rcedilla"] and sym <= keysymdef.keysyms["Tslash"]):
            lower += (keysymdef.keysyms["rcedilla"] - keysymdef.keysyms["Rcedilla"])
        elif (sym >= keysymdef.keysyms["rcedilla"] and sym <= keysymdef.keysyms["tslash"]):
            upper -= (keysymdef.keysyms["rcedilla"] - keysymdef.keysyms["Rcedilla"])
        elif (sym == keysymdef.keysyms["ENG"]):
            lower = keysymdef.keysyms["eng"]
        elif (sym == keysymdef.keysyms["eng"]):
            upper = keysymdef.keysyms["ENG"]
        elif (sym >= keysymdef.keysyms["Amacron"] and sym <= keysymdef.keysyms["Umacron"]):
            lower += (keysymdef.keysyms["amacron"] - keysymdef.keysyms["Amacron"])
        elif (sym >= keysymdef.keysyms["amacron"] and sym <= keysymdef.keysyms["umacron"]):
            upper -= (keysymdef.keysyms["amacron"] - keysymdef.keysyms["Amacron"])
    elif enc == 6: # cyrillic
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.keysyms["Serbian_DJE"]
                and sym <= keysymdef.keysyms["Serbian_DZE"]):
            lower -= (keysymdef.keysyms["Serbian_DJE"] - keysymdef.keysyms["Serbian_dje"])
        elif (sym >= keysymdef.keysyms["Serbian_dje"]
                and sym <= keysymdef.keysyms["Serbian_dze"]):
            upper += (keysymdef.keysyms["Serbian_DJE"] - keysymdef.keysyms["Serbian_dje"])
        elif (sym >= keysymdef.keysyms["Cyrillic_YU"]
                and sym <= keysymdef.keysyms["Cyrillic_HARDSIGN"]):
            lower -= (keysymdef.keysyms["Cyrillic_YU"] - keysymdef.keysyms["Cyrillic_yu"])
        elif (sym >= keysymdef.keysyms["Cyrillic_yu"]
                and sym <= keysymdef.keysyms["Cyrillic_hardsign"]):
            upper += (keysymdef.keysyms["Cyrillic_YU"] - keysymdef.keysyms["Cyrillic_yu"])
    elif enc == 7: # greek
        if (sym >= keysymdef.keysyms["Greek_ALPHAaccent"]
                and sym <= keysymdef.keysyms["Greek_OMEGAaccent"]):
            lower += (keysymdef.keysyms["Greek_alphaaccent"] -
                    keysymdef.keysyms["Greek_ALPHAaccent"])
        elif (sym >= keysymdef.keysyms["Greek_alphaaccent"]
                and sym <= keysymdef.keysyms["Greek_omegaaccent"] and
            sym != keysymdef.keysyms["Greek_iotaaccentdieresis"] and
            sym != keysymdef.keysyms["Greek_upsilonaccentdieresis"]):
            upper -= (keysymdef.keysyms["Greek_alphaaccent"] -
                    keysymdef.keysyms["Greek_ALPHAaccent"])
        elif (sym >= keysymdef.keysyms["Greek_ALPHA"]
                and sym <= keysymdef.keysyms["Greek_OMEGA"]):
            lower += (keysymdef.keysyms["Greek_alpha"] - keysymdef.keysyms["Greek_ALPHA"])
        elif (sym >= keysymdef.keysyms["Greek_alpha"]
                and sym <= keysymdef.keysyms["Greek_omega"] and
                sym != keysymdef.keysyms["Greek_finalsmallsigma"]):
            upper -= (keysymdef.keysyms["Greek_alpha"] - keysymdef.keysyms["Greek_ALPHA"])
    elif enc == 0x14: # armenian
        if (sym >= keysymdef.keysyms["Armenian_AYB"]
                and sym <= keysymdef.keysyms["Armenian_fe"]):
            lower = sym | 1
            upper = sym & ~1
    return lower, upper

class Keysyms(object):
    """
        a simple helper for keycodes and keysyms.
    """
    def __init__(self, conn):
        """
            :type conn: :class:`ooxcb.conn.Connection`
        """
        self.conn = conn

    @cached_property
    def _cookie(self):
        min_keycode = self.conn.get_setup().min_keycode
        max_keycode = self.conn.get_setup().max_keycode
        return self.conn.core.GetKeyboardMapping(
            min_keycode,
            max_keycode - min_keycode + 1)

    @cached_property
    def _reply(self):
        return self._cookie.reply()

    def get_keycode(self, keysym):
        """
            return the corresponding keycode for *keysym* or None.
        """
        for j in xrange(self._reply.keysyms_per_keycode):
            for keycode in xrange(self.conn.get_setup().min_keycode,
                    self.conn.get_setup().max_keycode + 1):

                if self.get_keysym(keycode, j) == keysym:
                    return keycode
        return None

    def get_keysym(self, keycode, col):
        """
            return the corresponding keysym for *keycode* in column
            *col*.

            :todo: no error checking for now :)
        """
        keysyms = self._reply.keysyms
        min_keycode = self.conn.get_setup().min_keycode
        max_keycode = self.conn.get_setup().max_keycode
        per = self._reply.keysyms_per_keycode

        #ptr = (keycode - min_keycode) * per
        keysyms = keysyms[(keycode - min_keycode) * per:]
        # TODO: error checking
        if col < 4:
            if col > 1:
                while (per > 2 and keysyms[per - 1] == NO_SYMBOL):
                    per -= 1
                if per < 3:
                    col -= 2
            if (per <= (col|1) or keysyms[col | 1] == NO_SYMBOL):
                lsym, usym = convert_case(keysyms[col & ~1])
                if not col & 1:
                    return lsym
                elif lsym == usym:
                    return 0
                else:
                    return usym
        return keysyms[col]

X_KEYS = ['Home', 'Left', 'Up', 'Right', 'Down', 'Page_Up',
          'Page_Down', 'End', 'Begin', 'BackSpace',
          'Return', 'Escape', 'KP_Enter'] + \
         ['F%d' % i for i in range(1, 36)]

def keysym_to_str(keysym):
    """
        convert a keysym to its equivalent character or
        key description and return it.
        Returns an empty for an unknown keysym.
        That's just a shortcut for :mod:`ooxcb.keysymdef`.
    """
    return keysymdef.names.get(keysym, '')

class ConversionError(Exception):
    pass

def keysym_to_char(keysym):
    """
        try to convert *keysym* (an `int`) to a character and return it as
        an unicode string.
        If it couldn't be converted or *keysym* is NoSymbol / VoidSymbol,
        a :class:`ConversionError` is raised.
        The approach is described in `http://www.cl.cam.ac.uk/~mgk25/ucs/X11.keysyms.pdf`.
        It is able to convert latin-1, unicode and legacy keysyms. Special,
        function and vendor keysyms will raise a :class:`ConversionError`.
    """
    # special keysyms
    if keysym in (0, 0x00ffffff):
        raise ConversionError("%d is a special keysym" % keysym)
    # latin-1 keysyms
    elif (0x0020 <= keysym <= 0x007e or 0x00a0 <= keysym <= 0x00ff):
        return unichr(keysym)
    # unicode keysyms
    elif (0x01000100 <= keysym <= 0x0110ffff):
        return unichr(keysym - 0x01000000)
    # legacy keysyms
    elif keysym in keysymdef.legacy_keysyms:
        return unichr(keysymdef.legacy_keysyms[keysym])
    # dunno!
    else:
        raise ConversionError("Unsupported keysym category or legacy keysym: %d" % keysym)

