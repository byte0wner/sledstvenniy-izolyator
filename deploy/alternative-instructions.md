инструкции если скрипт установки не отработал:

1. самое главное это создать бота в телеге и заполнить конфиг ниже:

```
BOT_TOKEN="токен бота из BotFather"
CHAT_ID="айди вашего чата с ботом"
LOG_PATH="путь/куда/будет/сохраняться/лог"
```

2. установить openssh если нету `sudo apt install openssh-server`
3. установить докер `sudo apt install docker.io`
4. спуллить из докера дебиан контейнер `sudo docker pull debian`
5. установить пакеты из `requirements.txt` с флагом `--break-system-packages`
6. вписать в `/etc/ssh/sshd_config` строку `ForceCommand /usr/bin/python3 <path_to_watchdog>/watchdog.py` (похуй куда)
7. установить https://gvisor.dev/docs/user_guide/install/


huinya:

- https://dohost.us/index.php/2025/09/14/implementing-ssh-forcecommand-for-restricted-shells/
- https://shaner.life/the-little-known-ssh-forcecommand/
- https://pickettsproblems.wordpress.com/2017/09/20/rdp-passthrough-connection/ VRDP (VirtualBox Remote Desktop Protocol)
- https://askubuntu.com/questions/1157448/how-do-i-configure-my-sshd-to-use-a-different-shell

ForceCommand
        Forces the execution of the command specified by
        ForceCommand, ignoring any command supplied by the client
        and ~/.ssh/rc if present.  The command is invoked by using
        the user's login shell with the -c option.  This applies
        to shell, command, or subsystem execution.  It is most
        useful inside a Match block.  The command originally
        supplied by the client is available in the
        SSH_ORIGINAL_COMMAND environment variable.  Specifying a
        command of internal-sftp will force the use of an in-
        process SFTP server that requires no support files when
        used with ChrootDirectory.  The default is none.