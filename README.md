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
To install all required packages and setup this package, run the following code.

```bash
git clone https://github.com/PavelTrutman/GoldFish.git
cd GoldFish
pip3 install -r requirements.txt
python3 setup.py install
```

## Usage
To run the backup, execute

```bash
goldFish config.yml
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
