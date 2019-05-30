# EgretLibMerge
EgretLib合并工具（工作项目），用于Egret项目引用的库文件打包成一个js文件，减少网络io，此工具依赖manifest.json
> exe文件是用pyinstaller打包成无依赖的执行文件，可以直接拷贝exe文件到任何地方执行

## 使用方法
```cmd
EgretLibMerge.exe --source xxx
```

```yaml
参数说明：
--source Egret项目发布目录
```

## 工具目录说明
-- EgretLibMerge.exe  
> 已经打包好的程序执行文件，无需其他文件依赖
  
-- EgretLibMerge.py
> 编译的源文件，exe文件执行时候无需依赖，只作开源学习用途  
> 如果有python环境，则可代替exe工具，通过python命令直接执行（python 3.7）

-- README.md
> 说明文档