def parse_user(user):
    try:
        return ({
            "id": user.id,
            "username": user.username,
        })
    except AttributeError:
        return None

def parse_guest(guest):
    if guest is not None:
        try:
            return ({
                "id": guest.id,
                "traits": parse_traits(guest.traits),
                "requirements": parse_traits(guest.requirements),
            })
        except AttributeError:
            return None
    else:
        return None

def parse_host(host):
    if host is not None:
        try:
            return ({
                "id": host.id,
                "traits": parse_traits(host.traits),
                "requirements": parse_traits(host.requirements),
            })
        except AttributeError:
            return None
    else:
        return None

def parse_traits(traits):
    if traits is not None:
        try:
            return ({
                "language": traits.language,
                "disabled": traits.disabled,
                "smoker": traits.smoker,
                "pets_allowed": traits.pets_allowed,
                "has_pets": traits.has_pets,
                "overnight_stay": traits.overnight_stay,
            })
        except AttributeError:
            return None
    else:
        return None
