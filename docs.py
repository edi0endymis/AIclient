from pdoc import doc, render
import memory

if __name__ == '__main__':
    document = doc.Module(memory)
    out = render.html_module(module=document, all_modules={'memory': document})
    with open('dist/docs.html', 'w') as f:
        f.write(out)
