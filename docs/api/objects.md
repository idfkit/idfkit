# Objects

`IDFObject` represents a single EnergyPlus object (e.g. a Zone or a
Material). Fields are accessed as snake_case Python attributes.

`IDFCollection` is a name-indexed container of objects that share the same
EnergyPlus type, providing O(1) lookup by name, iteration, and filtering.

::: idfkit.objects
