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