# code49 解码器

本项目仅供[明日方舟](https://ak.hypergryph.com/)解谜使用，目前可以正确解码Mode0和解谜中的两个Mode5条码，不一定能够正常解码其他的Code49条码。

本项目基于Future攻坚组的[code49-decoder](https://github.com/theTeamFuture/code49-decoder)开发。加入了对Mode5的支持以正确解码二阶段条码，并对非数据字符判断进行了修改以解码三阶段条码。

## 如何使用

### 下载

前往 [Release](https://github.com/Leo-455/code49-decoder/releases) 下载最新版的 `Code49Decoder_vx.x.x.exe` 文件

### 使用

在 exe 文件的同一目录下创建 `code.txt` 并输入条码数据。  
如何将条码读取为数据：可参考[这里](https://github.com/Leo-455/Arknights-PV4-ARG-Docs/blob/master/docs/zh_CN/main.md#%E6%89%8B%E5%8A%A8%E8%A7%A3%E7%A0%81)

示例：在`code.txt`中输入：
```
11143121314115211131114321124131314
11221611211411251111225122311314214
11123232212411212332131231332321114
11251311211242114112215212413213114
11123121511212521211113243422213114
11224211311211313421211153141112154
```

每一行代表了Code49条码中的一行。  
可在其中使用`_`作为分割注释，其在读取时将被忽略。  
如可使用`11_14312131_41152111_31114321_12413131_4`

> [!WARNING]
> 在每行两侧必须有起始符的`11`与终止符的`4`。  
> 输入时需要严格按照原条码的行数、位置进行，若条码有缺失的部分，必须输入数字（如0）进行占位。

启动 exe 输入`1`选择`从txt文件输入`  
输入`code.txt` 随后将显示读取到的内容  

按 Enter 后将进行解码并显示解码过程  

其中 Character Value 部分将显示每行的校验情况
```
Character Value:
Row1: [24, 44, 31, 44, 14, 44, 27, 32] Correct! # 校验正确
Row2: [44, 12, 44, 39, 44, 23, 44, 39] [ERROR] # 校验失败
```

Total Code Check 部分将显示使用校验词对整张条码进行校验的结果
```
Total Code Check: Correct! # 校验正确
Total Code Check: [ERROR] # 校验失败
```

Result 部分将显示最终解码的结果
```
Result:
overcontact binary
```

若需要保存解码结果，输入`y` 然后输入文件名或留空使用默认文件名，解码结果将保存到txt文件中

`result.txt`
```
overcontact binary
```

### 报错
code49-decoder 会显示解码过程中遇到的错误，但不会停止，而是继续尝试进行解码。

- `[ERROR]: Row1 length incorrect`  
某行的长度有误，可能是输入时漏了数字

- `[ERROR]: Row2 Word2 '14112521' is not in list Please Check pattern!`  
某行某词无法在对应表中找到，可能是输错了数字或词的位置有误

- `Mode:N/A decode as mode 0`  
模式词损坏，无法解码出模式号，以 Mode0 进行解码

- 若每行的行校验通过但整张条码的词校验未通过，可能是同一行或不同行的奇性词/偶性词之间的位置有错误

### 文档
Code49 介绍可参考：[这里](https://github.com/Leo-455/Arknights-PV4-ARG-Docs/blob/master/docs/zh_CN/main.md#code49)

### 其它模式

- `2.查看示例`  
选择后可选择解谜二阶段/三阶段中用到的条码进行尝试

## 参考

**Code 49 encoder source code:** <https://github.com/lukecyca/code49>  
**Code 49 specification:** <https://www.expresscorp.com/wp-content/uploads/2023/02/USS-49.pdf>
