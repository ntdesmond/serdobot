import vk


def parse(filepath):
    settings = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            name, value = line.split('=')
            settings[name] = value
    return settings


group = parse(".settings/group")
api = vk.API(vk.Session(group["MSG_PHOTOS_TOKEN"]), v=5.103)
