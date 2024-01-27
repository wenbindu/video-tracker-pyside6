from videotrackersystem.app import main
import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
else:
    print('running in a normal Python process')

if __name__ == '__main__':
    
    main()
