# MarkDown
renders markup language to **quickly** build docs that renders nicely *without the html pain*.
> Fashion changes, but style endures.<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— Coco Chanel

## Resources
- [Online editor](https://markdown-editor.github.io/)
- [Cheat Sheet](https://www.markdownguide.org/cheat-sheet)
- [My Templates](#templates)

## Templates

### Sections + starting menu + tasks
````markdown {id="" data-filename="classic.md"}
# Title
Description with **bold** and *italic* text followed by
> a smart quote<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— Someone

## Menu
- [Section](#section)
- [Section title with spaces](#section-title-with-spaces)
  - [Sub-Section](#sub-section)
- [Section with custom anchor](#custom-section)
- [Section with code](#section-with-code)
  - [Python](#python-code)
  - [JavaScript](#js-code)
  - [Generic](#generic-code)
- [Tasks](#tasks)

## Section

## Section title with spaces

### Sub-Section

## <a name="custom-section">Section with custom anchor</a>

## Section with code
- <a name="python-code">Python code block</a>
```python {id="python-code-foo" data-filename="foo.py"}
def foo(bar, baz):
  return bar + baz
```

- <a name="js-code">Javascript code block</a>
```javascript {id="js-code-foo" data-filename="foo.js"}
function foo(bar, baz){
  return bar + baz;
}
```

- <a name="generic-code">Inline generic code `print(foo(bar, baz));`</a>

## Tasks
- [x] Copy-paste this template
- [ ] Customize
````
