## CFe存储卡自动拉起配置

### 一、CFE磁盘准备

大于128GB，若启动硬盘休眠需要超过256GB

#### （一）格式化磁盘

``` bash
# 安装exfat依赖
sudo apt update
sudo apt install exfat-fuse exfatprogs

# 验证工具是否安装正确 （如果返回类似 /usr/bin/mount.exfat-fuse 的路径，说明工具已正确安装。）
which mount.exfat-fuse

# 查看磁盘信息 （确保目标磁盘是 nvme0n1）
lsblk

# 创建分区 （1.输入 g 创建 GPT 分区表；2.输入 w 保存并退出）
sudo fdisk /dev/nvme0n1

# 创建新分区 （1.输入 n 创建新分区；2.按提示选择分区号、起始扇区和结束扇区（默认值通常即可）；3.输入 t 设置分区类型，选择 7（Microsoft basic data，适用于 exFAT）；4.输入 w 保存并退出；）
sudo fdisk /dev/nvme0n1

# 命令格式化为 exFAT （假设新分区是 nvme0n1p1）
sudo mkfs.exfat /dev/nvme0n1p1
```

格式化磁盘与extfat类似选择分区类型和格式化mkfs的时候选择ext4即可

#### （二）配置rm01cfe标签

``` bash
# 配置标签
sudo exfatlabel /dev/nvme0n1p1 rm01cfe

# 检查标签 （正确输出为：rm01cfe）
sudo exfatlabel /dev/nvme0n1p1

# 若选择ext4格式磁盘
# 配置标签
sudo e2label /dev/nvme0n1p1 rm01cfe
# 验证标签
sudo blkid /dev/nvme0n1p1
```

#### （三）创建挂载点

``` bash
mkdir -p /home/rm01/cfe
```

#### （四）启用自动挂载 (修改/etc/fstab文件，添加如下配置)

```bash
# 使用exfat格式
LABEL=rm01cfe /home/rm01/cfe exfat-fuse defaults,nofail 0 2

# 使用ext4格式
LABEL=rm01cfe /home/rm01/cfe ext4 defaults,nofail 0 2
```

#### 参数说明 ：

- LABEL=rm01cfe：通过 LABEL 唯一标识硬盘。
- /mnt/nvme：挂载点目录。
- ext4：文件系统类型（根据实际情况调整，如 xfs、ntfs 等）。
- defaults,nofail：
  - defaults：使用默认挂载选项。
  - nofail：即使硬盘不存在也不影响系统启动。
- 0 2：
  - 第一个 0：表示不备份。
  - 第二个 2：表示文件系统检查顺序（根分区为 1，其他分区为 2 或 0）。

#### （五）测试配置与查看挂载情况

``` bash
# 测试配置
sudo mount -a

# 查看挂载情况
lsblk
```