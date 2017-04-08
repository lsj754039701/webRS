import re
import sys

def replace_js(m):
    return m.group(1) + "{{static_url('" + m.group(2) + "')}}" + m.group(3)

def replace_css(m):
    return m.group(1) + "{{static_url('css/" + m.group(3) + "')}}" + m.group(4)

def replace_img(m):
    return m.group(1) + "{{static_url('" + m.group(2) + "')}}" + m.group(3)

if __name__ == '__main__':
    f = sys.argv[1]
    with open(f) as f:
        str1 = f.read()
    p = re.compile(r'(script.*?src=")(.*?)(".*?</script>)', re.M)
    p2 = re.compile(r'(link href=")(css/)(.*?)(".*?>)', re.M)
    p3 = re.compile(r'(<img src=")(.*?)(".*?>)', re.M)
    str1 = p.sub(replace_js, str1)
    str1 = p2.sub(replace_css, str1)
    str1 = p3.sub(replace_img, str1)
    print str1

    # s = """hello
    #         <link href="css/bootstrap.min.css" rel='stylesheet' type='text/css' media="all" />
    #         <a href="single.html"><img src="images/c2.jpg" alt="" /></a>
		#     <div class="time small-time slider-time">
    #
    #         <link href="css/bootstrap.min.css" rel='stylesheet' type='text/css' media="all" />
    #         <!-- //bootstrap -->
    #         <link href="css/dashboard.css" rel="stylesheet">
    #         world"""
    #
    # p = re.compile(r'(script.*?src=")(.*?)(".*?</script>)', re.M)
    # p2 = re.compile(r'(link href=")(css/)(.*?)(".*?>)', re.M)
    # p3 = re.compile(r'(<img src=")(.*?)(".*?>)', re.M)
    # s = p2.sub(replace_css, s)
    # print s
    # s = p3.sub(replace_img, s)
    # print s