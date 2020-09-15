from copy import deepcopy
from random import randint

from patterns.default import Default
from utils.color import bound_sub, circular_step
from utils.modifier import Modifier
from utils.rgb import RGB


class FireWork(Default):
    """
    Simulate teh firing of multiple fireworks which propagate and vanish
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.fires = Modifier('fires', self.strip_length // 50, minimum=1, maximum=self.strip_length)
        self.loss = Modifier('speed', 25, minimum=1, maximum=80)

        self.step = 0
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(self.fires())}
        self.pattern_name = "FireWork"

        self.modifiers = dict(
            fires=self.fires,
            loss=self.loss
        )

    def empty_center(self):
        if self.randomize_color:
            return dict(color=RGB(random=True), tail=[], step=0)
        else:
            return dict(color=self.color, tail=[], step=0)

    def bound_attrs(self):
        self.fires.values = min(self.fires(), self.strip_length)

    def fill(self):

        self.bound_attrs()

        loss_weight = 1.3
        center_copy = deepcopy(self.centers)

        # for every center in the list
        for a, attr in center_copy.items():

            # get the color and the tail
            color = attr["color"]
            step = attr["step"]
            has_popped = False

            # estimate the center intesity and update
            ci = bound_sub(255, loss_weight * self.loss() * step)
            color.update_single(a=ci)
            self.add_update_pixel(a, color)

            idx = 1

            # if the intensity is more than zero, the the tail is still increasing
            if ci > 0:
                # for 1 to the current step
                for idx in range(idx, step + 1):
                    # get previous and next led
                    p = a - idx
                    n = a + idx
                    p %= self.strip_length
                    n %= self.strip_length

                    # estimate intensity and update
                    # ci is= 255 - the loss times the current step and the index (farther points from center are newer)
                    ci = bound_sub(255, self.loss() * (loss_weight * step + 1 - idx))
                    color.update_single(a=ci)

                    self.add_update_pixel(p, color)
                    self.add_update_pixel(n, color)

                    # update tail
                    attr["tail"].append((p, n, idx))
                # remove duplicates
                attr["tail"] = list(set(attr["tail"]))

            # if the center has faded then the tails need to fade too
            else:
                # if there are some non zero tail
                if len(attr["tail"]) > 0:
                    # for every tail
                    for t in attr["tail"]:
                        # get previous, next and index
                        p = t[0]
                        n = t[1]
                        idx = t[2]
                        # estimate ci as before
                        ci = bound_sub(255, self.loss() * (loss_weight * step + 1 - idx))
                        # update
                        color.update_single(a=ci)
                        self.add_update_pixel(p, color)
                        self.add_update_pixel(n, color)
                        # if ci is zero remove point from tail
                        if ci == 0:
                            attr["tail"].pop(attr["tail"].index(t))

                # if the center is faded and it has no more tail
                else:
                    # remove the center
                    self.centers.pop(a)

                    if len(self.centers) < self.fires():

                        for _ in range(self.fires() - len(self.centers)):

                            # get another one which is not in the center lists already
                            rd = randint(0, self.strip_length - 1)
                            while rd in self.centers.keys():
                                rd = randint(0, self.strip_length - 1)
                            # put random color
                            self.centers[rd] = self.empty_center()
                        has_popped = True

            # is the center has been removed then dont update
            if not has_popped:
                try:
                    self.centers[a]["tail"] = attr["tail"]
                    step = circular_step(step, self.strip_length)
                    self.centers[a]["step"] = step
                except KeyError:
                    pass

        self.update_counter()

    def add_update_pixel(self, idx, new_color):

        self.pixels[idx]['color'] = new_color

    def update_counter(self):
        self.step += 1
        self.step %= self.strip_length
