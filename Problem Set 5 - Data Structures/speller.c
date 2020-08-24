// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int wordCount = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int key = hash(word);

    node *nodePTR = table[key];

    while (nodePTR != NULL)
    {
        if (strcasecmp(nodePTR -> word, word) == 0)
        {
            return true;
        }

        nodePTR = nodePTR -> next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int value = 0;

    // Add a value to Words
    for (int i = 0; word[i] != '\0'; i++)
    {
        value += tolower(word[i]);
    }

    return value % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Opens the dictionary file
    FILE *infile = fopen(dictionary, "r");

    // If there is no file, return false
    if (infile == NULL)
    {
        return false;
    }

    // Add the NULL value to the entire table
    for (int i = 0; i < N; i ++)
    {
        table[i] = NULL;
    }

    // Creates a new temp word, bacause the original is a CONST one
    char tmpWord[LENGTH + 1];

    // Reads each word in the file, until reachs the end of file
    while (fscanf(infile, "%s\n", tmpWord) != EOF)
    {
        // Crates a new temp node
        node *tmpNode = malloc(sizeof(node));

        // Makes a copy, from the original word to the new temp word
        strcpy(tmpNode->word, tmpWord);

        // Finding out where to put the current word
        int key = hash(tmpWord);

        // If the current position of the hash table is null, crates a new position
        if (table[key] == NULL)
        {
            tmpNode -> next = NULL;
            table[key] = tmpNode;
        }

        // If the current position of the hash table already exists, crates a new position
        else
        {
            tmpNode -> next = table[key];
            table[key] = tmpNode;
        }

        wordCount ++;
    }

    fclose(infile);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *nodePTR = table[i];

        while (nodePTR != NULL)
        {
            node *deleteMe = nodePTR;
            nodePTR = nodePTR -> next; // Goes to the next word
            free(deleteMe);
        }

        table[i] = NULL;
    }

    return true;
}
