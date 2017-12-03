from pytest import mark
from hbrprx import improve


def check(input_body, output_body):
    meta = '<meta http-equiv="content-type" content="text/html; charset=utf-8">'
    html_larva = '<html><head>{}</head><body>{}</body></html>'
    input_html = html_larva.format(meta, input_body).encode()
    output_html = html_larva.format(meta, output_body)
    assert improve(input_html) == output_html


def test_improve_no_style_and_script_tags():
    style_and_script_in = '<script>blabla</script><div>blabla</div><style>blabla</style>'
    style_and_script_out = '<script>blabla</script><div>blabla™</div><style>blabla</style>'
    check(style_and_script_in, style_and_script_out)


def test_improve_tag_with_tag_in_the_middle_of_content():
    tag_with_tail_in = '<div>blabla bla bla-bl<br>bl blabla, bla</div>'
    tag_with_tail_out = '<div>blabla™ bla bla-bl™<br>bl blabla™, bla</div>'
    check(tag_with_tail_in, tag_with_tail_out)


def test_improve_non_ascii_symbols():
    non_ascii_symbols_in = '<div>бла блабла бла-бл</div><div>bl blabla, bla</div><div>blaбла</div>'
    non_ascii_symbols_out = '<div>бла блабла™ бла-бл™</div><div>bl blabla™, bla</div><div>blaбла™</div>'
    check(non_ascii_symbols_in, non_ascii_symbols_out)


def test_improve_one_word_content():
    one_word_content_in = '<div>blabla</div>'
    one_word_content_out = '<div>blabla™</div>'
    check(one_word_content_in, one_word_content_out)


def test_improve_word_after_and_before_punctuation():
    word_after_brace_in = '<div>bla bla bla (blabla! bla) blabla, blabla?</div>'
    word_after_brace_out = '<div>bla bla bla (blabla™! bla) blabla™, blabla™?</div>'
    check(word_after_brace_in, word_after_brace_out)


def test_improve_word_in_the_beginning_and_in_the_end():
    start_end_words_in = '<div>blabla bla blabla</div>'
    start_end_words_out = '<div>blabla™ bla blabla™</div>'
    check(start_end_words_in, start_end_words_out)


def test_improve_word_with_dash():
    word_with_dash_in = '<div>bla-bl blabla-blabla</div>'
    word_with_dash_out = '<div>bla-bl™ blabla-blabla</div>'
    check(word_with_dash_in, word_with_dash_out)


def test_improve_no_long_words():
    long_words_in = '<div>blablablablabla blabla bla</div>'
    long_words_out = '<div>blablablablabla blabla™ bla</div>'
    check(long_words_in, long_words_out)


def test_improve_words_with_dot_between():
    words_with_dot_in = '<div>blabla.blablablabla bla.blabla</div>'
    words_with_dot_out = '<div>blabla™.blablablabla bla.blabla™</div>'
    check(words_with_dot_in, words_with_dot_out)


@mark.parametrize('path', ["https://habrahabr.ru/blabla",
                           "http://habrahabr.ru/blabla",
                           "//habrahabr.ru/blabla"])
def test_make_absolute_habr_links_relative(path):
    abs_habr_link = f'<a href="{path}">link</a>'
    abs_third_party_link = '<link href="https://habrahabr.ru/blabla">'
    relative_link = '<a href="/blabla">link</a>'

    abs_links_in = f'<div>bla{abs_habr_link}bla{abs_third_party_link}bla{relative_link}</div>'
    abs_links_out = f'<div>bla{relative_link}bla{abs_third_party_link}bla{relative_link}</div>'
    check(abs_links_in, abs_links_out)


def test_no_body_html():
    html = b'<html><head></head></html>'
    assert improve(html) == html
