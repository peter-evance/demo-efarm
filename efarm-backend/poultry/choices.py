from django.db import models


class FlockSourceChoices(models.TextChoices):
    """
    Choices for the source of a flock.

    - `This_Farm`: Flock originated from "This Farm".
    - `Ken_Chic`: Flock originated from "Ken Chic".
    - `Kuku_Chick`: Flock originated from "Kuku Chick".
    - `Uzima_Chicken`: Flock originated from "Uzima Chick".
    - `Kiplels_Farm`: Flock originated from "Kiplel's Farm".
    """
    This_Farm = 'This Farm'
    Ken_Chic = 'Ken Chic'
    Kuku_Chick = 'Kuku Chick'
    Uzima_Chicken = 'Uzima Chick'
    Kiplels_Farm = "Kiplel's Farm"


class ChickenTypeChoices(models.TextChoices):
    """
    Choices for the type of chicken.

    - `Broiler`: Broiler chicken.
    - `Layers`: Layers chicken.
    - `Multi_Purpose`: Multi-purpose chicken.
    """
    Broiler = 'Broiler'
    Layers = 'Layers'
    Multi_Purpose = 'Multi-Purpose'


class HousingStructureTypeChoices(models.TextChoices):
    """
    Choices for the type of housing structure.

    - `Open_Sided_Shed`: Open-sided shed housing structure.
    - `Closed_Shed`: Closed shed housing structure.
    - `Battery_Cage`: Battery cage system housing structure.
    - `Deep_Litter_House`: Deep litter house housing structure.
    - `Semi_Intensive_Housing`: Semi-intensive housing structure.
    - `Pasture_Housing`: Pasture housing structure.
    """
    Open_Sided_Shed = 'Open-Sided Shed'
    Closed_Shed = 'Closed Shed'
    Battery_Cage = 'Battery Cage System'
    Deep_Litter_House = 'Deep Litter House'
    Semi_Intensive_Housing = 'Semi-Intensive Housing'
    Pasture_Housing = 'Pasture Housing'


class HousingStructureCategoryChoices(models.TextChoices):
    Brooder_Chick_House = 'Brooder Chick House'
    Growers_House = 'Growers House'
    Layers_House = 'Layers House'
    Broilers_House = 'Broilers House'
    Breeders_House = 'Breeders House'
    # General_Purpose_House = 'General Purpose House'


class RearingMethodChoices(models.TextChoices):
    """
    Choices for the rearing method of a flock.

    - `Free_Range`: Free range rearing method.
    - `Cage_System`: Cage system rearing method.
    - `Deep_Litter`: Deep litter rearing method.
    - `Barn_System`: Barn system rearing method.
    - `Pasture_Based`: Pasture-based rearing method.
    """
    Free_Range = 'Free Range'
    Cage_System = 'Cage System'
    Deep_Litter = 'Deep Litter'
    Barn_System = 'Barn System'
    Pasture_Based = 'Pasture Based'