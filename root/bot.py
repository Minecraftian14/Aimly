import json
import sys
import traceback
from datetime import datetime
from os import listdir, path

from discord.ext.commands import Bot, when_mentioned_or
from discord import Intents, Message, Activity, DMChannel


class Aimly(Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.session = None
        with open('../config.json') as conffile:
            self.config = json.load(conffile)
        self.last_errors = []

    async def start(self, *args, **kwargs):
        await super().start(self.config["bot_key"], *args, **kwargs)

    async def close(self):
        await super().close()

    def user_is_dev(self, user):
        superusers = self.config['developers']
        return user.id in superusers

    def user_is_banned(self, user):
        superusers = self.config['banned']
        return user.id in superusers

    # def user_is_admin(self, user):
    #     try:
    #         user_roles = [role.id for role in user.roles]
    #     except AttributeError:
    #         return False
    #     return any(role for role in user_roles) # make it, role.name == 'admin'


##########################################################################

# intents = Intents.default()
# intents.members = True

client = Aimly(
    command_prefix=when_mentioned_or('aimly ', 'Aelix ', '!'),
    description='Hi I am Aimly!',
    max_messages=1500,
    # intents=intents
)

STARTUP_EXTENSIONS = []

for file in listdir(path.join(path.dirname(__file__), 'commands/')):
    filename, ext = path.splitext(file)
    if '.py' in ext:
        STARTUP_EXTENSIONS.append(f'commands.{filename}')

for extension in reversed(STARTUP_EXTENSIONS):
    try:
        client.load_extension(f'{extension}')
    except Exception as e:
        client.last_errors.append((e, datetime.utcnow(), None, None))
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {extension}\n{exc}')


##########################################################################

@client.event
async def on_ready():
    main_id = client.config['headquarters']
    client.main_guild = client.get_guild(main_id) or client.guilds[0]
    print('\nActive in these guilds/servers:')
    [print(g.name) for g in client.guilds]
    print('\nMain guild:', client.main_guild.name)
    print('\nFelix-Python started successfully')
    return True


@client.event
async def on_error(event_method, *args, **kwargs):
    print('Default Handler: Ignoring exception in {}'.format(event_method), file=sys.stderr)
    traceback.print_exc()
    if len(args) > 1:
        a1, a2, *_ = args
        if isinstance(a1, Message) and isinstance(a2, Message):
            client.last_errors.append((sys.exc_info()[1], datetime.utcnow(), a2, a2.content))
        await client.change_presence(
            activity=Activity(name='ERROR encountered', url=None, type=3)
        )


@client.event
async def on_message(msg):
    if isinstance(msg.channel, DMChannel):
        return
    if client.user_is_banned(msg.author):
        return
    await client.process_commands(msg)


client.run()
print('Aimly is taking a rest 😁')
