import pytest

@pytest.mark.smoke(reason='/keyhole')
def test_get_keyhole(app):
    res = app.keyhole
    assert bool(res) == 1

@pytest.mark.smoke(reason="'/' index.html")
def test_get_index(app):
    res = app.index
    assert bool(res) == 1\

@pytest.mark.smoke(reason='/map')
def test_get_map(app):
    res = app.map
    assert bool(res) == 1\

@pytest.mark.smoke(reason='/partners')
def test_get_partner(app):
    res = app.partner
    assert bool(res) == 1

@pytest.mark.smoke(reason='/partner_info')
def test_get_partner_info(app):
    res = app.partner_info
    assert bool(res) == 1

@pytest.mark.smoke(reason='/partner_info_eliton')
def test_get_partner_info_eliton(app):
    res = app.partner_info_eliton
    assert bool(res) == 1

@pytest.mark.smoke(reason='/partner_info_lina')
def test_get_partner_info_lina(app):
    res = app.partner_info_lina
    assert bool(res) == 1

@pytest.mark.smoke(reason='/partner_info_pa')
def test_get_partner_info_pa(app):
    res = app.partner_info_pa
    assert bool(res) == 1

@pytest.mark.smoke(reason='/send')
def test_get_send(app):
    res = app.send
    assert bool(res) == 1

@pytest.mark.smoke(reason='/groups')
def test_get_groups(app):
    res = app.groups
    assert bool(res) == 1

@pytest.mark.smoke(reason='/price')
def test_get_price(app):
    res = app.price
    assert bool(res) == 1

@pytest.mark.smoke(reason='/catalog')
def test_get_catalog(app):
    res = app.catalog
    assert bool(res) == 1

@pytest.mark.smoke(reason='/ostatkyxlsx')
def test_get_ostatkyxlsx(app):
    res = app.ostatkyxlsx
    assert bool(res) == 1

