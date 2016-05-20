# GoldFish #
GoldFish is a backup script written in Python 3.4 for creating incremental backups. When creating new backup a hardlink is created if the same file exists in previous backup, if not the file is copied to the backup.

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
