from random import Random


class Person(object):
    def __init__(self, simulation, seed, mom=None, dad=None):
        self.random_obj = Random()
        self.random_obj.seed(seed)
        self.sim = simulation
    
        if mom is None:
            self.attractive = self.random_obj.random() * 10
            self.affluence = self.random_obj.random() * 10
            self.social = self.random_obj.random() * 10
            self.carnivore = self.random_obj.choice([True, False])
            self.smoker = self.random_obj.choice([True, False])
            self.twins_run_in_family = self.random_obj.choice([True, False])
            self.mother = None
            self.father = None
            self.father_biological = None
        else:
            self.attractive = (dad.attractive + mom.attractive) / 2 + self.random_obj.random() - 0.5
            self.carnivore = self.random_obj.choice([mom.carnivore, dad.carnivore])
            self.smoker = self.random_obj.choice([mom.smoker, dad.smoker])
            self.twins_run_in_family = self.random_obj.choice([mom.twins_run_in_family, dad.twins_run_in_family])
            self.mother = mom
            self.father = mom.spouse
            self.father_biological = dad
        
        self.years = 0
        self.months = 0
        self.age = 0
        self.children = 0
        self.children_with_down_syndrom = 0
        self.miscarriages = 0
        self.still_births = 0
        self.has_had_still_birth = False

        self.spouse = None
        
        self.married = False
        self.spouses = []
        
        self.in_relationship = False
        self.sexual_partners = []
        self.sexual_partner_vals = []
        self.prospects = []
        
        self.smv = 0.0

        self.bmi = 0.0

        self.sexual_partners = {
            'partners': {},
            'partner_count': 0,
            'log': {},
        }

    def add_sexual_partner(self, partner):
        if partner in self.sexual_history['partners']:
            count = self.sexual_history['partners'][partner]
            self.sexual_history['partners'][partner] = count + 1
        else:
            self.sexual_history['partners'][partner] = 1
            count = self.sexual_history['partner_count']
            self.sexual_history['partner_count'] = count + 1
        
        if self.years not in self.sexual_history['log']:
            self.sexual_history['log'][self.years] = {}
        if self.months not in self.sexual_history['log'][self.years]:
            self.sexual_history['log'][self.years][self.months] = partner

    def calc_smv(self, person):
        return -1.0

    def calc_smv_alpha(self, person):
        return -1.0

    def calc_smv_beta(self, person):
        return -1.0

    def update(self):
        return

    def update_person(self):
        if self.months == 12:
            self.years += 1
            self.months = 1
        else:
            self.months += 1

        weight_rand = self.random_obj.random()
        weight_inc = 5
        if self.weight_current < self.weight_natural_mod:
            if weight_rand < 0.2:
                self.weight_current -= (self.random_obj.random() * weight_inc)
            elif weight_rand < 0.5:
                self.weight_current = self.weight_current
            else:
                self.weight_current += (self.random_obj.random() * weight_inc)
        else:
            if weight_rand < 0.2:
                self.weight_current += (self.random_obj.random() * weight_inc)
            elif weight_rand < 0.5:
                self.weight_current = self.weight_current
            else:
                self.weight_current -= (self.random_obj.random() * weight_inc)

        self.update_bmi()
        self.update_smv()

    def update_bmi(self):
        self.bmi = 703 * self.weight_current / (self.height * self.height)
