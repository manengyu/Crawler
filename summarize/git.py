https://juejin.im/post/599e14875188251240632702
git远程仓库至本地
方法一
git clone http://...[[.git] myrepository]
方法二
git init
git remote add origin http://...git# 将本地库与远端库关联
git pull origin master

git pull等价git fetch + git merge拉取下来合并(合并时有冲突需要手动解决冲突)
git merge dev合并dev分支到当前分支
git log --graph --pretty=oneline --abbrev-commit查看分支合并图
git branch -m dev develop
git push origin develop
git push --delete origin dev
git rm -r --cached .idea


生成密钥
git config --global user.name "name"
git config --global user.email "xx@xx.com"
ssh-keygen -t rsa -C "xx@xx.com"
邮箱仅仅为注释用作标识用户身份而已
若某个项目使用单独用户名，可git config设置
多个ssh key时，在.ssh下新建config文件
Host github
HostName github.com
User manengyu@qq.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa

Host gitlab
HostName 192.168.8.15
User manengyu@qq.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa_gitlab
使用命令添加私钥
ssh-agent
ssh-add ~/.ssh/rsa（报错not open a connection时Windows:eval `ssh-agent`,CentOS:exec ssh-agent bash）
ssh-add -l

创建裸仓库（用于服务器中心仓库）
git init --bare <repo>
裸仓库需在.git/config中添加denyCurrentBranch = ignore才可push
执行git reset --hard后才可看见push代码
