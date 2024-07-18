from .models import EthicalTypes


def create_ethical_types():
    only_kantian = EthicalTypes()
    only_kantian.categorical_imperative = 100
    only_kantian.utilitarian = 0
    only_kantian.virtue_ethics = 0
    only_kantian.animal_rights = 0
    only_kantian.longtermism = 0
    only_kantian.save()

    kantian_animal_rights = EthicalTypes()
    kantian_animal_rights.categorical_imperative = 100
    kantian_animal_rights.utilitarian = 0
    kantian_animal_rights.virtue_ethics = 0
    kantian_animal_rights.animal_rights = 100
    kantian_animal_rights.longtermism = 0
    kantian_animal_rights.save()

    kantian_longtermist = EthicalTypes()
    kantian_longtermist.categorical_imperative = 100
    kantian_longtermist.utilitarian = 0
    kantian_longtermist.virtue_ethics = 0
    kantian_longtermist.animal_rights = 0
    kantian_longtermist.longtermism = 100
    kantian_longtermist.save()

    kantian_virtue_ethics = EthicalTypes()
    kantian_virtue_ethics.categorical_imperative = 100
    kantian_virtue_ethics.utilitarian = 0
    kantian_virtue_ethics.virtue_ethics = 100
    kantian_virtue_ethics.animal_rights = 0
    kantian_virtue_ethics.longtermism = 100
    kantian_virtue_ethics.save()

    undecided = EthicalTypes()
    undecided.categorical_imperative = 50
    undecided.utilitarian = 50
    undecided.virtue_ethics = 50
    undecided.animal_rights = 50
    undecided.longtermism = 50
    undecided.save()

    undecided_pro_animals = EthicalTypes()
    undecided_pro_animals.categorical_imperative = 50
    undecided_pro_animals.utilitarian = 50
    undecided_pro_animals.virtue_ethics = 50
    undecided_pro_animals.animal_rights = 100
    undecided_pro_animals.longtermism = 50
    undecided_pro_animals.save()

    undecided_longtermist = EthicalTypes()
    undecided_longtermist.categorical_imperative = 50
    undecided_longtermist.utilitarian = 50
    undecided_longtermist.virtue_ethics = 50
    undecided_longtermist.animal_rights = 100
    undecided_longtermist.longtermism = 50
    undecided_longtermist.save()

    undecided_utilitarian_preferring = EthicalTypes()
    undecided_utilitarian_preferring.categorical_imperative = 75
    undecided_utilitarian_preferring.utilitarian = 50
    undecided_utilitarian_preferring.virtue_ethics = 50
    undecided_utilitarian_preferring.animal_rights = 100
    undecided_utilitarian_preferring.longtermism = 50
    undecided_utilitarian_preferring.save()

    undecided_kantian_preferring = EthicalTypes()
    undecided_kantian_preferring.categorical_imperative = 50
    undecided_kantian_preferring.utilitarian = 75
    undecided_kantian_preferring.virtue_ethics = 50
    undecided_kantian_preferring.animal_rights = 100
    undecided_kantian_preferring.longtermism = 50
    undecided_kantian_preferring.save()

    undecided_virtue_ethics_preferring = EthicalTypes()
    undecided_virtue_ethics_preferring.categorical_imperative = 50
    undecided_virtue_ethics_preferring.utilitarian = 50
    undecided_virtue_ethics_preferring.virtue_ethics = 75
    undecided_virtue_ethics_preferring.animal_rights = 100
    undecided_virtue_ethics_preferring.longtermism = 50
    undecided_virtue_ethics_preferring.save()

    onyl_animals = EthicalTypes()
    onyl_animals.categorical_imperative = 0
    onyl_animals.utilitarian = 0
    onyl_animals.virtue_ethics = 0
    onyl_animals.animal_rights = 100
    onyl_animals.longtermism = 0
    onyl_animals.save()

    onyl_utilitarian = EthicalTypes()
    onyl_utilitarian.categorical_imperative = 0
    onyl_utilitarian.utilitarian = 100
    onyl_utilitarian.virtue_ethics = 0
    onyl_utilitarian.animal_rights = 0
    onyl_utilitarian.longtermism = 0
    onyl_utilitarian.save()

    utilitarian_animal_rights = EthicalTypes()
    utilitarian_animal_rights.categorical_imperative = 0
    utilitarian_animal_rights.utilitarian = 100
    utilitarian_animal_rights.virtue_ethics = 0
    utilitarian_animal_rights.animal_rights = 100
    utilitarian_animal_rights.longtermism = 0
    utilitarian_animal_rights.save()

    utilitarian_longtermist = EthicalTypes()
    utilitarian_longtermist.categorical_imperative = 0
    utilitarian_longtermist.utilitarian = 100
    utilitarian_longtermist.virtue_ethics = 0
    utilitarian_longtermist.animal_rights = 0
    utilitarian_longtermist.longtermism = 100
    utilitarian_longtermist.save()

    utilitarian_longtermist_animal_rights = EthicalTypes()
    utilitarian_longtermist_animal_rights.categorical_imperative = 0
    utilitarian_longtermist_animal_rights.utilitarian = 100
    utilitarian_longtermist_animal_rights.virtue_ethics = 0
    utilitarian_longtermist_animal_rights.animal_rights = 100
    utilitarian_longtermist_animal_rights.longtermism = 100
    utilitarian_longtermist_animal_rights.save()

    only_virtue = EthicalTypes()
    only_virtue.categorical_imperative = 0
    only_virtue.utilitarian = 0
    only_virtue.virtue_ethics = 100
    only_virtue.animal_rights = 0
    only_virtue.longtermism = 0
    only_virtue.save()

    virtue_animal_rights = EthicalTypes()
    virtue_animal_rights.categorical_imperative = 0
    virtue_animal_rights.utilitarian = 0
    virtue_animal_rights.virtue_ethics = 100
    virtue_animal_rights.animal_rights = 100
    virtue_animal_rights.longtermism = 0
    virtue_animal_rights.save()

    virtue_animal_rights_longterism = EthicalTypes()
    virtue_animal_rights_longterism.categorical_imperative = 0
    virtue_animal_rights_longterism.utilitarian = 0
    virtue_animal_rights_longterism.virtue_ethics = 100
    virtue_animal_rights_longterism.animal_rights = 100
    virtue_animal_rights_longterism.longtermism = 100
    virtue_animal_rights_longterism.save()

    virtue_longterism = EthicalTypes()
    virtue_longterism.categorical_imperative = 0
    virtue_longterism.utilitarian = 0
    virtue_longterism.virtue_ethics = 100
    virtue_longterism.animal_rights = 0
    virtue_longterism.longtermism = 100
    virtue_longterism.save()
