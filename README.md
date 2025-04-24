# code49解码器

本项目仅供[明日方舟](https://ak.hypergryph.com/)PV4解谜使用，目前可以正确解码Mode0和解谜中的两个Mode5条码，不一定能够正常解码其他的Code49条码。

本项目基于Future攻坚组的[code49-decoder](https://github.com/theTeamFuture/code49-decoder)开发。加入了对Mode5的支持以正确解码一阶段条码，并对非数据字符判断进行了修改以解码二阶段条码。

## 如何使用

在`main.py`中：
```
    # 二阶段Code49
    code = [
      '11143121314115211131114321124131314',
      '11221611211411251111225122311314214',
      '11123232212411212332131231332321114',
      '11251311211242114112215212413213114',
      '11123121511212521211113243422213114',
      '11224211311211313421211153141112154'
    ]
```
每一行代表了Code49条码中的一行，数出Code49条码每行中黑条或空白有几个单位长度，将其填入。
> [!WARNING]
> 在每行两侧必须有起始符的`11`与终止符的`4`。

## 参考

**Code 49 encoder source code:** <https://github.com/lukecyca/code49>  
**Code 49 specification:** <https://www.expresscorp.com/wp-content/uploads/2023/02/USS-49.pdf>
