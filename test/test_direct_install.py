import direct_install

def test_direct_install_redirects_with_302():
    result = direct_install.handle({}, {})
    assert result['statusCode'] == 302
    assert result['headers']['Location'] == direct_install.OAUTH_AUTHORIZE_URL
