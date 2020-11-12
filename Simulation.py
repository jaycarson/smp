from Woman import Woman
import yaml
import argparse
from Man import Man
from Woman import Woman


class Simulation(object):
    def __init__(self, size, debug):
        self.seed_size = int(size)
        self.seed_period = 12 * 10
        self.debug = debug

        self.chance_to_conceive = yaml.load(open('fertility.yml', 'r'), Loader=yaml.FullLoader)
        self.chance_to_miscarry = yaml.load(open('miscarriage.yml', 'r'), Loader=yaml.FullLoader)
        self.chance_on_ivf = yaml.load(open('ivf.yml', 'r'), Loader=yaml.FullLoader)

        self.population = []
        self.women = []
        self.men = []

        self.seed = 0

    def __call__(self):
        if self.debug:
            print('Simulation: Starting')
        for period in range(0, self.seed_period):
            print(period)
            if period % 12 == 0:
                self.seed_population()
            for man in self.men:
                man()
            for woman in self.women:
                woman()
        if self.debug:
            print('Simulation: Done')

    def seed_population(self):
        if self.debug:
            print('Simulation: Seeding Population')
        self.seed_men()
        self.seed_women()

    def seed_men(self):
        for man_id in range(0, self.seed_size):
            man = Man(simulation=self, seed=self.seed)
            self.population.append(man)
            self.men.append(man)
            self.seed += 1

    def seed_women(self):
        for woman_id in range(0, self.seed_size):
            woman = Woman(
                    simulation=self,
                    conceive=self.chance_to_conceive,
                    miscarry=self.chance_to_miscarry,
                    ivf=self.chance_on_ivf,
                    seed=self.seed,
            )
            self.population.append(woman)
            self.women.append(woman)
            self.seed += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            """,
        epilog="""
            """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action='store_true',
        help="Sets debugging.",
    )

    args = parser.parse_args()

    app = Simulation(size=100, debug=args.debug)
    app()
