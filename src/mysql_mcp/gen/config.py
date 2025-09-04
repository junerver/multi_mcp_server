# 生成配置，等同于原yaml配置
GEN_CONFIG = {
  # 作者
  "author": "jkr",
  # 默认生成包路径 system 需改成自己的模块名称 如 system monitor tool
  "packageName": "com.jkr.project.system",
  # 自动去除表前缀，默认是true
  "autoRemovePre": False,
  # 表前缀（生成类名不会包含表前缀，多个用逗号分隔）
  "tablePrefix": "sys_",
  # 是否允许生成文件覆盖到本地（自定义路径），默认不允许
  "allowOverwrite": False,
}