from core.settings import settings


def render_template(name: str, **kwargs) -> str:
    template = settings.templates.get_template(name=name)
    return template.render(
        **kwargs
    )
