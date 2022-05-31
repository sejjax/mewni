from muni.core import Model

@Model
class User(Model):
    @Column
    name: str
    @Column(
        null=False,
        default='Danil'
    )
    colort: str
