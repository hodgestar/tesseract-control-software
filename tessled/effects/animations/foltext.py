# -*- coding: utf-8 -*-

""" FolText animation.

    Displays the text "Festival of Light" and scrolls it across the
    tesseract.
"""

import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..engine import Animation
from ...resources import resource_filename


class FolText(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        text = "FESTIVAL OF LIGHT"
        self._x = -8

        font = ImageFont.truetype(resource_filename("vera.ttf"), size=8)
        w, h = font.getsize(text)
        image = Image.new("1", size=(w + 8, 8), color=0)
        draw = ImageDraw.Draw(image)
        draw.text((0, -1), text, font=font, fill=255)
        self._text = np.asarray(image)
        self._text = self._text[::-1, :]
        self._text = self._text * 255

    def render(self, frame):
        if self._x < self._text.shape[1] - 8:
            self._x += 1
        else:
            self._x = -8
        x_min = max(self._x, 0)
        x_max = self._x + 8
        x_diff = x_max - x_min
        frame[:, (8-x_diff):8, 0] = self._text[0:8, x_min:x_max]


class LoremIpsumFieldText(Animation):

    ANIMATION = __name__ + ".lorem"
    ARGS = {
    }

    def post_init(self):
        text = [
                "                    Fusce   sit   amet   condimentum   mauris.   Nulla   non   risus   quis   ante   congue   convallis   vitae   eu   massa.   Donec   tristique   mauris   quis   dolor   posuere   tempus.   Sed   id   sem   a   nibh   varius   gravida.   Donec   tincidunt   ipsum   quis   nibh   dictum,   sed   laoreet   massa   porttitor.   Donec   pulvinar   rhoncus   tristique.   Duis   consequat   tincidunt   condimentum.   Pellentesque   in   sagittis   lorem,   sed   placerat   nisi.   Nunc   a   laoreet   nisl.   Aenean   sagittis   non   odio   et   tincidunt.   Ut   laoreet   dui   ut   dignissim   ultrices.",
                "     Nullam   massa   lectus,   molestie   nec   neque   ac,   tincidunt   volutpat   mi.   Morbi   non   venenatis   est.   In   faucibus   non   tortor   rutrum   viverra.   Proin   et   felis   ac   felis   ultrices   consectetur.   Orci   varius   natoque   penatibus   et   magnis   dis   parturient   montes,   nascetur   ridiculus   mus.   Praesent   hendrerit,   sem   ut   vulputate   posuere,   enim   est   tempus   ipsum,   et   congue   nisl   purus   et   tellus.   Nam   ac   sem   in   augue   finibus   pulvinar   rutrum   at   velit.   Etiam   magna   odio,   sodales   quis   nulla   ut,   aliquet   egestas   mi.   Nunc   eu   neque   rhoncus,   gravida   elit   at,   rutrum   ex.   Cras   quis   malesuada   lacus.   In   non   dapibus   tellus,   ut   ultricies   justo.",
                "               Morbi   sed   lobortis   ex,   quis   aliquam   odio.   Aliquam   mollis   erat   metus.   Vivamus   congue   justo   a   ante   consequat,   viverra   semper   sem   sollicitudin.   Pellentesque   vel   ex   vitae   lacus   tristique   consequat.   Nullam   sem   lacus,   cursus   et   lacus   nec,   tristique   aliquet   diam.   Pellentesque   vitae   massa   risus.   Nullam   pretium   facilisis   ultricies.   Vestibulum   ante   ipsum   primis   in   faucibus   orci   luctus   et   ultrices   posuere   cubilia   Curae;   Vestibulum   vitae   tempor   sem.   Curabitur   sed   feugiat   ante.   Cras   et   volutpat   est.   Morbi   risus   est,   tempus   tempus   enim   vitae,   tempor   maximus   nisl.   Sed   sed   posuere   ante.",
                "Lorem   ipsum   dolor   sit   amet,   consectetur   adipiscing   elit.   Pellentesque   neque   ex,   interdum   ut   ante   tempus,   accumsan   maximus   nisi.   Pellentesque   habitant   morbi   tristique   senectus   et   netus   et   malesuada   fames   ac   turpis   egestas.   Maecenas   ultricies   ante   eros,   non   aliquet   libero   venenatis   in.   Curabitur   cursus   est   velit,   quis   sollicitudin   tellus   vestibulum   at.   Donec   tristique   nisl   ullamcorper   dui   porttitor   rhoncus.   Aliquam   a   efficitur   lectus,   sed   porttitor   ligula.   Maecenas   pharetra   erat   vestibulum,   blandit   leo   sed,   aliquet   justo.   Fusce   sit   amet   vestibulum   orci.   Aliquam   feugiat   nunc   tellus,   a   feugiat   turpis   vestibulum   et.   Nunc   quis   est   tempor,   porttitor   velit   quis,   tempor   nisi.   Phasellus   aliquet   augue   at   neque   laoreet   tempus.   Class   aptent   taciti   sociosqu   ad   litora   torquent   per   conubia   nostra,   per   inceptos   himenaeos.",
                "               Suspendisse   scelerisque   mi   enim,   vitae   molestie   ante   tristique   nec.   Sed   malesuada   erat   varius   faucibus   hendrerit.   Donec   egestas   elit   eu   iaculis   aliquet.   Quisque   volutpat   elementum   neque,   sed   consequat   turpis.   Nunc   eleifend   eros   vel   nisl   faucibus   consectetur.   Duis   fermentum   mauris   aliquam   mi   tempus,   ac   bibendum   nunc   iaculis.   Class   aptent   taciti   sociosqu   ad   litora   torquent   per   conubia   nostra,   per   inceptos   himenaeos.   Maecenas   vitae   tellus   sed   dui   sagittis   blandit.   Donec   porttitor   orci   ac   nisi   lacinia,   ac   efficitur   mi   facilisis.   Mauris   quis   sem   eu   metus   condimentum   efficitur.   Lorem   ipsum   dolor   sit   amet,   consectetur   adipiscing   elit.",
                "                    Mauris   vitae   erat   id   nisl   convallis   posuere.   Proin   tincidunt   eros   quam,   id   lobortis   nisl   gravida   ut.   Phasellus   orci   tortor,   feugiat   vitae   enim   at,   maximus   facilisis   enim.   Integer   eu   felis   commodo,   porta   orci   id,   elementum   est.   Pellentesque   habitant   morbi   tristique   senectus   et   netus   et   malesuada   fames   ac   turpis   egestas.   Suspendisse   in   aliquam   ex.   In   semper   malesuada   risus,   at   vulputate   erat.   Donec   velit   diam,   lobortis   ac   metus   sed,   semper   porttitor   magna.   Donec   at   sem   massa.",
                "     Praesent   rhoncus,   nulla   quis   aliquet   malesuada,   justo   risus   tempus   tellus,   quis   fringilla   lorem   metus   ut   purus.   Donec   accumsan   nunc   eget   porta   egestas.   Aliquam   eu   facilisis   elit,   id   blandit   nisl.   Nulla   facilisi.   Mauris   dapibus   velit   non   neque   pellentesque   egestas.   Integer   dignissim   aliquet   augue   ac   venenatis.   Orci   varius   natoque   penatibus   et   magnis   dis   parturient   montes,   nascetur   ridiculus   mus.   Donec   gravida,   libero   id   pellentesque   convallis,   ante   lectus   efficitur   nunc,   eu   tempor   purus   sapien   vel   dui.   Duis   malesuada   vestibulum   porttitor.   Mauris   ac   ullamcorper   neque.   Suspendisse   eget   pharetra   ipsum.   Mauris   id   diam   interdum,   varius   est   sed,   rhoncus   elit.   Sed   sed   felis   tellus.   Donec   venenatis   pharetra   nibh,   at   tincidunt   arcu   ullamcorper   a.",
                "               Fusce   sodales   ex   et   est   varius,   eget   vehicula   erat   aliquet.   In   sed   est   lacinia   mi   pellentesque   consequat   ac   sit   amet   lacus.   Cras   enim   ipsum,   laoreet   in   massa   vitae,   dignissim   hendrerit   eros.   Nulla   eget   justo   eu   tellus   tincidunt   mattis.   Maecenas   et   dui   quis   ipsum   scelerisque   maximus.   Suspendisse   vulputate   porttitor   malesuada.   Donec   sollicitudin,   lectus   vitae   scelerisque   efficitur,   nulla   enim   consectetur   velit,   eu   malesuada   dui   felis   ac   eros.   In   malesuada   orci   sed   libero   ultricies   suscipit.   Fusce   et   enim   ut   magna   vulputate   faucibus.   Aenean   porta   placerat   quam   sagittis   dapibus.   Suspendisse   ornare   ullamcorper   tortor,   eget   tincidunt   ante   venenatis   id.   Donec   felis   sem,   accumsan   vel   lobortis   in,   interdum   et   diam.   Etiam   rhoncus   mi   eu   lorem   faucibus   sollicitudin.   Nullam   sollicitudin   mi   vel   aliquam   gravida.   Ut   eget   magna   mi."
                ]
        self._x = [-8.0, -8.0, -8.0, -8.0, -8.0, -8.0, -8.0, -8.0]
        self._rate = [max(0.1, random.random()), max(0.1, random.random()),
                      max(0.1, random.random()), 0.5,
                      max(0.1, random.random()), max(0.1, random.random()),
                      max(0.1, random.random()), max(0.1, random.random())]
        self._text = []

        for i in range(len(text)):
            font = ImageFont.truetype(resource_filename("vera.ttf"), size=8)
            w, h = font.getsize(text[i])
            image = Image.new("1", size=(w + 8, 8), color=0)
            draw = ImageDraw.Draw(image)
            draw.text((0, -1), text[i], font=font, fill=255)
            _text = np.asarray(image)
            _text = _text[::-1, :]
            _text = _text * 255
            self._text.append(_text)

    def render(self, frame):
        for i in range(len(self._text)):
            if self._x[i] < self._text[i].shape[1] - 8:
                self._x[i] += self._rate[i]
            else:
                self._x[i] = -8
            x_min = max(int(self._x[i]), 0)
            x_max = int(self._x[i]) + 8
            x_diff = x_max - x_min
            frame[:, (8-x_diff):8, i] = self._text[i][0:8, x_min:x_max]
