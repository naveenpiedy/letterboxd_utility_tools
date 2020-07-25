from jinja2 import Environment, FileSystemLoader


def make_card_html(img_src, content):
    content = 'This is about page'
    img_src = "http://image.tmdb.org/t/p/w600_and_h900_bestv2/wOgmhrSUwOuZJsQXf2GsI923N0f.jpg"
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('card.html')

    output = template.render(content=content, imgsrc=img_src)
    print(output)


if __name__ == '__main__':
    make_card_html("hh", "jj")
