# Lang_assignment1

## Language analytics assignment 1 description:
Assignment 1 - Collocation tool

In the previous lesson, we saw that words which frequently co-occur together in a given context are known as collocates. We also saw that we could calculate the strength of association between collocates, allowing us to see how much two words are related to one another. This is important because of the distributional hypothesis - that you can learn a lot about what a word means based on the other words that appear around it.

For this assignment, you will write a small Python program to perform collocational analysis using the string processing and NLP tools you've already encountered. Your script should do the following:

    Take a user-defined search term and a user-defined window size.
    Take one specific text which the user can define.
    Find all the context words which appear ± the window size from the search term in that text.
    Calculate the mutual information score for each context word.
    Save the results as a CSV file with (at least) the following columns: the collocate term; how often it appears as a collocate; how often it appears in the text; the mutual information score.

## Methods
As previously stated, this assignment has to do with the distributional hypothesis. The resulting script provides a csv of a key-word and its collocates, along with their mutual information scores, which should tell us something about the relationship between these words. The script utilizes the spacy nlp pipeline. The script begins with loading in a user-defined file, converting it all to lowercase, removing any non-alphanumerical characters and then running it through the nlp pipeline. 
Then, it takes a user-defined key-word and finds its collocates, with a window size of 5. Then, it extracts the necessary information for MI calculation; it counts how many times each collocate occurs in the whole text, how many times each collocate occurs close to the key-word and the size of the corpus. Then the script calculates the MI scores and saves the result to a csv with a user-defined name. 

## Usage
To get this script to run, you should first run the ```setup_lang.sh``` script. Then, you should download the ```100 English Novels``` corpus from here: https://github.com/computationalstylistics/100_english_novels and put it in the ```in``` folder. Then, you should point your command line to the ```lang_assignment1``` folder and run the ```assignment1.py``` script from the ```src``` folder, with the following command line arguments: ```-f``` which defines which file you want to work with, for instance ```Bennet_Helen_1910.txt``` which is the one I've been testing on. You also need to include ```-k``` which defines the key-word you want to work with, and finally, ```-o``` which defines the name of the output, for instance ```MI_score_Bennet_Helen.csv``` 

## Results
The script does what it needs to do, but with some room for improvement. For instance, in my test-runs, where I've been working with ```Bennet_Helen_1910.txt```, the strongest collocates are ```mr``` in first place and ```ollerenshaw``` in second. These words seems to refer to the same person, and should perhaps be counted as the same? However, without having read the novel, it is likely that ```mr``` could refer to other people as well - the point being that this method can lead to this sort of confusion. Beyond that, a lot of function words, such as ```but```, ```and``` and ```that``` make the list of strongest collocates, which doesn't necessarily tell us much about the bigger picture - we might have wanted to remove those. Further, some words seem to make the list multiple times, such as ```her``` having more than one entry. A bigger spacy model might be able to fix that.
