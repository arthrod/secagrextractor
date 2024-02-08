#sh
#!/bin/bash

# run_mainmongo.sh

while true; do
    # Run the mainmongo.py script
    python3 mainmongo.py

    # Generate a random delay between 2 and 10 seconds
    delay=$((RANDOM % 9 + 2))
    echo "Waiting for $delay seconds before the next run..."

    # Wait for the specified delay
    sleep $delay
done
