# 动漫之家订阅导出工具

导出动漫之家的漫画订阅到[Tachiyomi](https://github.com/inorichi/tachiyomi)

## 使用方式

1. 网页端登录[动漫之家](https://i.dmzj.com/my)，找到自己的UID
![](img/uid.png)

2. 在[Tachiyomi](https://github.com/inorichi/tachiyomi)中添加动漫之家，收藏任一漫画，创建备份
![](img/backup.png)

3. 打开备份的json文件，找到 `"extensions": ["2884190037559093788:动漫之家"]`，数字部分即为图源ID
![](img/json.png)

4. 运行本工具，填入图源ID和动漫之家UID，生成json文件，在[Tachiyomi](https://github.com/inorichi/tachiyomi)中选择恢复
![](img/example.png)

5. EOF

## TODO

- [ ] 同时支持Cimoc