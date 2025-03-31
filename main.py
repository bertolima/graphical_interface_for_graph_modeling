from src.App import App
from os import path
 
if __name__ == "__main__" :
    main_path = path.dirname(__file__)
    app = App(main_path=main_path)
    app.start()