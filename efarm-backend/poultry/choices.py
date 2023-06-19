from django.db import models


class FlockSourceChoices(models.TextChoices):
    """
    Choices for the source of a flock.

    - `THIS_FARM`: Flock originated from "This Farm".
    - `KEN_CHICK`: Flock originated from "Ken Chic".
    - `KUKU_CHICK`: Flock originated from "Kuku Chick".
    - `UZIMA_CHICKEN`: Flock originated from "Uzima Chick".
    - `KIPLELS_FARM`: Flock originated from "Kiplel's Farm".
    """
    THIS_FARM = 'This Farm'
    KEN_CHICK = 'Ken Chick'
    KUKU_CHICK = 'Kuku Chick'
    UZIMA_CHICKEN = 'Uzima Chicken'
    KIPLELS_FARM = "Kiplel's Farm"


class ChickenTypeChoices(models.TextChoices):
    """
    Choices for the type of chicken.

    - `BROILER`: BROILER chicken.
    - `LAYERS`: LAYERS chicken.
    - `MULTI_PURPOSE`: Multi-purpose chicken.
    """
    BROILER = 'Broilers'
    LAYERS = 'Layers'
    MULTI_PURPOSE = 'Multi-Purpose'


class HousingStructureTypeChoices(models.TextChoices):
    """
    Choices for the type of housing structure.

    - `OPEN_SIDED_SHED`: Open-sided shed housing structure.
    - `CLOSED_SHED`: Closed shed housing structure.
    - `BATTERY_CAGE`: Battery cage system housing structure.
    - `DEEP_LITTER_HOUSE`: Deep litter house housing structure.
    - `SEMI_INTENSIVE_HOUSING`: Semi-intensive housing structure.
    - `PASTURE_HOUSING`: Pasture housing structure.
    """
    OPEN_SIDED_SHED = 'Open-Sided Shed'
    CLOSED_SHED = 'Closed Shed'
    BATTERY_CAGE = 'Battery Cage System'
    DEEP_LITTER_HOUSE = 'Deep Litter House'
    SEMI_INTENSIVE_HOUSING = 'Semi-Intensive Housing'
    PASTURE_HOUSING = 'Pasture Housing'


class HousingStructureCategoryChoices(models.TextChoices):
    BROODER_CHICK_HOUSE = 'Brooder Chick House'
    GROWERS_HOUSE = 'Growers House'
    LAYERS_HOUSE = 'Layers House'
    BROILERS_HOUSE = 'Broilers House'
    BREEDERS_HOUSE = 'Breeders House'
    # General_Purpose_House = 'General Purpose House'


class RearingMethodChoices(models.TextChoices):
    """
    Choices for the rearing method of a flock.

    - `FREE_RANGE`: Free range rearing method.
    - `CAGE_SYSTEM`: Cage system rearing method.
    - `DEEP_LITTER`: Deep litter rearing method.
    - `BARN_SYSTEM`: Barn system rearing method.
    - `PASTURE_BASED`: Pasture-based rearing method.
    """
    FREE_RANGE = 'Free Range'
    CAGE_SYSTEM = 'Cage System'
    DEEP_LITTER = 'Deep Litter'
    BARN_SYSTEM = 'Barn System'
    PASTURE_BASED = 'Pasture Based'


class FlockBreedTypeChoices(models.TextChoices):
    """
    Choices for the breed type of flock.

    - `KUROILER`: Kuroiler breed.
    - `RAINBOW_ROOSTER`: Rainbow Rooster breed.
    - `KENBRO`: Kenbro breed.
    - `INDIGENOUS`: Indigenous breed.
    - `LEGHORN`: Leghorn breed.
    - `SUSSEX`: Sussex breed.
    - `PLYMOUTH_ROCK`: Plymouth Rock breed.
    - `RHODE_ISLAND_RED`: Rhode Island Red breed.
    - `BRAHMA`: Brahma breed.
    - `CORNISH_CROSS`: Cornish Cross breed.
    - `AUSTRALORP`: Australorp breed.
    - `ORPINGTON`: Orpington breed.
    - `WYANDOTTE`: Wyandotte breed.
    - `SILKIE`: Silkie breed.
    - `COCHIN`: Cochin breed.
    - `EASTER_EGGER`: Easter Egger breed.
    - `BANTAM`: Bantam breed.
    - `SASS0_F1`: Sasso F1 breed.
    - `OTHER`: Other breed.
    """
    KUROILER = 'Kuroiler'
    RAINBOW_ROOSTER = 'Rainbow Rooster'
    KENBRO = 'Kenbro'
    INDIGENOUS = 'Indigenous'
    LEGHORN = 'Leghorn'
    SUSSEX = 'Sussex'
    PLYMOUTH_ROCK = 'Plymouth Rock'
    RHODE_ISLAND_RED = 'Rhode Island Red'
    BRAHMA = 'Brahma'
    CORNISH_CROSS = 'Cornish Cross'
    AUSTRALORP = 'Australorp'
    ORPINGTON = 'Orpington'
    WYANDOTTE = 'Wyandotte'
    SILKIE = 'Silkie'
    COCHIN = 'Cochin'
    EASTER_EGGER = 'Easter Egger'
    BANTAM = 'Bantam'
    SASSO_F1 = 'Sasso F1'
    OTHER = 'Other'
