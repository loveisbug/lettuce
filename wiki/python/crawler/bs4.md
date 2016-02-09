#### `.children` & `.previous_sibling`
original text is:

    <li><a href="example"> s.r.o., <small>small</small></a></li>
    
need to get the text ` s.r.o., `.

    from bs4 import BeautifulSoup
    data = '<li><a href="example"> s.r.o., <small>small</small></a></li>'
    soup = BeautifulSoup(data)

1. `.contents`

    `.contents`返回一个`list`。

        print soup.find('a').contents[0]
        # print soup.find('a').contents
        # [u' s.r.o., ', <small>small</small>]
        
1. `.children`

    也可用`.children`迭代输出`.contents`返回`list`的内容。

        print next(soup.find('a').children)
        
1. `.descendants` or `iter`

    `.contents`和`.children`都只考虑了直接children，`.descendants`迭代所有的children，递归输出。

        print next(soup.find('a').descendants)
        
        print next(iter(soup.find('a')))
    
1. `.previous_sibling`

        print soup.find('small').previous_sibling
        
参考：

[`.children`文档](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children)

[`.previous_sibling`文档](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling)