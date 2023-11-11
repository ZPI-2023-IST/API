# API

### Example call to make_move action

    {
        "move":
            {
                "ml_no_cards": "TBD",
                "ml_src": "TBD",
                "ml_dst": "TBD"
            }
    }

### The program has a get_response event that is triggered by calling the make_move action and returns to each listener a JSON with the following structure:
    {
        "moves_vector": "moves",
        "game_board": "board", 
        "reward": 0, "state": 
        "State.ONGOING"
    }

### How to open it on your own comp
1. Clone the repo
2. Open the project in your IDE
3. Make venv
4. Install requirements
5. pip3 install git+https://github.com/ZPI-2023-IST/FreeCell.git
6. pip3 install git+https://github.com/ZPI-2023-IST/Translator.git@Z2-68_make_tr_a_package