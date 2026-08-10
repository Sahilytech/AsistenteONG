from src.core.access_control import AccessContext, can


def test_roles_have_least_privilege():
    assert can("consulta", "view")
    assert not can("consulta", "delete")
    assert can("administracion", "manage_users")


def test_access_context_rejects_unauthorized_action():
    context = AccessContext("u1", "operador")
    assert context.can("edit")
    assert not context.can("delete")
