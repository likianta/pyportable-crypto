# Cythonize 生成 PYD 文件时的注意事项

## `Cython.cythonize` 不支持海象运算符

测试用例:

```python
_ = (a := 0)
print(a)
```

命令行输入:

```
cythonize -i -3 test.py
```

错误信息:

```
...
Error compiling Cython file:
------------------------------------------------------------
...
_ = (a := 0)
      ^
------------------------------------------------------------
... Expected ')', found ':'
...
```

备注: Github 上似乎有修复它的分支. 但从 PyPI 下载的库未包含此特性.

## 不能对同一变量先后赋予不同类型的值

测试用例:

```python
a = 'some string blabla'
a = a.encode()
```

可以生成 pyd 文件, 但在运行时会报错, 大意是说, 把 `a.encode()` 中的 a 当成了 bytes. (?)

当然这样也不可以:

```python
a = 'some string blabla'
a = a.decode()
```

同类型之间则是可以的:

```python
a = 'some string blabla'
a += 'blabla'
```

解决方法: 赋给一个新的变量即可.

```python
a = 'some string blabla'
b = a.encode()
...
```
