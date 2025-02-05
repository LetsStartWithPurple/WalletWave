from colorama import init, Fore
init()

def print_wave_banner():
        # Using Colorama's color codes
    BLUE = Fore.LIGHTBLUE_EX  # This replaces the ANSI code \033[94m
    RESET = Fore.RESET  # This replaces the ANSI code \033[0m

    wave_art = f"""



                           ::::::::::::--::                           
                      :.:::+----=---=-----:::::-                      
                   .:::--==-=-------------------:::                   
                .:::======----====-=-========-----+-:.                
               ::-=====-===-==+++++++===---------------.              
             ::==========+****:      ...:-:=:=-----------             
           ::========++*#:      .....:.....=:---.+:-:-----.           
          ::=======+*@               ::.:..:-+=-***+==-----:          
         ::======+*#{BLUE}     %@@@@@@@@@{RESET}    ...=+-*-*--:-:==-----:         
        ::=====+#*   {BLUE}.@@@@@%#@#**#@@@{RESET}:  :----*=-=.::++--------        
       .:====+#%   {BLUE}..      @*=#+*@@@@@%{RESET}  ..+-*+++:#**+++=--===.       
       :===+*#   {BLUE}...      @##+*@@={RESET}-{BLUE}::=@{RESET}  -=+.+:--.::  =-=---==-       
      .:==+%.  {BLUE}..    .@@@@+#*#@={RESET}-:--{BLUE}--*#{RESET}  .=.*++*.+*#*++=-=---=.      
      :==+@   {BLUE}    @@@@@++=@+#@={RESET}-----==+#%-=+++ -* .+.+.=--=====:      
      :+*@  {BLUE}   :@@@@#@+=@*--@%{RESET}---=======+**++*:+=:=*-=+=-======-      
      -%:  {BLUE}  #@@@%@*@=##:%--@%{RESET}:-=========+=++**+-*-=+.:===--===+      
         {BLUE}  @@@@%%@*%#=@#:@:*@@{RESET}-:-=============+++**==+++========+      
        {BLUE}@@@@@*#%#@*@=+@+:@%+*@@{RESET}::-==============================-      
      {BLUE}@@@@#@**@*%%#@=*@@::@:%#@@{RESET}::--===========------=-========:      
       {BLUE}+##@##%%*@#%%=*%@:::@+##@@%{RESET}:::--===============----:::--       
       {BLUE}-*#%**@**@#%@=**@@:::@#*%*@@@#{RESET}-:::::------::::-{BLUE}=#@@@@@@%{RESET}       
        {BLUE}-#%#*@*#%%#@-**%@@:-:+@+##%=@@@@@@@%%%@@@@@@#**+==*#%+.       
         +%*#@**#@*@@+*+@@@---:=@%%%#**++****+===--=++++==---         
          #*##@#*@@%@:#**%@@@--=-::@@@%%%%%%%######*+====+*=          
           =*#@#**@%@@.*#**@%@@--*******++++======-::**++*-           
            =*#@#*#@%@@+ %#**%%@@#:.::::::::::::::-----=+-            
             ==*@***@@@@@..#%%*%%@@@@@@@%***+++++****%%+              
               :+%#**%@@@@@# :+*=#@@@@@@@@@@@@@@@%%%%+.               
                  #@%#*%@@@@@#**-...........::::*%*-                  
                    .=*#%=@@@@@@%%%%%%%%%@@@@@@*:                     
                        .:-*+@@@@@@@@@@@@@%+{RESET}                          


                      {BLUE}==WELCOME TO WALLETWAVE=={RESET}                                                                                                             
    """
    print(wave_art)

if __name__=="__main__":
    print_wave_banner()
