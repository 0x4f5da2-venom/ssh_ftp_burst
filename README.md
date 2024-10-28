# 爆破工具

此工具是一款小型的爆破工具，目前支持 SSH、FTP 和端口爆破。

## 功能

- **FTP 爆破**：使用用户名和密码字典进行 FTP 登录尝试。
- **SSH 爆破**：使用用户名和密码字典进行 SSH 登录尝试。
- **端口爆破**：扫描目标 IP 的开放端口。

## 使用方法

### 运行环境

确保已安装以下 Python 库：

- `ftplib`
- `paramiko`
- `socket`
- `queue`
- `threading`

### 命令行参数

- `[模式]`：选择 `ftp`、`ssh` 或 `burst`。
- `[参数]`：
  - 对于 `ftp` 和 `ssh` 模式：需要提供目标 IP、用户名字典文件和密码字典文件。
  - 对于 `burst` 模式：只需提供目标 IP。

### 示例

- **FTP 爆破**

- - **SSH 爆破**

  - 示例

    ```
    python xxx.py ftp 192.168.1.1 user.txt password.txt
    ```

```
python xxx.py ssh 192.168.1.1 user.txt password.txt
```

```
python xxx.py burst
```

然后根据提示输入目标 IP 和线程数，并选择扫描模式（全端口或自定义端口）。

## 注意事项

- 请确保在合法和授权的范围内使用此工具。
- 使用前请确认符合相关法律法规。

## 作者

- 0x4f5da2