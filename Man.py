from Person import Person


class Man(Person):
    def __init__(self, simulation, seed, mom=None, dad=None):
        Person.__init__(self, simulation, seed, mom, dad)
        self.random_obj = Random()
        self.random_obj.seed(seed)
        self.sim = simulation

        if mom is None:
            self.height = self.random_obj.random() * 14.5 + 60
            self.weight_natural = self.random_obj.random() + 200 + 90
        else:
            if mom.spouse is not None:
                self.affluence = (mom.spouse.affluence + mom.affluence) / 2 + self.random_obj.random() - 0.5
                self.social = (mom.spouse.social + mom.social) / 2 + self.random_obj.random() - 0.5
            else:
                self.affluence = mom.affluence + self.random_obj.random() - 0.5
                self.social = mom.social + self.random_obj.random() - 0.5
            self.height = (dad.height + (mom.height * 60 / 57)) / 2 + (self.random_obj.random() * 5 - 5)
            self.weight_natural = (dad.weight_natural + (mom.weight_natural * 198 / 170)) / 2 + (self.random_obj.random() * 5 - 5)

        self.weight_current = 90
        self.weight_natural_mod = self.weight_natural

    def __call__(self):
        self.prospects = []
        if self.years < 18:
            self.update()
            return

        if self.spouse is not None:
            self.prospects.append(self.spouse)

        for prospect_i in range(0, ((self.social // 10) * 2)):
            self.prospects.append(self.random_obj.rand_choice(self.sim.women))
        for prospect in self.prospects:
            if prospect.years < 18:
                self.prospects.remove(prospect)
            elif self.calc_smv_alpha < self.smv:
                self.prospects.remove(prospect)
        if self.spouse is not None:
            if self.spouse in self.prospects:
                self.spouse.suitors.append(self)
            else:
                for prospect in self.prospects:
                    self.prospect.suitors.append(self)
        else:
            for prospect in self.prospects:
                self.prospect.suitors.append(self)

        self.update()

    def calc_smv(self, woman):
        if woman.years > self.years:
            des = (1.0 / (2.0 * (woman.years - self.years)))
        else:
            des = (1.0 - (woman.years / self.years) )

        des *= 10.0

        if woman.bmi < 18:
            des *= (woman.bmi / 18.0)
        else:
            des -= ((woman.bmi - 20.0) / 5.0)

        return des

    def calc_smv_alpha(self, woman):
        return self.calc_smv(woman) * woman.attractive

    def calc_smv_beta(self, woman):
        return self.calc_smv_alpha(woman)

    def enter_relationship(self, woman):
        if self.spouse is not None and woman != self.spouse:
            if self.calc_smv_beta(self.spouse) > self.calc_smv_beta(woman):
                return False
            else:
                return True
        elif self.calc_smv_beta(woman) >= self.smv:
            return True

    def update(self):
        self.update_person()
    
    def update_smv(self):
        value = 0.0
        if len(self.sexual_partner_vals) < 6:
            for sexual_partner_val in self.sexual_partner_vals:
                value += sexual_partner_val
            self.smv = value / len(self.sexual_partner_vals)
        else:
            for sexual_partner_val in self.sexual_partner_vals[-5:]:
                value += sexual_partner_val
            self.smv = value / len(self.sexual_partner_vals)
