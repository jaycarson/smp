from Person import Person


class Woman(object):
    def __init__(self, simulation, conceive, miscarry, ivf, seed, mom=None, dad=None):
        Person.__init__(self, simulation=simulation, seed=seed, mom=mom, dad=dad)

        if mom is None:
            self.height = self.random_obj.random() * 13.0 + 57
            self.weight_natural = self.random_obj.random() + 200 + 90
        else:
            self.attractive = (dad.attractive + mom.attractive) / 2 + self.random_obj.random() - 0.5
            if mom.spouse is not None:
                self.affluence = (mom.spouse.affluence + mom.affluence) / 2 + self.random_obj.random() - 0.5
                self.social = (mom.spouse.social + mom.social) / 2 + self.random_obj.random() - 0.5
            else:
                self.affluence = mom.affluence + self.random_obj.random() - 0.5
                self.social = mom.social + self.random_obj.random() - 0.5
            self.height = (mom.height + (dad.height * 57 / 60)) / 2 + (self.random_obj.random() * 5 - 5)
            self.weight_natural = (mom.weight_natural + (dad.weight_natural * 170 / 198)) / 2 + (self.random_obj.random() * 5 - 5)

        self.father_of_pregnancy = None

        self.weight_current = 90
        self.weight_natural_mod = self.weight_natural
        
        self.months_trying = 0
        self.chance_to_conceive = conceive
        self.chance_to_miscarry_early = miscarry
        self.chance_on_ivf = ivf
        self.chance_to_miscarry_late = 0.015
        self.has_had_still_birth = False
        self.on_ivf = False

        self.miscarriage_risk = 0.0

        self.is_pregnant = False
        self.preg_month = 0
        
    def __call__(self):
        for x in range(len(self.sexual_partners)):
            if x >= 3:
                break
            partner = self.sexual_partners[-x]
            if partner not in self.suitors:
                self.suitors.append(partner)
            
        smvs = []
        for suitor in self.suitors:
            smvs.append(self.calc_smv_alpha(suitor))
        sorted_smvs = sorted(smvs)
        considering = round(self.social)
        if len(sorted_smvs) < considering:
            for suitor in self.suitors:
                if self.calc_smv_alpha(suitor) < self.smv:
                    self.suitors.remove(suitor)
        else:
            cutoff = sorted_smvs[-considering:]
            for suitor in self.suitors:
                if self.calc_smv_alpha(suitor) < cutoff:
                    self.suitors.remove(suitor)
                elif self.calc_smv_alpha(suitor) < self.smv:
                    self.suitors.remove(suitor)
            if self.spouse is not None:
                if self.spouse in self.suitors:
                    self.have_sex(self.spouse)
                else:
                    self.have_sex(self.random_obj.choice(self.suitors))
        self.update()

    def manage_relationship(self, man):
        if self.sexual_history['partners'][man] > 6 and man != self.spouse:
            if man.enter_relationship(self):
                if man.spouse is not None:
                    man.spouse.spouse = None
                    man.spouse.in_relationship = False
                    man.married = False
                    man.spouse.married = False
                self.spouse = man
                man.spouse = self
                self.in_relationship = True
                man.in_relationship = True
                self.spouses.append(man)
                man.spouses.append(self)
        if self.sexual_history['partners'][man] > 12 and man == self.spouse:
            if not self.married:
                if man.enter_relationship(self):
                    self.married = True
                    man.married = True

    def birth(self):
        children = 1

        fraternal_twin_chance = 1.0 / 250.0
        identical_twin_chance = 3.5 / 1000.0

        if self.on_ivf:
            if self.years <= 35:
                fraternal_twin_chance = 0.121
            elif self.years <= 37:
                fraternal_twin_chance = 0.091
            elif self.years <= 40:
                fraternal_twin_chance = 0.053
        else:
            if self.height > 64.0:
                fraternal_twin_chance *= 2.0
            if self.years > 35:
                fraternal_twin_chance *= 4.0
            if self.bmi > 30.0:
                fraternal_twin_chance *= 1.25
            if self.bmi < 18.5:
                fraternal_twin_chance *= 0.75
            if self.carnivore:
                fraternal_twin_chance *= 5.0
            if self.twins_run_in_family:
                fraternal_twin_chance *= 2.5

        if self.random_obj.random() < fraternal_twin_chance:
            children += 1

        count = children

        for twin in range(0, count):
            if self.random_obj.random() < identical_twin_chance:
                children += 1

        count = children

        children_objs = []

        for child in range(0, count):
            if self.random_obj.random() < 0.5:
                child_obj = Woman(sim=self.sim, seed=self.sim.get_seed(), mom=self, dad=self.father_of_pregnancy)
            else:
                child_obj = Man(sim=self.sim, seed=self.sim.get_seed(), mom=self, dad=self.father_of_pregnancy)
            if self.random_obj.random() < self.get_down_syndrom_chance():
                self.children_with_down_syndrom += 1
            if self.random_obj.random() < self.get_still_birth_chance():
                children -= 1
                self.still_births += 1
                self.has_had_still_birth = True
            else:
                children_objs.append(child_obj)
            self.weight_natural_mod += ((self.random_obj.random() * 2.5) + 2.5)

        self.father_of_pregnancy = None
        return children_objs

    def calc_smv(self, man):
        if man.years < self.years:
            des = (1.0 / (2.0 * (self.years - man.years)))
        else:
            des = self.years / man.years

        des *= 10.0

        if man.bmi < 18:
            des *= (man.bmi / 18.0)
        else:
            des -= ((man.bmi - 20.0) / 5.0)

        des *= ((man.height - 3) / self.height)

        return des

    def calc_smv_alpha(self, man):
        return self.calc_smv(man) * man.attractive

    def calc_smv_beta(self, man):
        return self.calc_smv(man) * man.affluence

    def get_down_syndrom_chance(self):
        if self.years < 25:
            return 1.0 / 1200.0
        elif self.years < 35:
            return 1.0 / 350.0
        elif self.years < 40:
            return 1.0 / 100.0
        elif self.years < 45:
            return 1.0 / 30.0
        else:
            return 1.0 / 30.0

    def get_miscarriage_early_chance(self):
        success = 1 - self.chance_to_miscarry_early[self.years]
        mod = -self.miscarriage_risk + 2
        return 1 - success * mod

    def get_miscarriage_late_chance(self):
        return self.chance_to_miscarry_late

    def get_pregnant(self, man):
        if self.is_pregnant:
            if self.preg_month == 2:
                if self.random_obj.random() < self.get_miscarriage_early_chance():
                    self.is_pregnant = False
                    self.miscarriages += 1
                else:
                    self.preg_month += 1
            elif self.preg_month == 6:
                if self.random_obj.random() < self.chance_to_miscarry_late:
                    self.is_pregnant = False
                    self.miscarriages += 1
                else:
                    self.preg_month += 1
            elif self.preg_month == 9:
                self.is_pregnant = False
                self.children += self.birth()
                self.on_ivf = False
            else:
                self.preg_month += 1
        else:
            if self.on_ivf:
                if self.random_obj.random() < self.chance_on_ivf[self.years]:
                    self.is_pregnant = True
                    self.preg_month = 0
                    self.months_trying = 0
                else:
                    self.months_trying += 1
            else:
                if self.years > 12:
                    if self.random_obj.random() < self.chance_to_conceive[self.years]:
                        self.is_pregnant = True
                        self.preg_month = 0
                        self.months_trying = 0
                        self.father_of_pregnancy = man
                else:
                    if self.years > 30:
                        self.months_trying += 1
                        if self.months_trying >= 6 and self.ivf_allowed:
                            self.on_ivf = True

    def get_still_birth_chance(self):
        if self.has_had_still_birth:
            chance = 0.025
        else:
            chance = 0.01

        # Note chances increased by 20% per 5 BMI points starting at 26
        if self.bmi > 26.0:
            chance *= 1.2
        if self.bmi > 31.0:
            chance *= 1.2
        if self.bmi > 36.0:
            chance *= 1.2
        if self.bmi > 41.0:
            chance *= 1.2
        if self.bmi > 46.0:
            chance *= 1.2

        # Note smoking 1-9 cigarettes per day increases chance 9%
        if self.casual_smoker:
            chance *= 1.09

        # Note smoking 10+ cigarettes per day increases chance 52%
        if self.smoker:
            chance *= 1.52

        return chance
    
    def have_sex(self, man)
        self.sexual_partners.append(man)
        man.sexual_partners.append(self)

        self.sexual_partner_vals.append(self.calc_smv_alpha(man))
        man.sexual_partner_vals.append(man.calc_smv_alpha(self))
        
        if self.father_of_pregnancy is None:
            if self.calc_smv_alpha(man) > self.smv:
                self.get_pregnant(man)

        self.add_sexual_partner(man)
        man.add_sexual_partner(self)

        self.manage_relationship(man)

    def update(self):
        self.update_person()
        self.update_smv()
        self.update_risks()

    def update_risks(self):
        if self.bmi < 18.5:
            self.miscarriage_risk = 1.08
        elif self.bmi < 25.0:
            self.miscarriage_risk = 1.0
        elif self.bmi < 30.0:
            self.miscarriage_risk = 1.09
        elif self.bmi < 35.0:
            self.miscarriage_risk = 1.15
        else:
            self.miscarriage_risk = 1.27
    
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
