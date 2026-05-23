"""
Wani-Doko! (ワニどこ!) — 程式進入點 (Entry Point)

NTU Japanese 1 Vocabulary Trainer
PBC Final Project
"""

from controllers.app_controller import AppController


def main():
    app = AppController()
    app.start()


if __name__ == "__main__":
    main()
