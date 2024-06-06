from dataclasses import dataclass

from django.contrib.auth.management.commands import createsuperuser

from core.organization_id import is_inn_valid
from organizations.models import Organization


class Command(createsuperuser.Command):
    """ Команда, заменяющая стандартную createsuperuser.
        Так как модель User содержит поле organization, которое не может быть пустым,
        мы должны перед созданием super user получить id организации, проверить,
        существует ли такая в системе и если нет, то запросить имя организации и
        создать её в системе, передав на вход основной команде id организации.
    """

    def _print_msg(self, msg: str) -> None:
        self.stdout.write(msg=msg, ending="")
        self.stdout.flush()

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Named (optional) arguments

        # Дополнительный аргумент создался автоматически при добавлении "organization_id" в
        # REQUIRED_FIELDS = [f'{AbstractUser.EMAIL_FIELD}', "organization_id"]
        # в модели User

        # parser.add_argument(
        #     "--organization",
        #     type=str,
        #     help="ИНН организации",
        # )

    def validate_organization_id(self, organization_id: str) -> bool:
        """Проверяем правильность ИНН"""
        return is_inn_valid(organization_id)

    def get_organization(self, **kwargs) -> str:
        # Проверим, присутствует ли в командной строке id организации
        org_ig_from_command_line = kwargs.get('organization_id', None)
        if org_ig_from_command_line:
            # Если в командной строке есть ИНН организации, то
            # проверим, есть ли такая организация в нашей базе
            if Organization.objects.filter(id=org_ig_from_command_line).exists():
                return org_ig_from_command_line
            new_organization_id = org_ig_from_command_line
        else:
            # Необходимо создать новую организацию
            self._print_msg("Введите ИНН организации: ")
            new_organization_id = self.stdin.readline().rstrip('\n')
        organization = self.create_organization(new_organization_id)
        return organization.id

    def create_organization(self, id: str) -> Organization:
        new_organization_id = id
        while not self.validate_organization_id(new_organization_id):
            self.stdout.write(self.style.ERROR(f'Ошибка:  ИНН {new_organization_id} не может существовать.'))
            self._print_msg("Введите ИНН организации: ")
            new_organization_id = self.stdin.readline().rstrip('\n')

        self._print_msg("Введите наименование организации: ")
        new_organization_name = self.stdin.readline().rstrip('\n')
        return Organization.objects.create(id=new_organization_id, name=new_organization_name)

    def handle(self, *args, **kwargs):
        try:
            kwargs['organization_id'] = self.get_organization(**kwargs)
        except KeyboardInterrupt:
            self.stdout.write("\nKeyboardInterrupt")
            return
        super().handle(*args, **kwargs)

