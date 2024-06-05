from dataclasses import dataclass

from django.contrib.auth.management.commands import createsuperuser

from organizations.models import Organization


class Command(createsuperuser.Command):
    """ Команда, заменяющая стандартную createsuperuser.
        Так как модель User содержит поле organization, которое не может быть пустым,
        мы должны перед созданием super user получить id организации, проверить,
        существует ли такая в системе и если нет, то запросить имя организации и
        создать её в системе, передав на вход основной команде id организации.
    """

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
        return True

    def get_organization(self, **kwargs) -> str:
        def print_msg(msg: str) -> None:
            self.stdout.write(msg=msg, ending="")
            self.stdout.flush()

        # Проверим, присутствует ли в командной строке id организации
        command_line_id = kwargs.get('organization_id', None)
        if command_line_id:
            # Если в командной строке есть ИНН организации, то
            # проверим, есть ли такая организация в нашей базе
            organization_exists = Organization.objects.filter(id=command_line_id).exists()
        else:
            organization_exists = False

        if not organization_exists:



            # Необходимо создать новую организацию
            print_msg("Введите ИНН организации: ")
            new_organization_id = self.stdin.readline().rstrip('\n')
            while not self.validate_organization_id(new_organization_id):
                self.stdout.write(self.style.WARNING(f'ИНН {new_organization_id} не может существовать.'))
                print_msg("Введите ИНН организации: ")
                new_organization_id = self.stdin.readline().rstrip('\n')

            print_msg("Введите наименование организации: ")
            new_organization_name = self.stdin.readline().rstrip('\n')
            Organization.objects.get_or_create(id=new_organization_id, name=new_organization_name)
            return new_organization_id
        else:
            organization = Organization.objects.get(id=command_line_id)
            return organization.id

    def create(self, data):
        return None

    def display_result(self, data):
        pass

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating superuser !!!'))
        self.stdout.write(self.style.WARNING(f'args: {args}'))
        self.stdout.write(self.style.ERROR(f'kwargs: {kwargs}'))

        kwargs['organization_id'] = self.get_organization(**kwargs)

        # organization = self.get_organization(**kwargs)

        # super().handle(*args, **kwargs)

        # for user_id in users_ids:
        #     try:
        #         user = User.objects.get(pk=user_id)
        #         user.delete()
        #         self.stdout.write(self.style.SUCCESS(f'Пользователь {user.username} c ID {user_id} был удален!'))
        #     except User.DoesNotExist:
        #         self.stdout.write(self.style.WARNING(f'Пользователь с ID {user_id} не существует.'))

