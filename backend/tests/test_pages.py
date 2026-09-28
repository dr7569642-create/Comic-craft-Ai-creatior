def test_homepage_loads(client):
    """Verify that the homepage renders successfully with key comic creator elements."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    content = response.text
    assert "COMICCRAFT" in content
    assert "AI Comic Story Creator" in content
    assert 'name="prompt"' in content
    assert 'name="main_character"' in content
    assert 'name="setting"' in content
    assert 'name="tone"' in content
    assert 'name="art_style"' in content


def test_export_success_page(client):
    """Verify that the export success page renders with download action."""
    response = client.get("/export-success?pdf_url=/static/exports/test.pdf&title=Test%20Comic")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Comic Exported Successfully!" in response.text
    assert "DOWNLOAD PDF NOW" in response.text


def test_static_css_accessible(client):
    """Verify that the comic design CSS file is properly served."""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "COMICCRAFT DESIGN SYSTEM" in response.text
