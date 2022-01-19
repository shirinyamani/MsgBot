from types import SimpleNamespace
from src.utils.keyboard import create_keyboard


keys = SimpleNamespace(
    random_connect='Connect :handshake:',
    help='Help :smiling_face_with_halo:',
    exit=':cross_mark: Exit')
    
keyboards = SimpleNamespace(
    exit=create_keyboard(keys.exit),
    main_keyboard=create_keyboard(keys.random_connect, keys.help))

states = SimpleNamespace(
    random_connect='Your State is <strong>Random Connect!</strong>',
    menu='You are in <strong>Menu!</strong>'
)