# GoldFish #
GoldFish is a backup utility for creating incremental backups. When creating new backup a hardlink is created if the same file exists in previous backup, if not the file is copied to the backup.

```
                    (@@@@@@@@@@%                           
                  &@@@       .@@@@@@@@@/                   
                 @@@                @@@@                   
                @@@                @@@                     
              .@@@@@@@@@@@@@@@@@&  @@                      
          (@@@@@/              &@@@@@&              /@@@@% 
       (@@@@                        @@@@/        @@@@@,@@@ 
     @@@@                              @@@@    @@@#   @@@  
    @@@                                   @@@&@@&    @@@   
  &@@       &@@/                            @@@     (@@    
 @@@       /@@@@                                    @@&    
 @@          @@                                     @@@    
 ,@@#                                       @@@     ,@@    
   @@@                                   @@@@,@@     @@@   
     @@@@                             &@@@&    @@@    @@@  
       &@@@@/                     #@@@@%        (@@@@# @@@ 
           @@@@@@@@@@%/,,,/%@@@@@@@@                @@@@@@ 
                 /@@@@@@@@@@@@&                            
                  @@@       @@                             
                   ,@@@.    @@@                            
                      @@@@@@@@@                     
```

## Installation
Install `pipx` on Debian, then install GoldFish from the repository:

```bash
sudo apt install pipx
pipx ensurepath
git clone https://github.com/PavelTrutman/GoldFish.git
cd GoldFish
pipx install .
```

If you ran `pipx ensurepath`, open a new terminal before running `goldFish`.

## Usage
To run the backup, execute

```bash
goldFish backup config.yml
```

with `config.yml` file looking like this:

```yml
folders:
  dest: /media/user/external_hdd/backups
  src:
  - /home/user/firstDirToBackup
  - /home/user/secondDirToBackup
  - /etc
  - /var/lib

database:
  enable: True
  path: db.sqlite
  linkMtimeDiffer: False
```
