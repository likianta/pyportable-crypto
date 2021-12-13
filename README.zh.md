# PyPortable Crypto

`pyportable-crypto` 是一个开源的加解密库. 它可以用于:

- 加密/解密文件内容.
- 保护 Python 源代码不被用户查看 (另请参阅 [pyportable-installer](https://github.com/likianta/pyportable-installer)).

## 安装

使用 pip 来安装:

```sh
pip install pyportable-crypto
```

请注意最低支持的 python 版本为 3.8.

## 开始使用

### 加密操作

```python
from pyportable_crypto import encrypt_data
from pyportable_crypto import encrypt_file

# 假设这是我们的密钥.
key = 'abc123456'

# 加密一段文本.
text_i = 'hello world'
text_o = encrypt_data(text_i, key)  # type: bytes
print(text_o)  # -> 加密结果: b'ZKIP01h5mH/6sESFUrAGwQ=='

# 加密文件.
file_i = 'file_i.md'
file_o = 'file_o.md'
encrypt_file(file_i, file_o, key)
# 文件的加密效果见下面的截图.
```

![image-20211213220357973](.assets/README.zh/image-20211213220357973.png)

### 解密操作

```python
from pyportable_crypto import decrypt_data
from pyportable_crypto import decrypt_file

key = 'abc123456'

# 解密一段字符串.
text_i = b'ZKIP01h5mH/6sESFUrAGwQ=='
text_o = decrypt_data(text_i, key)
print(text_o)  # -> 'hello world'

# 解密文件.
file_i = 'file_i.md'
file_o = 'file_o.md'
decrypt_file(file_i, file_o, key)
```

### 保护 Python 源代码

这是 pyportable-crypto 的重点功能. 你可以通过脚本或者 CMD 调用的方式用它来 "编译" 你的 python 源代码文件. 编译的结果可以打包发给用户, 在用户电脑上, 他们可以正常地运行, 但是打开文件所看到的是 "乱码"; 用于解密的钥匙就保存在一个运行时包中 (体积非常小巧, 只有不到 40KB), 即使其他人打开运行时包, 也无法查看到里面的内容, 更无法从中提取到我们真正的密钥 (相关研究和技术验证见 [这篇文章 (*TODO*)](TODO)).

**通过脚本调用**

```python
from pyportable_crypto import Compiler
from uuid import uuid1
compiler = Compiler(key=str(uuid1()), dir_o='~/my_project/lib')
#   `[param]dir_o` 指定一个目录, 我们将会在该目录下生成一个 "pyportable_runtiem"
#   的运行时包. 该运行时包会被用于在用户的电脑上进行解码和加载 python 对象.

# 单文件编译演示.
compiler.compile_file(
    file_i='~/my_project/src/main.py', 
    file_o='~/my_project/dist/main.py'
    #   注: 生成的同样是一个文本类型的 python 脚本文件, 一般建议使用同名表示.
    #       (注意同名但放在不同目录, 以免产生覆盖冲突 (会报错).)
)

# 编译整个文件夹中的 py 文件 (含所有子文件夹)
compiler.compile_dir(
    dir_i='~/my_project/src',
    dir_o='~/my_project/dist',
    # file_exists_scheme='skip'
    #   有一个关键词参数. 该参数的默认值是 "raise_error". 表示当 dir_o 下事先
    #   存在了要编译的文件的话就报错.
    #   可选值: "raise_error", "skip", "overwrite", 或者自定义函数来处理此冲
    #   突 (自定义函数接收一个参数 file_o, 即待处理的冲突文件的绝对路径).
)
#   注: 建议 `[param]dir_o` 使用一个不同于 `dir_i` 的文件夹放置 (二者不要相互包含). 

```

**在 CMD 中调用**

```sh
python -m pyportable_crypto compile-file <file_i> <file_o> <key>
#   随同产生的 `pyportable_runtime` 运行时包会在 <file_o> 同目录下生成.

python -m pyportable_crypto compile-dir <dir_i> <dir_o> <key>
#   随同产生的 `pyportable_runtime` 运行时包会在 <dir_o> 目录下生成.
```

混淆后的脚本文件看起来长这样:

```python
# some_compiled_files.py
from pyportable_runtime import decrypt
globals(decrypt(b'ZKIP01h5mH/6sESFUrAGwQ==...', globals(), locals()))
```

其中 decrypt 函数会返回一个 python 字典对象. 调用者可以像平时一样使用该模块, 无需关心有什么内部变化需要处理. 再次提醒, 整个过程中并不会把任何源代码暴露给使用者, 并且在多方面验证和隔绝了使用者从加载后的 python 字典对象攫取源代码的可能性.

PS: 不要忘记把 `pyportable_runtime` 运行时包随要发布的应用程序一起打包. 并且在调用其他模块之前, 它需要最先被加入到 `sys.path`.

